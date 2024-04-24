"""
任务的起点
"""
from .base import AbstractJob
from .base import switch_hour, crontab_dir


def append_jobs(jobs):
    jobs.append(local_check())


class after_2000(AbstractJob):
    def __init__(self,):
        super(after_2000, self).__init__()
        self.job_name = 'after_2000'
        self.dependent_job_list = []
        self.time_list = ['16:00:00']
        self.system_syntax = 'pwd && sleep 1'
        self.check_run()


class local_check(AbstractJob):
    def __init__(self, ):
        super(local_check, self).__init__()
        self.job_name = 'local_check'
        self.time_list = ['%s:05:00' % (switch_hour)]
        self.system_syntax = "cd %s && source ./%s" % (crontab_dir, "local_check.yml")
        self.max_running_second = 3600 * 1
        self.send_email = 0
        self.check_run()
