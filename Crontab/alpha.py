"""
alpha运维
"""
from .base import AbstractJob
from .base import crontab_dir


def append_jobs(jobs):
    jobs.append(local_alpha_check())
    jobs.append(array_alpha_feature())
    jobs.append(array_alpha_algo())
    jobs.append(array_alpha_gru_encoder())


class local_alpha_check(AbstractJob):
    def __init__(self, ):
        super(local_alpha_check, self).__init__()
        self.job_name = 'local_alpha_check'
        self.dependent_job_list = ['gen_otmd']
        self.system_syntax = {}
        # self.run_daytime = True
        self.max_running_second = 3600 * 1.5
        self.send_email = 1
        self.system_syntax = {}
        self.system_syntax['00:01:00'] = "cd %s && source ./%s" % (crontab_dir, "local_alpha_check.yml")
        self.time_list = self.system_syntax.keys()
        self.check_run()
        print(self.system_syntax)


class array_alpha_feature(AbstractJob):
    def __init__(self, ):
        super(array_alpha_feature, self).__init__()
        self.job_name = 'array_alpha_feature'
        self.dependent_job_list = ['local_alpha_check']
        self.system_syntax = {}
        # self.run_daytime = True
        self.max_running_second = 3600 * 1.5
        self.send_email = 1
        self.system_syntax = {}
        self.system_syntax['00:10:00'] = "cd %s && source ./%s" % (crontab_dir, "array_alpha_feature.yml")
        self.time_list = self.system_syntax.keys()
        self.check_run()
        print(self.system_syntax)


class array_alpha_algo(AbstractJob):
    def __init__(self, ):
        super(array_alpha_algo, self).__init__()
        self.job_name = 'array_alpha_algo'
        self.dependent_job_list = ['array_alpha_feature']
        self.system_syntax = {}
        # self.run_daytime = True
        self.max_running_second = 3600 * 1.5
        self.send_email = 1
        self.system_syntax = {}
        self.system_syntax['00:10:00'] = "cd %s && source ./%s" % (crontab_dir, "array_alpha_algo.yml")
        self.time_list = self.system_syntax.keys()
        self.check_run()
        print(self.system_syntax)


class array_alpha_gru_encoder(AbstractJob):
    def __init__(self, ):
        super(array_alpha_gru_encoder, self).__init__()
        self.job_name = 'array_alpha_gru_encoder'
        self.system_syntax = {}
        self.dependent_job_list = ['array_alpha_algo', ]
        # self.run_daytime = True
        self.max_running_second = 3600 * 2
        self.send_email = 1
        self.system_syntax = {}
        self.system_syntax['00:01:00'] = "cd %s && source ./%s" % (crontab_dir, "array_alpha_gru_encoder.yml")
        self.time_list = self.system_syntax.keys()
        self.check_run()
        print(self.system_syntax)
