import abc
import time
import os
import sys
import datetime
import pandas as pd
import numpy as np
import datetime

try:
    import MMEmail
except:
    pass

import sys
sys.path.insert(0, '/home/fisher_research/Data')

from .base import AbstractJob
from .base import crontab_dir, switch_hour


def show(date=None):
    AbstractJob.running_cout = 10
    print(date)
    if date:
        x = after_2000()
        df = x.read_symmary(date)
    else:
        df = run()
    print(df)
    return df


from .blocking import append_jobs as append_jobs_for_blocking
from .marketdata_h5 import append_jobs as append_jobs_for_marketdata_h5
from .s2d import append_jobs as append_jobs_for_s2d
from .s2d_realtime import append_jobs as append_jobs_for_s2d_realtime
from .alpha import append_jobs as append_jobs_for_alpha
from .hft import append_jobs as append_jobs_for_hft
from .alpha_realtime import append_jobs as append_jobs_for_alpha_realtime


def run():
    time_str = time.strftime("%H:%M:%S", time.localtime())
    if (time_str >= "19:15:00") and (time_str <= "19:00:00"):
        print('temp skip')
    else:
        myJobsList = []
        append_jobs_for_blocking(myJobsList)
        append_jobs_for_marketdata_h5(myJobsList)
        append_jobs_for_s2d(myJobsList)
        append_jobs_for_s2d_realtime(myJobsList)
        append_jobs_for_alpha(myJobsList)
        append_jobs_for_hft(myJobsList)
        append_jobs_for_alpha_realtime(myJobsList)
        # 最后生成一个summary文件
        print('===================gen summary===================')
        df = pd.concat([x.get_status() for x in myJobsList], axis=0)
        df = df.reset_index(drop=True)
        myJobsList[0].write_symmary(df)
    print('sleep switch_hour = ', switch_hour)
    return df
