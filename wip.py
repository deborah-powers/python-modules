#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from datetime import datetime
"""
champs intéressants de datetime
self.year, self.month, self.day, self.hour, self.minute, self.second
newDay = self.replace (day=4, month= self.month +3)
"""
today = datetime.now()
print (today)
nwday = today.replace (day=3, month=today.month +1)
print (nwday)




