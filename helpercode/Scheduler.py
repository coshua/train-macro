from apscheduler.jobstores.base import JobLookupError
from apscheduler.schedulers.background import BackgroundScheduler
import time


class Scheduler:
    def __init__(self):
        self.cnt = 0
        self.sched = BackgroundScheduler()
        self.sched.start()
        self.job_id = ''

    def __del__(self):
        self.shutdown()

    def shutdown(self):
        self.sched.shutdown()

    def kill_scheduler(self, job_id):
        try:
            self.sched.remove_job(job_id)
            print(f'scheduler {job_id} has been removed')
        except JobLookupError as err:
            print("fail to stop Scheduler: {err}".format(err=err))
            return

    def kill_on_condition(self, job_id):
        self.cnt += 1
        print(f'Running {self.cnt - 1} times')
        if self.cnt == 4:
            self.kill_scheduler(job_id)
    
    def setup_ticketing(self, func, exe_time, job_id):
        self.sched.add_job(func, "cron", 
        month=exe_time["month"], hour='11', minute="8-11", id=job_id)
    
    def hello(self, type, job_id):
        print("%s Scheduler process_id[%s] : %d" % (type, job_id, time.localtime().tm_sec))

    def scheduler(self, type, job_id):
        self.cnt = 0
        print("{type} Scheduler Start".format(type=type))
        if type == 'interval':
            self.sched.add_job(self.kill_on_condition, type, seconds=2, id=job_id, args=(job_id))
        elif type == 'cron':
            self.sched.add_job(self.hello, type, day_of_week='mon-fri',
                                                 hour='0-23', second='0-59',
                                                 id=job_id, args=(type, job_id))


if __name__ == '__main__':
    scheduler = Scheduler()
    # scheduler.scheduler('cron', "1")
    scheduler.scheduler('interval', "1")
    while True:
        pass
    count = 0
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