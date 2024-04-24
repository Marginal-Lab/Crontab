
from .base import AbstractJob
from .base import crontab_dir


def append_jobs(jobs):
    jobs.append(gen_1d_md())
    jobs.append(gen_otmd())
    jobs.append(check_md())
    jobs.append(gen_feature())
    jobs.append(check_feature())
    jobs.append(local_mv2oss())


class gen_1d_md(AbstractJob):
    def __init__(self, ):
        super(gen_1d_md, self).__init__()
        self.job_name = 'gen_1d_md'
        self.system_syntax = {}
        self.dependent_job_list = ['local_check',]
        # self.run_daytime = True
        self.max_running_second = 3600 * 1
        self.send_email = 1
        self.system_syntax = {}
        self.system_syntax['00:00:00'] = "cd %s && source ./%s" % (crontab_dir, "1d_md.yml")
        self.time_list = self.system_syntax.keys()
        self.check_run()
        print(self.system_syntax)


class gen_otmd(AbstractJob):
    def __init__(self, ):
        super(gen_otmd, self).__init__()
        self.job_name = 'gen_otmd'
        self.system_syntax = {}
        self.dependent_job_list = ['gen_1d_md',]
        # self.run_daytime = True
        self.max_running_second = 3600 * 5
        self.send_email = 1
        self.system_syntax = {}
        self.system_syntax['00:01:00'] = "cd %s && source ./%s" % (crontab_dir, "0ms_otmd.yml")
        self.system_syntax['00:02:00'] = "cd %s && source ./%s" % (crontab_dir, "3000ms_otmd.yml")
        self.system_syntax['00:03:00'] = "cd %s && source ./%s" % (crontab_dir, "50ms_otmd.yml")
        self.system_syntax['00:04:00'] = "cd %s && source ./%s" % (crontab_dir, "50ms_otmd_sz.yml")
        self.system_syntax['00:05:00'] = "cd %s && source ./%s" % (crontab_dir, "1m_otmd.yml")
        self.system_syntax['00:06:00'] = "cd %s && source ./%s" % (crontab_dir, "1m_volumedetail.yml")
        self.system_syntax['00:07:00'] = "cd %s && source ./%s" % (crontab_dir, "1m_multilevel.yml")
        self.time_list = self.system_syntax.keys()
        self.check_run()
        print(self.system_syntax)


class check_md(AbstractJob):
    def __init__(self, ):
        super(check_md, self).__init__()
        self.job_name = 'check_md'
        self.system_syntax = {}
        self.dependent_job_list = ['gen_otmd',]
        # self.run_daytime = True
        self.max_running_second = 3600 * 5
        self.send_email = 1
        self.system_syntax = {}
        self.system_syntax['00:01:00'] = "cd %s && source ./%s" % (crontab_dir, "check_md.yml")
        self.time_list = self.system_syntax.keys()
        self.check_run()
        print(self.system_syntax)


class gen_feature(AbstractJob):
    def __init__(self, ):
        super(gen_feature, self).__init__()
        self.job_name = 'gen_feature'
        self.system_syntax = {}
        self.dependent_job_list = ['gen_otmd',]
        # self.run_daytime = True
        self.max_running_second = 3600 * 1.5
        self.send_email = 1
        self.system_syntax = {}
        self.system_syntax['00:00:00'] = "cd %s && source ./%s" % (crontab_dir, "50ms_feature_250ms.yml")
        self.system_syntax['00:01:00'] = "cd %s && source ./%s" % (crontab_dir, "50ms_feature_3000ms.yml")
        self.system_syntax['00:02:00'] = "cd %s && source ./%s" % (crontab_dir, "50ms_feature.yml")
        self.system_syntax['00:03:00'] = "cd %s && source ./%s" % (crontab_dir, "50ms_feature_250ms_sh.yml")
        self.system_syntax['00:04:00'] = "cd %s && source ./%s" % (crontab_dir, "50ms_feature_3000ms_sh.yml")
        self.system_syntax['00:05:00'] = "cd %s && source ./%s" % (crontab_dir, "50ms_feature_sh.yml")
        # self.system_syntax['00:03:00'] = "cd %s && source ./%s"%(crontab_dir, "3000ms_feature.yml")
        # self.system_syntax['00:04:00'] = "cd %s && source ./%s"%(crontab_dir, "1d_feature.yml")
        # self.system_syntax['00:05:00'] = "cd %s && source ./%s"%(crontab_dir, "seq_map.yml")
        # self.system_syntax['00:06:00'] = "cd %s && source ./%s"%(crontab_dir, "seq_feature.yml")
        self.time_list = self.system_syntax.keys()
        self.check_run()
        print(self.system_syntax)


class check_feature(AbstractJob):
    def __init__(self, ):
        super(check_feature, self).__init__()
        self.job_name = 'check_feature'
        self.system_syntax = {}
        self.dependent_job_list = ['gen_feature', 'array_alpha_algo']
        # self.run_daytime = True
        self.max_running_second = 3600 * 5
        self.send_email = 1
        self.system_syntax = {}
        self.system_syntax['00:01:00'] = "cd %s && source ./%s" % (crontab_dir, "check_feature.yml")
        self.time_list = self.system_syntax.keys()
        self.check_run()
        print(self.system_syntax)


class local_mv2oss(AbstractJob):
    """
    将数据集移动到oss存储
    """

    def __init__(self, ):
        super(local_mv2oss, self).__init__()
        self.job_name = 'local_mv2oss'
        self.system_syntax = {}
        self.dependent_job_list = ['check_md', 'check_feature']
        # self.run_daytime = True
        self.max_running_second = 3600 * 5
        self.send_email = 1
        self.system_syntax = {}
        self.system_syntax['00:01:00'] = "cd %s && source ./%s" % (crontab_dir, "local_mv2oss.yml")
        self.time_list = self.system_syntax.keys()
        self.check_run()
        print(self.system_syntax)
