#!/usr/bin python

import rospy
import diagnostic_updater
from std_msgs.msg import String

CAMERA_UI = "/camera_btn"

class CameraDriver:

    def __init__(self):

        rospy.loginfo("initialising Camera")
        self.iter = 1

        self.ui_sub = rospy.Subscriber(CAMERA_UI, String, self.receiveUiInput)

        self.disableCamera = False
        self.initState = True

        self.updater = diagnostic_updater.Updater()
        self.updater.setHardwareID("CAMERA")
        self.updater.add("State", self.sensorCheck)

    def runOnce(self):
        if self.initState:
            self.iter += 1
            if self.iter == 10: self.initState = False

        self.updater.force_update()

    def receiveUiInput(self, msg):
        print(msg.data)
        self.disableCamera = True
        pass


    def sensorCheck(self,stat):

        if self.disableCamera and not self.initState:
            stat.summary(diagnostic_updater.DiagnosticStatus.ERROR, "Lost connection")
            stat.add("Error code", "ER_C1")
            return

        if self.initState:
            if self.iter < 5:
                stat.summary(diagnostic_updater.DiagnosticStatus.WARN, "Initialising")
            else:
                stat.summary(diagnostic_updater.DiagnosticStatus.OK, "Connected")
            return

        stat.summary(diagnostic_updater.DiagnosticStatus.OK, "Connected")
        