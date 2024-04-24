
import time
import datetime
from .base import AbstractJob
from .base import crontab_dir


def append_jobs(jobs):
    thisHour = int(time.strftime("%H", time.localtime()))
    if ((datetime.datetime.now()).strftime('%Y%m%d') <= '20240222') and thisHour < switch_hour:
        pass
    else:
        jobs.append(deploy())

    # 交易
    jobs.append(get_trade_log())
    jobs.append(get_client_log())


class deploy(AbstractJob):
    def __init__(self, ):
        super(deploy, self).__init__()
        self.job_name = 'deploy'
        self.system_syntax = {}
        self.dependent_job_list = ['s2d_linear', 's2d_gru']
        self.run_daytime = True
        self.max_running_second = 600
        self.send_email = 1
        self.system_syntax = {}
        self.system_syntax['07:45:00'] = "cd %s && source ./%s" % (crontab_dir, "local_deploy.yml")
        comd = 'source /opt/share/Modules/init/bash  && module load anaconda3 && module load /home/fisher_research/Module/fishermodulefile && source /opt/share/Modules/init/bash && cd /home/fisher_research/Task/Stock2Derivative.2.5/maintain &&  python client_monitor.py --config 1'
        self.system_syntax['08:25:00'] = comd
        self.time_list = self.system_syntax.keys()
        self.check_run()
        print(self.system_syntax)


class get_trade_log(AbstractJob):
    def __init__(self):
        super(get_trade_log, self).__init__()
        self.job_name = 'get_trade_log'
        # self.job_name = 'get_trade_log_%s_%s'%( mechine, root_dir.split('/')[-1])
        self.run_daytime = True
        self.dependent_job_list = []
        comd = 'source /opt/share/Modules/init/bash  && module load anaconda3 && module load /home/fisher_research/Module/fishermodulefile && source /opt/share/Modules/init/bash && cd /home/fisher_research/Task/Stock2Derivative.2.5/maintain &&  python monitor.py'
        comd_log = 'source /opt/share/Modules/init/bash  && module load anaconda3 && module load /home/fisher_research/Module/fishermodulefile && source /opt/share/Modules/init/bash && cd /home/fisher_research/Task/Stock2Derivative.2.5/maintain &&  python trading_log.py'
        self.system_syntax = {}
        # self.system_syntax['09:36:00'] = comd
        # self.system_syntax['10:10:00'] = comd
        # self.system_syntax['10:40:00'] = comd
        # self.system_syntax['11:10:00'] = comd
        self.system_syntax['11:40:00'] = comd
        self.system_syntax['12:10:00'] = comd + " --eval 1"
        # self.system_syntax['13:10:00'] = comd
        # self.system_syntax['13:40:00'] = comd
        # self.system_syntax['14:10:00'] = comd
        # self.system_syntax['14:40:00'] = comd
        self.system_syntax['15:10:00'] = comd
        self.system_syntax['15:40:00'] = comd
        self.system_syntax['16:10:00'] = comd
        self.system_syntax['16:40:00'] = comd
        self.system_syntax['17:10:00'] = comd_log
        self.time_list = self.system_syntax.keys()
        self.max_running_second = 3600 * 4
        self.send_email = 1
        self.check_run()


class get_client_log(AbstractJob):
    def __init__(self):
        super(get_client_log, self).__init__()
        self.job_name = 'get_client_log'
        # self.job_name = 'get_trade_log_%s_%s'%( mechine, root_dir.split('/')[-1])
        self.run_daytime = True
        self.dependent_job_list = []
        comd = 'source /opt/share/Modules/init/bash  && module load anaconda3 && module load /home/fisher_research/Module/fishermodulefile && source /opt/share/Modules/init/bash && cd /home/fisher_research/Task/Stock2Derivative.2.5/maintain &&  python client_monitor.py'
        self.system_syntax = {}
        # self.system_syntax['10:10:00'] = comd
        self.system_syntax['11:40:00'] = comd
        # self.system_syntax['14:10:00'] = comd
        self.system_syntax['16:10:00'] = comd
        self.time_list = self.system_syntax.keys()
        self.max_running_second = 3600 * 4
        self.send_email = 1
        self.check_run()
