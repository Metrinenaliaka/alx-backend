import createPushNotificationsJobs from './8-job';
import { expect } from 'chai';
import kue from 'kue';

const queue = kue.createQueue();

describe('createPushNotificationsJobs', () => {
  before(() => queue.testMode.enter());
  afterEach(() => queue.testMode.clear());
  after(() => queue.testMode.exit());

  it('display an error message if jobs is not an array', () => {
    expect(() => createPushNotificationsJobs('jobs', queue)).to.throw(Error, 'Jobs is not an array');
  });

  it('create two new jobs to the queue', () => {
    const jobs = [
      {
        phoneNumber: '918456789',
        message: 'This is the code to verify your account',
      },
      {
        phoneNumber: '408123567',
        message: 'This is the code to verify your account',
      },
    ];

    createPushNotificationsJobs(jobs, queue);

    expect(queue.testMode.jobs.length).to.equal(2);

    expect(queue.testMode.jobs[0].data).to.deep.equal(jobs[0]);
    expect(queue.testMode.jobs[1].data).to.deep.equal(jobs[1]);

    expect(queue.testMode.jobs[0].type).to.equal('push_notification_code_3');
    expect(queue.testMode.jobs[1].type).to.equal('push_notification_code_3');
  });
});