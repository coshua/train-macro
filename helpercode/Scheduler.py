from apscheduler.jobstores.base import JobLookupError
from apscheduler.schedulers.background import BackgroundScheduler
import time
from collections import defaultdict

class Scheduler:
    _instance = None
    d = defaultdict(int)
    jobs = {}
    def __init__(self):
        self.cnt = 0
        self.sched = BackgroundScheduler()
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
    
    def setup_ticketing(self, func, exe_time, job_id):
        self.sched.add_job(func, "cron", 
        month=exe_time["month"], hour='11', minute="8-11", id=job_id)
    
    def hello(self, type, job_id):
        print("%s Scheduler process_id[%s] : %d" % (type, job_id, time.localtime().tm_sec))

    def scheduler(self, type, job_id, cnt):
        print(self.sched.get_jobs())
        self.cnt = 0
        print("{type} Scheduler Start".format(type=type))
        if type == 'interval':
            self.jobs[job_id] = self.sched.add_job(self.kill_on_condition, type, seconds=2, id=job_id, args=(job_id, cnt))
        elif type == 'cron':
            self.sched.add_job(self.hello, type, day_of_week='mon-fri',
                                                 hour='0-23', second='0-59',
                                                 id=job_id, args=(type, job_id))
    
    def setup_scheduler(self, func, type, job_id, cnt):
        print(f"Setting up scheduler {job_id}")
        self.jobs[job_id] = self.sched.add_job(func, seconds=2, trigger='interval', id=job_id)
def setup_ticketing(job_id):
    sched = Scheduler()
    print(f"setup_ticketing running {id(sched)}")
    sched.scheduler('interval', job_id, 5)

def setup_tickets_scrapping(func, job_id):
    sched = Scheduler()
    print(f"setup_tickets_scrapping running {id(sched)}")
    sched.setup_scheduler(func, 'interval', job_id, 3)
def hello(job_id, cnt):
    print("Hello")
if __name__ == '__main__':
    # scheduler.scheduler('cron', "1")
    sc = Scheduler()
    sc.setup_scheduler(hello, 'interval', 'hf', 5)
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