"""
hft
"""
from .base import AbstractJob
from .base import crontab_dir


def append_jobs(jobs):
    jobs.append(gen_hft_1d())
    jobs.append(local_etf_log())
    


class gen_hft_1d(AbstractJob):
    """
    hft 日频数据
    """

    def __init__(self, ):
        super(gen_hft_1d, self).__init__()
        self.job_name = 'gen_hft_1d'
        self.system_syntax = {}
        self.dependent_job_list = []
        self.run_daytime = True
        self.max_running_second = 3600
        self.send_email = 1
        self.system_syntax = {}
        real_time_str = "15:15:00"
        self.system_syntax[real_time_str] = "cd %s && source ./%s" % (crontab_dir, "local_hft_1d.yml")
        self.time_list = self.system_syntax.keys()
        self.check_run()





class local_etf_log(AbstractJob):
    """
    下载日志，signal collect
    """

    def __init__(self, ):
        super(local_etf_log, self).__init__()
        self.job_name = 'local_etf_log'
        self.system_syntax = {}
        self.dependent_job_list = []
        self.run_daytime = True
        self.max_running_second = 3600
        self.send_email = 1
        self.system_syntax = {}
        self.system_syntax["11:45:00"] = "cd %s && source ./%s.yml" % (crontab_dir, self.job_name)
        self.system_syntax["15:15:00"] = "cd %s && source ./%s.yml" % (crontab_dir, self.job_name)
        self.time_list = self.system_syntax.keys()
        self.check_run()
