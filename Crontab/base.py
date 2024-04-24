import abc
import time
import os
import sys
import datetime
# from qrcommons.util import LogUtil
import pandas as pd
import numpy as np
import datetime

try:
    import MMEmail
except:
    pass

import sys
sys.path.insert(0, '/home/fisher_research/Data')
try:
    from data_base import switch_hour
except:
    switch_hour = 18

crontab_dir = '/home/fisher_research/Data/source/submitter/crontab'


class AbstractJob(abc.ABC):
    """
    特征读写抽象接口
    """
    running_cout = 0

    def __init__(self):
        self.dependent_job_list = []
        self.time_list = []
        self.system_syntax = ''
        self.job_name = 'base'
        self.describe = 'unknown'
        # 21点之后算第二天
        self.run_daytime = False
        thisHour = int(time.strftime("%H", time.localtime()))
        if thisHour >= switch_hour:
            self.today_str = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime('%Y%m%d')
        else:
            self.today_str = time.strftime("%Y%m%d", time.localtime())

        self.time_str = time.strftime("%H:%M:%S", time.localtime())
        self.log_root_dir = '/home/fisher_research/Task/CrontabLog'
        self.job_time = ''
        self.max_running_second = 3600
        self.send_email = False
        self.comment = "None"

    def get_log_path(self, job=None, time=None, aType=None):
        if job is None:
            return os.path.join(self.log_root_dir, self.today_str)
        else:
            if time is None:
                return os.path.join(self.log_root_dir, self.today_str, job)
            else:
                return os.path.join(self.log_root_dir, self.today_str, job, aType + '_' + time)

    def bool_has_done(self, time):
        myCheckFile = self.get_log_path(self.job_name, time, 'log')
        if os.path.exists(myCheckFile):
            return True
        return False

    def bool_is_start(self, time):
        myCheckFile = self.get_log_path(self.job_name, time, 'start')
        if os.path.exists(myCheckFile):
            # 检查是否运行超时
            x = pd.read_csv(myCheckFile, header=None)
            max_second = x.iloc[:, 2].values[-1]
            x = x.iloc[:, 0].values[-1]
            x = x.split(':')
            y = self.time_str.split(':')
            diff = 3600 * (int(y[0]) - int(x[0])) + 60 * (int(y[1]) - int(x[1])) + 1 * (int(y[2]) - int(x[2]))
            if diff > max_second:
                print('!!!!!!!!!!!! running to long', diff, '>', max_second, y, x)
                myEmailCheckFile = self.get_log_path(self.job_name, time, 'email')
                # 发送邮件提醒
                if (self.send_email) & (not os.path.exists(myEmailCheckFile)):
                    # MMEmail.SelfEmail('INFO', 'MMCrontab' + ' running to long ' + self.job_name)
                    pd.DataFrame({1: ['MMEmail'], 2: [str(self.time_str)], }).to_csv(myEmailCheckFile, index=False, header=False, mode='a')
                else:
                    print(self.job_name, 'skip send email')

            else:
                pass

            return True
        return False

    def need_run_by_time(self):
        if ((self.run_daytime) & (time.strftime("%Y%m%d", time.localtime()) < self.today_str)):
            return False
        else:
            done_count = 0
            for this_time in self.time_list:
                if (self.time_str >= this_time) | ((not self.run_daytime) & (time.strftime("%Y%m%d", time.localtime()) == self.today_str)):
                    if self.bool_has_done(this_time):
                        done_count += 1
                        print(self.job_name, 'has done', self.job_name, this_time)
                    elif self.bool_is_start(this_time):
                        print(self.job_name, 'is_start', self.job_name, this_time)
                        # 注释掉这一行，就能够并行提交任务了！
                        # return False
                    else:
                        self.job_time = this_time
                        print(self.job_name, 'true', self.job_name, this_time)
                        return True
            if done_count == len(self.time_list):
                pass
                myAllDoneFile = self.get_log_path(self.job_name, list(self.time_list)[0], "alldone")
                if not os.path.exists(myAllDoneFile):
                    pd.DataFrame({1: [str('')], 2: [str('')], 3: [str('')]}).to_csv(myAllDoneFile, index=False, header=False, mode='a')

        return False

    def need_run_by_dependent(self):
        for job in self.dependent_job_list:
            myCheckFile = self.get_log_path(job)
            if os.path.exists(myCheckFile):
                myDoneFile = [x for x in os.listdir(myCheckFile) if 'alldone' == x[:7]]
                if len(myDoneFile) > 0:
                    pass
                else:
                    return False
            else:
                return False
        return True

    def check_well_done(self, job_time):
        cout_file = self.get_log_path(self.job_name, job_time, 'cout')
        myStr = 'tail -n 2 ' + cout_file
        theReturn = os.popen(myStr)
        theReturn = theReturn.read()
        print('last lines:', theReturn)
        return ('CrontabDone' in theReturn)

    def run(self):
        time_start = time.time()
        time_start_str = time.strftime("%H:%M:%S", time.localtime())
        # 创建根目录
        myRootDir = self.get_log_path(self.job_name)
        os.path.isdir(myRootDir) or os.makedirs(myRootDir)
        # 锁定任务
        myLockFile = self.get_log_path(self.job_name, self.job_time, 'start')
        pd.DataFrame({1: [str(time_start_str)], 2: [str('--:--:--')], 3: [str(self.max_running_second)]}
                     ).to_csv(myLockFile, index=False, header=False, mode='a')
        try:
            # 执行任务
            if type(self.system_syntax) == str:
                thisStr = self.system_syntax
            else:
                thisStr = self.system_syntax[self.job_time]
            myPrintFile = self.get_log_path(self.job_name, self.job_time, 'cout')
            thisStr += ' | tee '
            thisStr += myPrintFile
            print(thisStr)
            os.system(thisStr)
            print(thisStr, 'done')
            time_end = time.time()
            time_end_str = time.strftime("%H:%M:%S", time.localtime())
            # 写日志
            myCheckFile = self.get_log_path(self.job_name, self.job_time, 'log')
            pd.DataFrame({1: [str(time_start_str)], 2: [str(time_end_str)], 3: [str(int(time_end - time_start))]}
                         ).to_csv(myCheckFile, index=False, header=False, mode='a')
            print(self.job_name, 'finish once running. exit.')
        except:
            pass
        finally:
            # 删除锁
            os.system('rm -rf ' + myLockFile)
            AbstractJob.running_cout += 1
        # sys.exit()

        return

    def check_run(self):
        # 判断是否需要启动
        if self.need_run_by_time():
            if self.need_run_by_dependent():
                if AbstractJob.running_cout == 0:
                    self.run()
                else:
                    self.comment = 'max running count'
                    print(self.job_name, 'need not running_cout. ', AbstractJob.running_cout)
            else:
                self.comment = 'wait for dependent job'
                print(self.job_name, 'need not run. dependent_job_list = ', self.dependent_job_list)
        else:
            self.comment = ' '
            # print(self.job_name, 'need not run. ', self.time_list)
        return

    def get_status(self):
        myDir = {}
        myDir['JobName'] = []
        myDir['CrontabTime'] = []
        myDir['UpdateTime'] = []
        myDir['Status'] = []
        myDir['Comment'] = []
        myDir['StartTime'] = []
        myDir['EndTime'] = []
        myDir['CostTime'] = []
        myDir['Command'] = []
        for time in self.time_list:
            if self.bool_has_done(time):
                if self.check_well_done(time):
                    thisStatus = 'Done'
                else:
                    thisStatus = 'End'
                myFile = self.get_log_path(self.job_name, time, 'log')
            elif self.bool_is_start(time):
                thisStatus = 'Start'
                myFile = self.get_log_path(self.job_name, time, 'start')
            else:
                thisStatus = 'Wait'
                myFile = '/home/maming/fdafasdfasdfasdfadf'
            myDir['JobName'].append(self.job_name)
            myDir['CrontabTime'].append(time)
            myDir['UpdateTime'].append(self.time_str)
            myDir['Status'].append(thisStatus)
            myDir['Comment'].append(self.comment)

            myStartTime = 'None'
            myEndTime = 'None'
            myCostTime = 'None'
            if os.path.exists(myFile):
                df = pd.read_csv(myFile, header=None)
                try:
                    myStartTime = df.iloc[:, 0].values[-1]
                except:
                    pass
                try:
                    myEndTime = df.iloc[:, 1].values[-1]
                except:
                    pass
                try:
                    myCostTime = df.iloc[:, 2].values[-1]
                except:
                    pass
            myDir['StartTime'].append(str(myStartTime))
            myDir['EndTime'].append(str(myEndTime))
            myDir['CostTime'].append(str(myCostTime))
            if type(self.system_syntax) == dict:
                myDir['Command'].append('&&'.join(self.system_syntax[time].split('&&')[-1:]))
            else:
                myDir['Command'].append('&&'.join(self.system_syntax.split('&&')[-1:]))
        return pd.DataFrame(myDir)

    def append_crontab(self, df):
        # 检查运维路径中，是否还有未部署的yml
        yml_list = [x for x in os.listdir(crontab_dir) if x.endswith('.yml')]
        yml_list_not_done = []
        print(yml_list)
        for this_yml in yml_list:
            have_done = False
            for comd in df.loc[:, 'Command'].values:
                if this_yml in comd:
                    have_done = True
                    break
            if not have_done:
                yml_list_not_done.append(this_yml)
        # 给df添加列
        for this_yml in yml_list_not_done:
            df.loc[len(df), "Command"] = this_yml
        pass

    def write_symmary(self, df):
        self.append_crontab(df)
        mySummaryPath = os.path.join(self.get_log_path(), 'summary.csv')
        print(mySummaryPath)
        try:
            os.path.isdir(self.get_log_path()) or os.makedirs(self.get_log_path())
            df.to_csv(mySummaryPath, index=False)
        except:
            pass

        return

    def read_symmary(self, date=None):
        mySummaryPath = os.path.join(self.get_log_path(), 'summary.csv')
        if date:
            mySummaryPath = mySummaryPath.replace(self.today_str, date)
        df = pd.read_csv(mySummaryPath)
        self.append_crontab(df)
        return df
