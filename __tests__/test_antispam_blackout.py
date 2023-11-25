#---------------------------------
# Discord Bot
# __tests__/test_antispam_blackout.py
#
# @ start date          25 11 2023
# @ last update         25 11 2023
#---------------------------------

#---------------------------------
# Imports
#---------------------------------
import unittest

import sys
sys.path.append("..")
print(sys.path)

from authorization import is_within_antispam_blackout, DATE_FORMAT

#---------------------------------
# Tests
#---------------------------------
class TestAntiSpamBlackout(unittest.TestCase):
   def should_block_weekday_noon(self):
      date = "24/11/2023,12:00:00".strptime(date, DATE_FORMAT)
      self.assertEqual(is_within_antispam_blackout(date), False)

   def should_allow_weekday_before_8am(self):
      date = "24/11/2023,7:59:10".strptime(date, DATE_FORMAT)
      self.assertEqual(is_within_antispam_blackout(date), True)

   def should_allow_weekday_night(self):
      date = "24/11/2023,22:59:10".strptime(date, DATE_FORMAT)
      self.assertEqual(is_within_antispam_blackout(date), True)

   def should_block_weekday_8am(self):
      date = "24/11/2023,8:00:00".strptime(date, DATE_FORMAT)
      self.assertEqual(is_within_antispam_blackout(date), False)

   def should_block_weekday_before_8pm(self):
      date = "24/11/2023,18:30:13".strptime(date, DATE_FORMAT)
      self.assertEqual(is_within_antispam_blackout(date), False)

   def should_allow_weekend_noon(self):
      date = "25/11/2023,12:00:00".strptime(date, DATE_FORMAT)
      self.assertEqual(is_within_antispam_blackout(date), True)

   def should_allow_weekend_8am(self):
      date = "25/11/2023,8:00:00".strptime(date, DATE_FORMAT)
      self.assertEqual(is_within_antispam_blackout(date), True)
