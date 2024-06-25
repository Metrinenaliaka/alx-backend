const redis = require('redis');
const kue = require('kue');
const express = require('express');
const { promisify } = require('util');

const client = redis.createClient();
const queue = kue.createQueue({
  redis: {
    port: 6379,
    host: 'localhost',
  },
});
const app = express();

const getAsync = promisify(client.get).bind(client);
const setAsync = promisify(client.set).bind(client);

async function reserveSeat(number) {
  await setAsync('available_seats', number);
}

async function getCurrentAvailableSeats() {
  const numberOfAvailableSeats = await getAsync('available_seats');
  return parseInt(numberOfAvailableSeats, 10) || 0; // Handle potential parsing errors
}

const initialAvailableSeats = 50;
let reservationEnabled = true;

app.get('/available_seats', async (req, res) => {
  const numberOfAvailableSeats = await getCurrentAvailableSeats();
  res.json({ numberOfAvailableSeats });
});

app.get('/reserve_seat', async (req, res) => {
  if (!reservationEnabled) {
    return res.json({ status: 'Reservation are blocked' });
  }

  try {
    const job = queue.create('reserve_seat', {}).save((err) => {
      if (!err) {
        res.json({ status: 'Reservation in process' });
      } else {
        console.error('Error creating reservation job:', err);
        res.json({ status: 'Reservation failed' });
      }
    });

    job.on('complete', () => {
      console.log(`Seat reservation job ${job.id} completed`);
    }).on('failed', (errorMessage) => {
      console.error(`Seat reservation job ${job.id} failed: ${errorMessage}`);
    });
  } catch (error) {
    console.error('Error reserving seat:', error);
    res.json({ status: 'Reservation failed' });
  }
});

app.get('/process', async (req, res) => {
  res.json({ status: 'Queue processing' });
  queue.process('reserve_seat', async (job, done) => {
    try {
      const currentAvailableSeats = await getCurrentAvailableSeats();
      if (currentAvailableSeats > 0) {
        await reserveSeat(currentAvailableSeats - 1);
        if (currentAvailableSeats - 1 === 0) {
          reservationEnabled = false;
        }
        done();
      } else {
        throw new Error('Not enough seats available');
      }
    } catch (error) {
      console.error('Error reserving seat:', error);
      done(new Error('Not enough seats available'));
    }
  });
});

app.listen(1245, async () => {
  await reserveSeat(initialAvailableSeats);
  console.log('API listening on port 1245');
});
