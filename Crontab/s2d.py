"""
s2d项目
"""

from .base import AbstractJob
from .base import crontab_dir


def append_jobs(jobs):
    jobs.append(s2d_dataset())
    jobs.append(s2d_linear())
    jobs.append(s2d_gru())


class s2d_dataset(AbstractJob):
    """
    2.5版本的数据集
    """

    def __init__(self, ):
        super(s2d_dataset, self).__init__()
        self.job_name = 's2d_dataset'
        self.system_syntax = {}
        self.dependent_job_list = ['gen_feature', ]
        # self.run_daytime = True
        self.max_running_second = 3600 * 2
        self.send_email = 1
        self.system_syntax = {}
        self.system_syntax['00:01:00'] = "cd %s && source ./%s" % (crontab_dir, "array_s2d_dataset.yml")
        self.time_list = self.system_syntax.keys()
        self.check_run()
        print(self.system_syntax)


class s2d_linear(AbstractJob):
    """
    2.5版本的s2d_linear
    """

    def __init__(self, ):
        super(s2d_linear, self).__init__()
        self.job_name = 's2d_linear'
        self.system_syntax = {}
        self.dependent_job_list = ['s2d_dataset', ]
        # self.run_daytime = True
        self.max_running_second = 3600 * 2
        self.send_email = 1
        self.system_syntax = {}
        self.system_syntax['00:01:00'] = "cd %s && source ./%s" % (crontab_dir, "array_s2d_linear.yml")
        self.time_list = self.system_syntax.keys()
        self.check_run()
        print(self.system_syntax)


class s2d_gru(AbstractJob):
    """
    2.5版本的s2d_gru
    """

    def __init__(self, ):
        super(s2d_gru, self).__init__()
        self.job_name = 's2d_gru'
        self.system_syntax = {}
        self.dependent_job_list = ['s2d_dataset', ]
        # self.run_daytime = True
        self.max_running_second = 3600 * 2
        self.send_email = 1
        self.system_syntax = {}
        self.system_syntax['00:01:00'] = "cd %s && source ./%s" % (crontab_dir, "array_s2d_gru.yml")
        self.time_list = self.system_syntax.keys()
        self.check_run()
        print(self.system_syntax)
