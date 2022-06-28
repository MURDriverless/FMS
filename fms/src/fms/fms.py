#!/usr/bin/env python

import rospy
from diagnostic_msgs.msg import DiagnosticStatus
from std_msgs.msg import Int8, String
from mur_common.msg import status_msg
import subprocess
# from fms.uart import Uart

GPS_TOPIC = "/gps_status"
LIDAR_TOPIC = "/lidar_status"
CAMERA_TOPIC = "/camera_status"

CONTROLS_TOPIC = "/controls_status"
PERCEPTION_TOPIC = "/perception_status"
SLAM_TOPIC = "/slam_status"

PORT = "'/dev/ttyACM0'"
BAUDE_RATE = 9600

class FMS:

    # initalise in WARN state
    system_status = {
        "GPS":1,
        "Camera":1,
        "LiDAR":1,
        "Controls":1,
        "Perception":1,
        "SLAM":1,
    }
    uart = None
    
    def __init__(self):

        # TODO: Add try catch exception for serial connection

        # self.uart = Uart(PORT,BAUDE_RATE)
        rospy.loginfo("serial connection established")
        rospy.init_node('fms')
        rospy.loginfo("fms initialised")
        self.launchSubscribers()

        self.initalised = False

        self.stop_act_pub = rospy.Publisher('/fms_actuation', String, queue_size=10)
        self.fms_pub =  rospy.Publisher('/fms', String, queue_size=10)

        rospy.spin()
    
    def launchSubscribers(self):
        # subscribe to all the sensor status
        rospy.Subscriber(GPS_TOPIC, status_msg, self.performSystemCheck)
        rospy.Subscriber(LIDAR_TOPIC, status_msg, self.performSystemCheck)
        rospy.Subscriber(CAMERA_TOPIC, status_msg, self.performSystemCheck)
        rospy.Subscriber(CONTROLS_TOPIC, status_msg, self.performSystemCheck)
        rospy.Subscriber(PERCEPTION_TOPIC, status_msg, self.performSystemCheck)
        rospy.Subscriber(SLAM_TOPIC, status_msg, self.performSystemCheck)
        rospy.loginfo("launched subscribers")

    def performSystemCheck(self,msg):
        status_name = msg.name
        status_code = msg.status_code

        print(status_name + " " + str(status_code))

        # if error, immediately slam the brakes
        if status_code == DiagnosticStatus.ERROR:
            self.triggerEBS()

        prev_status_code = self.system_status[status_name]

        if prev_status_code != status_code:
            self.system_status[status_name] = status_code
            self.checkRules()

        return

    def checkRules(self):
        # TODO: define subscomponent failure rules
        print("System status changed, performing system check")

        # If all sensors change their state from WARN to OK, send READY to UI
        # to perform handshake
        if list(self.system_status.values()).count(0) == len(self.system_status.values()) and not self.initalised:
            self.fms_pub.publish("INIT")
            self.initalised = True
            print("SYSTEM INITIALISED")
            # Proceed to setup UART, connect to it, initiate handshake
            # RUN SERIAL PUBLISHER
            # roslaunch serial_publisher serial_publisher
            # immediately starts listening for handshake
            subprocess.call(['sh', 'src/fms_demo_scripts/launch_serial.sh'])



        pass 

    def triggerEBS(self):
        # trigger ebs
        
        # TODO: SPAM STOP
        self.stop_act_pub.publish("STOP")

        while(True):
            # self.uart.sendData("EBS1\r")
            print("Triggering EBS")