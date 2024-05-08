
from .base import AbstractJob
from .base import crontab_dir


def append_jobs(jobs):
    jobs.append(gen_50ms_otmd_dev())


class gen_50ms_otmd_dev(AbstractJob):
    def __init__(self, ):
        super(gen_1d_md, self).__init__()
        self.job_name = 'gen_50ms_otmd_dev'
        self.system_syntax = {}
        self.dependent_job_list = ['local_check',]
        # self.run_daytime = True
        self.max_running_second = 3600 * 1
        self.send_email = 1
        self.system_syntax = {}
        self.system_syntax['00:00:00'] = "cd %s && source ./%s" % (crontab_dir, "50ms_otmd_dev.yml")
        self.time_list = self.system_syntax.keys()
        self.check_run()
        print(self.system_syntax)

