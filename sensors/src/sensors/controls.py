#!/usr/bin python

import rospy
import diagnostic_updater
from std_msgs.msg import String

CONTROLS_UI = "/controls_btn"

class ControlDriver:

    def __init__(self):

        rospy.loginfo("initialising Controls Pipeline")
        self.iter = 1

        self.ui_sub = rospy.Subscriber(CONTROLS_UI, String, self.receiveUiInput)

        self.disable = False
        self.initState = True

        self.updater = diagnostic_updater.Updater()
        self.updater.setHardwareID("Controls")
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
            stat.summary(diagnostic_updater.DiagnosticStatus.ERROR, "No command received")
            stat.add("Error code", "ER_CTRL1")
            return

        if self.initState:
            if self.iter < 5:
                stat.summary(diagnostic_updater.DiagnosticStatus.WARN, "Initialising")
            else:
                stat.summary(diagnostic_updater.DiagnosticStatus.OK, "Ready to receive commands")
            return

        stat.summary(diagnostic_updater.DiagnosticStatus.OK, "Running")
        