from apscheduler.jobstores.base import JobLookupError
from apscheduler.schedulers.background import BackgroundScheduler
import time
from datetime import datetime
from collections import defaultdict
from apscheduler.events import EVENT_JOB_ERROR, EVENT_JOB_EXECUTED

class Scheduler:
    _instance = None
    d = defaultdict(int)
    jobs = {}
    def __init__(self):
        self.cnt = 0
        self.sched = BackgroundScheduler()
        # self.sched.add_listener(self.listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
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
        try:
            # self.sched.remove_job(job_id)
            self.jobs[job_id].remove()
            self.jobs[job_id] = None
            print(f'scheduler {job_id} has been removed')
        except JobLookupError as err:
            print("fail to stop Scheduler: {err}".format(err=err))
            return

    def kill_on_condition(self, job_id, cnt):
        self.d[job_id] += 1
        print(f'Job id {job_id} is running {self.d[job_id]} times')
        if self.d[job_id] == cnt:
            self.kill_scheduler(job_id)
            return True
        return False
    

    def hello(self, type, job_id):
        print("%s Scheduler process_id[%s] : %d" % (type, job_id, time.localtime().tm_sec))

    def scheduler(self, type, job_id, cnt):
        self.cnt = 0
        print("{type} Scheduler Start".format(type=type))
        if type == 'interval':
            self.jobs[job_id] = self.sched.add_job(self.kill_on_condition, type, seconds=2, id=job_id, args=(job_id, cnt))
        elif type == 'cron':
            self.sched.add_job(self.hello, type, day_of_week='mon-fri',
                                                 hour='0-23', second='0-59',
                                                 id=job_id, args=(type, job_id))
    
    def setup_ticketing(self, func, args, job_id):
        print(f"Setting up job {job_id}")
        self.jobs[job_id] = self.sched.add_job(func, seconds=15, trigger="interval", id=job_id, args=args)

    def setup_scrapping(self, func, job_id):
        print(f"Setting up scheduler {job_id}")
        self.jobs[job_id] = self.sched.add_job(func, seconds=300, trigger='interval', id=job_id, next_run_time=datetime.now())

    def listener(self, event):
        if not event.exception:
            print("Event has occurred", event.job_id, event.retval)
            if event.retval:
                self.kill_scheduler(event.job_id)

def setup_ticketing(func, args, job_id):
    sched = Scheduler()
    print(f"setup_ticketing running scheduler: {id(sched)}, job: {job_id}")
    sched.setup_ticketing(func, args, job_id)

def setup_tickets_scrapping(func, job_id):
    sched = Scheduler()
    print(f"setup_tickets_scrapping running scheduler: {id(sched)}, job: {job_id}")
    sched.setup_scrapping(func, job_id)

cnt = 0
a = "Hello func"
def hello(word):
    print("Hello", word)
    global cnt
    cnt += 1
    if cnt == 3:
        return True
b = "world"
if __name__ == '__main__':
    # scheduler.scheduler('cron', "1")
    sc = Scheduler()
    sc.sched.add_listener(sc.listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
    sc.setup_ticketing(hello, (b), a)
    while True:
        pass
    # while True:
    #     '''
    #     count 제한할 경우 아래와 같이 사용
    #     '''
    #     print("Running main process")
    #     time.sleep(1)
    #     count += 1
    #     if count == 10:
    #         scheduler.kill_scheduler("1")
    #         print("Kill cron Scheduler")
    #     elif count == 15:
    #         scheduler.kill_scheduler("2")
    #         print("Kill interval Scheduler")