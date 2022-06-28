#!/usr/bin python

import rospy
import diagnostic_updater
from std_msgs.msg import String

LIDAR_UI = "/lidar_btn"

class LidarDriver:

    def __init__(self):

        rospy.loginfo("initialising LiDAR")
        self.iter = 1

        self.ui_sub = rospy.Subscriber(LIDAR_UI, String, self.receiveUiInput)

        self.disable = False
        self.initState = True

        self.updater = diagnostic_updater.Updater()
        self.updater.setHardwareID("LiDAR")
        self.updater.add("State", self.sensorCheck)

    def runOnce(self):
        if self.initState:
            self.iter += 1
            if self.iter == 10: self.initState = False

        self.updater.force_update()

    def receiveUiInput(self, msg):
        print(msg.data)
        self.disable = True
        pass


    def sensorCheck(self,stat):

        if self.disable and not self.initState:
            stat.summary(diagnostic_updater.DiagnosticStatus.ERROR, "Disconnected")
            stat.add("Error code", "ER_L1")
            return

        if self.initState:
            if self.iter < 5:
                stat.summary(diagnostic_updater.DiagnosticStatus.WARN, "Initialising")
            else:
                stat.summary(diagnostic_updater.DiagnosticStatus.OK, "Connected")
            return

        stat.summary(diagnostic_updater.DiagnosticStatus.OK, "Connected")
        