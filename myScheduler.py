import time
import schedule
import json


class Scheduler():
    def __init__(self):

        #self.launchSchedule()
        # schedule.every(10).seconds.do(self.schedule_message,msg="hola").tag("title")
        # schedule.clear('title')
        #exec("schedule.every(10).seconds.do(self.reminder1)")
        pass


    def launchSchedule(self):
        self.dayTask= schedule.every(self.mySC.TIME_LAPSE_DAY_MINUTES).minutes.do(self.mySC.take_picture)
        schedule.every().day.at(self.mySC.MORNING).do(self.startDay)
        schedule.every().day.at(self.mySC.NIGHT).do(self.endDay)


    def schedule_task(self):
        pass

"""
# After every 10mins geeks() is called. 
schedule.every(10).minutes.do(geeks)

# After every hour geeks() is called.
schedule.every().hour.do(geeks)

# Every day at 12am or 00:00 time bedtime() is called.
schedule.every().day.at("00:00").do(bedtime)

# After every 5 to 10mins in between run work()
schedule.every(5).to(10).minutes.do(work)

# Every monday good_luck() is called
schedule.every().monday.do(good_luck)

# Every tuesday at 18:00 sudo_placement() is called
schedule.every().tuesday.at("18:00").do(sudo_placement)

"""