#!/usr/bin/env python

import datetime
import sys
#with open ('access_log.txt') as f:
for line in sys.stdin:
    log_time = line.split('[')[1].split('-0800')[0]
    log_date_obj = datetime.datetime.strptime(log_time, "%d/%b/%Y:%H:%M:%S ")
    convert_time = datetime.datetime.strftime(log_date_obj, "%Y-%m-%d T %H:00:00.000")
    print("%s\t%d" % (convert_time, 1))