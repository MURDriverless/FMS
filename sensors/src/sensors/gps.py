#!/usr/bin/env python

import rospy
import diagnostic_updater
from std_msgs.msg import String

GPS_UI = '/gps_btn'

class GPSDriver:

    updater = None
    gps_precision = 0
    rate = None

    def __init__(self):

        rospy.loginfo("initialising GPS driver...")

        self.ui_sub = rospy.Subscriber(GPS_UI, String, self.receiveUiInput)

        self.disableGPS = False
        self.initState = True

        self.updater = diagnostic_updater.Updater()
        self.updater.setHardwareID("GPS")
        self.updater.add("State", self.accuracyCheck)


    def receiveUiInput(self,msg):
        self.disableGPS = True
        self.updater.force_update()

    def runOnce(self):
        if self.initState:
            self.gps_precision += 1
            if self.gps_precision == 10: self.initState = False

        self.updater.force_update()

    def accuracyCheck(self, stat):
        if self.disableGPS and not self.initState:
            stat.summary(diagnostic_updater.DiagnosticStatus.ERROR, "GPS Malfunctioning")
            stat.add("Sattelites connected", 0)
            return

        if self.initState:
            if self.gps_precision < 3:
                stat.summary(diagnostic_updater.DiagnosticStatus.WARN, "Initialising GPS")
                stat.add("Sattelites connected", 0)
            elif self.gps_precision < 6:
                stat.summary(diagnostic_updater.DiagnosticStatus.WARN, "Connecting to sattelites")
                stat.add("Sattelites connected", self.gps_precision)
            else:
                stat.summary(diagnostic_updater.DiagnosticStatus.OK, "Connected")
                stat.add("Sattelites connected", self.gps_precision)

            return

        stat.summary(diagnostic_updater.DiagnosticStatus.OK, "Connected")
        stat.add("Sattelites connected", self.gps_precision)

        
        
            
    