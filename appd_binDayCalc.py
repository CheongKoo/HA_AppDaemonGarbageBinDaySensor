#-------------------------------------------------------------------------------
# Name:        appd_binDayCalc.py
#
# Purpose:     This AppDaemon module is to show on the front end of Hass.IO what
#              type of bin is needed for the next collection day.
#              I know that there are many examples out there but this is my
#              attempt at learning how to create a sensor and pass it to the
#              front end of Hass.IO.
#
#              I have used a Class for the bins. You can declare as many bins as
#              you like. It will show the collection date for the latest bin.
#
#              Note that this module is developed to work with AppDaemon 3.
#
# Author:      Cheong Koo
# Created:     11/04/2020
#
# Reference:
# 1) https://www.home-assistant.io/docs/ecosystem/appdaemon/api/
# 2) https://community.home-assistant.io/t/make-sensor-from-python-via-appdaemon/41858/6
#
# Note: In your "apps.yaml" file, put the following lines
# binCollectionDay:
#   module: appd_binDayCalc
#   class: binCalc
#
#-------------------------------------------------------------------------------

import appdaemon.plugins.hass.hassapi as hass
import datetime
from time import ctime
from datetime import date
from datetime import timedelta
from time import strftime, localtime


#-------------------------------------------------------------------------------
# Class to store the bin type and find the next cycle based on an entered date
# Bins are stored as a list of this class type
# REF: https://www.geeksforgeeks.org/how-to-create-a-list-of-object-in-python-class/
#-------------------------------------------------------------------------------
class binType:
    #-- Initialise the class
    def __init__(self, binColour, startDate, cycleDays):
        self.binColour = binColour # Colour of bin
        self.startDate = datetime.datetime.strptime(startDate, "%d/%m/%Y").date()
        self.cycleDays = cycleDays # Number of days till next collection
        self.nextDate = date.today() # Default to today's date

    #-- Required for sorting the list
    # https://stackoverflow.com/questions/4010322/sort-a-list-of-class-instances-python
    def __lt__ (self, other):
         return self.nextDate < other.nextDate

    #-- Calculate the next cycle based on the currDate
    # It will populate the nextDate variable
    def findNextCycle(self, currDate):
        if currDate <= self.startDate: # Error condition
            self.nextDate = currDate
            return(currDate)
        newDay = self.startDate
        while True:
            newDay = newDay + timedelta(days=self.cycleDays)
            if newDay >= currDate:
                self.nextDate = newDay
                return(newDay)


#-------------------------------------------------------------------------------
# Main class for AppDaemon. Remember to declare this in apps.yaml.
#-------------------------------------------------------------------------------
class binCalc(hass.Hass):
    garbageBins = []

    #-- Initialise the module
    def initialize(self):
        #-- Configure it to run at midnight
        #-- Modify this if you have more than 2 bins
        self.log("** Starting the bin calculator module **")
        self.setupBins() # Initialise the bins
        runtime = datetime.time(0, 1, 0) # h, m, s - triger 1 min after midnight
        self.run_daily(self.calculateCollectionValues, runtime)
        self.run_in(self.calculateCollectionValues, 5) # Run first time in 5 sec

    #-- Setup the bins
    def setupBins(self):
        #-- Initialise the bins
        self.garbageBins.append(binType("BLUE", "13/01/2020", 14))
        self.garbageBins.append(binType("RED", "06/01/2020", 14))

    #-- Calculate the bin collection days based on today's date
    def calculateCollectionValues(self, kwargs):
        #-- Modify this if you have more than 2 bins
        today = date.today() # Get today's date
        lastUpdated = strftime('%d/%m/%y %H:%M', localtime())
        self.log("-- Starting calculation at " + lastUpdated)

        #-- Calculate the next date
        today = date.today()
        for nBin in self.garbageBins:
            nBin.findNextCycle(today) # Initialise the next date

        #-- Sort bins so that earlies date is first. Note sort function __lt__()
        self.garbageBins.sort()

        #-- Prepare to send out to front end
        # nBinColour = colour of next bin
        # nextCollectionDate = date of next collection
        # daysLeft = days left till next colleciton
        nBinDate = self.garbageBins[0].nextDate
        nBinDays = abs(nBinDate - today) # Days left till bin pickup
        daysLeft = str(nBinDays.days) # Convert it into a string
        nextCollectionDate = nBinDate.strftime("%a %d/%m/%y")
        nBinColour = self.garbageBins[0].binColour
        if daysLeft == "0":
            stateInfo = nBinColour + " bin TODAY! " + nextCollectionDate
        else:
            stateInfo = nBinColour + " bin in " + daysLeft + " days on " + nextCollectionDate
        self.log(stateInfo)
        self.set_state("sensor.next_garbageCollection", state=stateInfo, attributes=\
                       {"binColour": nBinColour, \
                        "nextCollectionDate": nextCollectionDate, \
                        "daysTillNextCollection": daysLeft,
                        "lastUpdated": lastUpdated
                       })




