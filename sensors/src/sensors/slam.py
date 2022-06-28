#!/usr/bin python

import rospy
import diagnostic_updater
from std_msgs.msg import String

SLAM_UI = "/slam_btn"

class SLAMDriver:

    def __init__(self):

        rospy.loginfo("initialising SLAM")
        self.iter = 1

        self.ui_sub = rospy.Subscriber(SLAM_UI, String, self.receiveUiInput)

        self.disableSLAM = False
        self.initState = True

        self.updater = diagnostic_updater.Updater()
        self.updater.setHardwareID("SLAM")
        self.updater.add("State", self.sensorCheck)

    def runOnce(self):
        if self.initState:
            self.iter += 1
            if self.iter == 10: self.initState = False

        self.updater.force_update()

    def receiveUiInput(self, msg):
        print(msg.data)
        self.disableSLAM = True
        pass


    def sensorCheck(self,stat):

        if self.disableSLAM and not self.initState:
            stat.summary(diagnostic_updater.DiagnosticStatus.ERROR, "Failed to localise")
            stat.add("Error code", "ER_S1")
            return

        if self.initState:
            if self.iter < 5:
                stat.summary(diagnostic_updater.DiagnosticStatus.WARN, "Initialising")
            else:
                stat.summary(diagnostic_updater.DiagnosticStatus.OK, "Running")
            return

        stat.summary(diagnostic_updater.DiagnosticStatus.OK, "Running")
        