"""
alpha
"""
import datetime
from .base import AbstractJob
from .base import crontab_dir


def append_jobs(jobs):
    jobs.append(update_instrument_info())
    timestr_list = ['10:06:00', '11:35:00', '13:36:00', '15:05:00']  # 目前留足25min给运维
    run_daytime = True
    for t, timestr in enumerate(timestr_list):
        if t == 0:
            last_time_str = None
        else:
            last_time_str = timestr_list[t - 1]
        jobs.append(clear_realtime(timestr, run_daytime, last_time_str))
        jobs.append(gen_realtime_otmd(timestr, run_daytime))
        jobs.append(gen_realtime_feature(timestr, run_daytime))
        jobs.append(gen_realtime_pred(timestr, run_daytime))
        jobs.append(check_realtime_otmd(timestr, run_daytime))


class update_instrument_info(AbstractJob):
    def __init__(self):
        super(update_instrument_info, self).__init__()
        self.job_name = 'update_instrument_info'
        self.system_syntax = {}
        self.dependent_job_list = []
        self.run_daytime = True
        self.max_running_second = 3600 * 5
        self.send_email = 1
        self.system_syntax = {}
        real_time_str = "09:40:00"
        self.system_syntax[real_time_str] = "cd %s && source ./%s" % (crontab_dir, "local_update_instrument_info.yml")
        self.time_list = self.system_syntax.keys()
        self.check_run()
        print(self.system_syntax)


class clear_realtime(AbstractJob):
    def __init__(self, time_str, run_daytime, last_time_str=None):
        super(clear_realtime, self).__init__()
        self.job_name = 'clear_realtime_%s' % (time_str.replace(':', ''))
        self.system_syntax = {}
        if last_time_str is None:
            self.dependent_job_list = ['update_instrument_info']
        else:
            self.dependent_job_list = ['gen_realtime_pred_%s' % (last_time_str.replace(':', ''))]
        self.run_daytime = run_daytime
        self.max_running_second = 3600 * 5
        self.send_email = 1
        self.system_syntax = {}
        # 减少五分钟
        time_format = "%H:%M:%S"
        time_obj = datetime.datetime.strptime(time_str, time_format)
        real_time_str = (time_obj - datetime.timedelta(minutes=5)).strftime(time_format)
        self.system_syntax[real_time_str] = "cd %s && source ./%s" % (crontab_dir, "local_clear_realtime.yml")
        self.time_list = self.system_syntax.keys()
        self.check_run()
        print(self.system_syntax)


class gen_realtime_otmd(AbstractJob):
    def __init__(self, time_str, run_daytime):
        super(gen_realtime_otmd, self).__init__()
        self.job_name = 'gen_realtime_otmd_%s' % (time_str.replace(':', ''))
        self.system_syntax = {}
        self.dependent_job_list = ['clear_realtime_%s' % (time_str.replace(':', ''))]
        self.run_daytime = run_daytime
        self.max_running_second = 3600 * 5
        self.send_email = 1
        self.system_syntax = {}
        time_format = "%H:%M:%S"
        # 将时间字符串解析为datetime对象
        time_obj = datetime.datetime.strptime(time_str, time_format)
        self.system_syntax[time_str] = "cd %s && source ./%s" % (crontab_dir, "1m_otmd_realtime.yml")
        next_time_str = (time_obj + datetime.timedelta(seconds=5)).strftime(time_format)
        self.system_syntax[next_time_str] = "cd %s && source ./%s" % (crontab_dir, "1m_multilevel_realtime.yml")
        self.time_list = self.system_syntax.keys()
        self.check_run()
        print(self.system_syntax)


class check_realtime_otmd(AbstractJob):
    def __init__(self, time_str, run_daytime):
        super(check_realtime_otmd, self).__init__()
        self.job_name = 'check_realtime_otmd_%s' % (time_str.replace(':', ''))
        self.system_syntax = {}
        self.dependent_job_list = ['gen_realtime_otmd_%s' % (time_str.replace(':', ''))]
        self.run_daytime = run_daytime
        self.max_running_second = 3600 * 5
        self.send_email = 1
        self.system_syntax = {}
        time_format = "%H:%M:%S"
        # 将时间字符串解析为datetime对象
        time_obj = datetime.datetime.strptime(time_str, time_format)
        self.system_syntax[time_str] = "cd %s && source ./%s" % (crontab_dir, "local_check_realtime_otmd.yml")
        self.time_list = self.system_syntax.keys()
        self.check_run()
        print(self.system_syntax)


class gen_realtime_feature(AbstractJob):
    def __init__(self, time_str, run_daytime):
        super(gen_realtime_feature, self).__init__()
        self.job_name = 'gen_realtime_feature_%s' % (time_str.replace(':', ''))
        self.system_syntax = {}
        self.dependent_job_list = ['gen_realtime_otmd_%s' % (time_str.replace(':', ''))]
        self.run_daytime = run_daytime
        self.max_running_second = 3600 * 5
        self.send_email = 1
        self.system_syntax = {}
        time_format = "%H:%M:%S"
        # 将时间字符串解析为datetime对象
        time_obj = datetime.datetime.strptime(time_str, time_format)
        self.system_syntax[time_str] = "cd %s && source ./%s" % (crontab_dir, "array_alpha_feature_realtime.yml")
        self.time_list = self.system_syntax.keys()
        self.check_run()
        print(self.system_syntax)


class gen_realtime_pred(AbstractJob):
    def __init__(self, time_str, run_daytime):
        super(gen_realtime_pred, self).__init__()
        self.job_name = 'gen_realtime_pred_%s' % (time_str.replace(':', ''))
        self.system_syntax = {}
        self.dependent_job_list = ['gen_realtime_feature_%s' % (time_str.replace(':', ''))]
        self.run_daytime = run_daytime
        self.max_running_second = 3600 * 5
        self.send_email = 1
        self.system_syntax = {}
        time_format = "%H:%M:%S"
        # 将时间字符串解析为datetime对象
        time_obj = datetime.datetime.strptime(time_str, time_format)
        self.system_syntax[time_str] = "cd %s && source ./%s" % (crontab_dir, "array_alpha_gru_encoder_realtime.yml")
        self.time_list = self.system_syntax.keys()
        self.check_run()
        print(self.system_syntax)
