import math
from src.objs import *

# src -> https://stackoverflow.com/a/14822210

#: Convert bytes into human-readable size
def convertSize(byte):
   if byte == 0:
       return "0B"

   size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
   i = int(math.floor(math.log(byte, 1024)))
   p = math.pow(1024, i)
   s = round(byte / p, 2)
   return "%s %s" % (s, size_name[i])

#: Convert seconds into human-readable time
def convertTime(seconds):
   if seconds == 0:
       return "0 Sec"

   size_name = ("Sec", "Min", "Hrs")
   i = int(math.floor(math.log(seconds, 60)))
   p = math.pow(60, i)
   s = round(seconds / p, 2)
   return "%s %s" % (s, size_name[i])