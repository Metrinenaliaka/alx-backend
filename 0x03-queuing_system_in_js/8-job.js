export default function createPushNotificationsJobs(jobs, queue) {
    if (!Array.isArray(jobs)) throw new Error('Jobs is not an array');
  
    for (const jobObj of jobs) {
      const job = queue.create('push_notification_code_3', jobObj);
  
      job.on('enqueue', () => console.log(`Notification job created: ${job.id}`))
        .on('complete', () => console.log(`Nofification job ${job.id} completed`))
        .on('failed', (err) => console.log(`Nofification job ${job.id} failed: ${err}`))
        .on('progress', (progress) => console.log(`Nofification job ${job.id} ${progress}% complete`));
  
      job.save();
    }
  }
  