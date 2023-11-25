#---------------------------------
# Discord Bot
# authorization.py
#
# @ start date          25 11 2023
# @ last update         25 11 2023
#---------------------------------

#---------------------------------
# Imports
#---------------------------------
from typing import Any
from datetime import datetime

DATE_FORMAT = "%d/%m/%Y,%H:%M:%S"

#---------------------------------
# Antispam Authorization
#---------------------------------
antispam_registry = {}

def is_within_antispam_blackout(now: datetime = datetime.now()) -> bool:
   """
   Returns true if the request should be blocked due to time restrictions.
   Not allowed on weekdays, from 8am to 7pm.
   """
   is_weekday = now.weekday() < 5
   is_within_time = now.hour >= 8 and now.hour <= 19

   return is_weekday and is_within_time

def is_antispam_allowed(ctx: Any) -> bool:
   """
   Checks if the user is allowed to perform an "antispam" action.
   Returns true if **allowed**, otherwise returns false.
   """
   timestamp = datetime.now()
   if is_within_antispam_blackout(timestamp):
      return False
   
   # Check if user has already "antispammed" today
   username = ctx.author
   is_first_time = (username not in antispam_registry)

   if not is_first_time:
      last_date = datetime.strptime(antispam_registry[username], DATE_FORMAT)
      
      if timestamp.day == last_date.day:
         return False
   
   antispam_registry[username] = timestamp.strftime(DATE_FORMAT)
   return True