from apscheduler.jobstores.base import JobLookupError
from apscheduler.schedulers.background import BackgroundScheduler
import time
import pytz
from datetime import datetime
from collections import defaultdict
from apscheduler.events import EVENT_JOB_ERROR, EVENT_JOB_EXECUTED

class Scheduler:
    _instance = None
    jobs = {}
    def __init__(self):
        self.cnt = 0
        self.sched = BackgroundScheduler(timezone=pytz.timezone('Asia/Seoul'))
        self.sched.add_listener(self.listener_foundSeat, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
        self.sched.start()
        self.job_id = ''

    def __new__(class_):
        if not isinstance(class_._instance, class_):
            class_._instance = object.__new__(class_)
        return class_._instance

    def __del__(self):
        self.shutdown()
        
    def shutdown(self):
        self.sched.shutdown()

    def kill_scheduler(self, job_id):
        res = ""
        try:
            # self.sched.remove_job(job_id)
            self.jobs[job_id].remove()
            self.jobs[job_id] = None
            res = f'@kill_scheduler - scheduler {job_id} has been removed'
        except Exception as err:
            res = "fail to stop Scheduler: {err}".format(err=err)
        return res
    
    def kill_every_scheduler(self):
        for job in self.jobs:
            try:
                self.jobs[job].remove()
            except:
                pass
        
        self.jobs.clear()
        
    def get_active_jobs(self):
        # res = self.jobs.keys()
        # print(res)
        # return self.jobs.keys()
        return str(self.jobs)

    def setup_login(self, func, args, run_date, job_id):
        print(f"@Scheduler:setup_login - Job '{job_id}' is added to the scheduler")
        print(f"@Scheduler:setup_login - It will be executed at {run_date}, current time is {datetime.now()}")
        self.jobs[job_id] = self.sched.add_job(func, 'date', run_date=run_date, args=args, id=job_id)

    def setup_ticketing(self, func, args, seconds, next_run_time, job_id):
        res = ""
        try:
            self.jobs[job_id] = self.sched.add_job(func, seconds=seconds, trigger="interval", id=job_id, args=args, next_run_time=next_run_time, max_instances=5)
            res = f"@Scheduler:setup_ticketing - Job '{job_id}' is added to the scheduler"
        except Exception as err:
            res = "fail to setup Scheduler: {err}".format(err=err)
        print(res)
        return res

    def search_and_find(self, func, args, run_date, job_id):
        res = ""
        try:
            self.jobs[job_id] = self.sched.add_job(func, trigger='date', args=args, run_date=run_date)
            res = f"@Scheduler:setup_ticketing - Job '{job_id}' is added to the scheduler"
        except Exception as err:
            res = "fail to setup Scheduler: {err}".format(err=err)
        print(res)
        return res

    def setup_scrapping(self, func, job_id):
        print(f"Setting up scheduler {job_id}")
        self.jobs[job_id] = self.sched.add_job(func, seconds=300, trigger='interval', id=job_id, next_run_time=datetime.now())

    def listener_foundSeat(self, event):
        """
        It listens recursive scheduler events and it stops the task 'setup_ticketing' when given function (Ticketing().findSeatRecursively in this case)
        returns 2 (means user has two tickets for the same train)

        Returns:
            numofTicket (int): 
            Return -1 if something went wrong while trying to find the train.
            Return 0 if it finds the train and opens a page for it.
            Return 1 if it finds the train and opens a page for it, but notices there is a ticket for that train.
            Return 2 if it finds the train, but notices two tickets so it is not able to reserve more seats.
        """
        if not event.exception:
            print(f"@listener_foundSeat - listens to event on '{event.job_id}', return value is {event.retval}")
            if event.retval == 2:
                print(f"@listener_foundSeat - ends the task '{event.job_id}' as reservation request was made successfully")
                self.kill_scheduler(event.job_id)

def setup_tickets_scrapping(func, job_id):
    sched = Scheduler()
    print(f"setup_tickets_scrapping running scheduler: {id(sched)}, job: {job_id}")
    sched.setup_scrapping(func, job_id)
