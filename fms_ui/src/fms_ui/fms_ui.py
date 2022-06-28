#!/usr/bin/env python
import time
from Tkinter import StringVar
from Tkinter import Button
import Tkinter as tk
import rospy
from std_msgs.msg import String
import subprocess

SERIAL_TO_UI = "/serial_to_ui"
UI_TO_SERIAL = "/ui_to_serial"
UI_TO_ACTUATOR = "/ui_to_act"


class FMSUI(tk.Tk):

    def __init__(self):

        # initialisation
        tk.Tk.__init__(self)

        # rospy intialisation
        self.gps_pub = rospy.Publisher('gps_btn', String, queue_size=10)
        self.camera_pub = rospy.Publisher('camera_btn', String, queue_size=10)
        self.lidar_pub = rospy.Publisher('lidar_btn', String, queue_size=10)
        self.controls_pub = rospy.Publisher('controls_btn', String, queue_size=10)
        self.perception_pub = rospy.Publisher('perception_btn',String, queue_size=10)
        self.slam_pub = rospy.Publisher('slam_btn',String,queue_size=10)
        self.ui2serial_pub = rospy.Publisher(UI_TO_SERIAL,String,queue_size=10)
        # self.ui2act_pub = rospy.Publisher(UI_TO_ACTUATOR, String, queue_size=10)

        self.roscore = subprocess.Popen('roscore')
        time.sleep(1)

        rospy.init_node('ui', anonymous=True)

        # system params
        self.system_status = StringVar(self)
        self.system_status.set("System status: Off")

        # FRAME
        # self.geometry("500x500")
        self.title('Supervisory Software Demo')

        # ROW 1
        self.system_stat_label = tk.Label(self, textvariable=self.system_status).grid(row = 0, column = 1, sticky = 'w')

        # ROW 2
        # TODO: Create shell script to launch sensors, system analyzers and fms
        
        # QUIT
        self.quitButton = tk.Button(
            self, width=12, text='Quit', bg='tan', command=self.close_app)
        self.quitButton.grid(row=1, column=0, padx=8, pady=8)
        # Start autonomous pipeline
        self.startAutoBtn = tk.Button(
            self, text='Start Autonomous System', command=self.startAuto)
        self.startAutoBtn.grid(row=1, column=1, padx=8, pady=8)
        
        # gps 
        self.gpsBtn = tk.Button(
            self, text='Disable GPS', command=self.disableGPS)
        self.gpsBtn.grid(row=2, column=0, padx=8, pady=8)
        # camera
        self.cameraBtn = tk.Button(
            self, text='Disable Camera', command=self.disableCamera)
        self.cameraBtn.grid(row=2, column=1, padx=8, pady=8)
        # lidar
        self.lidarBtn = tk.Button(
            self, text='Disable Lidar', command=self.disableLiDAR)
        self.lidarBtn.grid(row=3, column=0, padx=8, pady=8)
        # controls
        self.controlsBtn = tk.Button(
            self, text='Disable Controls', command=self.disableControls)
        self.controlsBtn.grid(row=3, column=1, padx=8, pady=8)
        # perception
        self.perceptionBtn = tk.Button(
            self, text='Disable Perception', command=self.disablePerception)
        self.perceptionBtn.grid(row=4, column=0, padx=8, pady=8)
        # slam
        self.slamBtn = tk.Button(
            self, text='Disable Slam', command=self.disableSLAM)
        self.slamBtn.grid(row=4, column=1, padx=8, pady=8)

        # quit sim
        self.slamBtn = tk.Button(
            self, text='Quit Simulation', command=self.quitSim)
        self.slamBtn.grid(row=5, column=1, padx=8, pady=8)
    
     # --------------------------- UI STUFF ----------------------------

    # Hide all buttons
    def hideBtns(self):
        self.cameraBtn.grid_forget()
        self.gpsBtn.grid_forget()
        self.lidarBtn.grid_forget()
        self.controlsBtn.grid_forget()
        self.perceptionBtn.grid_forget()
        self.slamBtn.grid_forget()

    # Disable Camera
    def disableCamera(self):
        self.camera_pub.publish('DISABLE')
        self.cameraBtn["text"] = "disabled"
        print('Disabling Camera')
        pass

    # Disable LiDAR
    def disableLiDAR(self):
        self.lidar_pub.publish('DISABLE')
        self.lidarBtn["text"] = "disabled"
        print('Disabling LiDAR')
        pass

    # Disable GPS
    def disableGPS(self):
        self.gps_pub.publish('DISABLE')
        self.gpsBtn["text"] = "disabled"
        print('Disabling GPS')

    # Disable Controls
    def disableControls(self):
        self.controls_pub.publish('DISABLE')
        self.controlsBtn["text"] = "disabled"
        print('Disabling Controls Pipeline')
        pass

    # Disable Perception
    def disablePerception(self):
        self.perception_pub.publish('DISABLE')
        self.perceptionBtn["text"] = "disabled"
        print('Disabling Perception Pipeline')
        pass
    
    # Disable SLAM
    def disableSLAM(self):
        self.slam_pub.publish('DISABLE')
        self.slamBtn["text"] = "disabled"
        print('Disabling SLAM Pipeline')
        pass

    # Quit simulation
    def quitSim(self):
        # check if vehicle is in driving state
        # TODO: Disable this button otherwise
        if self.system_status.get() == "Driving":
            self.system_status.set("Simulation has finished")
            self.sendToSerial("END\r")
        pass


    # --------------------------- FUNCTIONS ----------------------------

    # Send END to ui
    def sendToSerial(self,msg):
        self.ui2serial_pub.publish(msg)
        print('successfully send to serial')

    # TODO: Subscribe to fms, wait until all systems are initialised
    def launchFMSSubscriber(self):
        rospy.Subscriber("/fms", String, self.listenToFMS)

    def listenToFMS(self,msg):
        print(msg.data)
        if msg.data == "INIT":
            self.system_status.set("System status: Attempting Handshake")
            rospy.Subscriber(SERIAL_TO_UI, String, self.listenToSerial)

    # Listen to serial for handshake acknowledgment
    def listenToSerial(self,msg):
        if msg.data == "WAITING":
            self.system_status.set("System status: Waiting for GO")
        elif msg.data == "GO":
            self.system_status.set("Driving")
        elif msg.data == "EBS1":
            self.system_status.set("Emergency")

    # Braking commands

    # Wait for autonomous pipeline to initalise, fms then launches serial 
    # listener script to intiate handshake 
    # and wait for go signal
    def startAuto(self):
        self.system_status.set("System status: Initialising")
        subprocess.call(['sh', 'src/fms_demo_scripts/fms_demo.sh'])   
        self.launchFMSSubscriber()

    # quite btn for clean up
    def close_app(self):
        self.roscore.terminate()
        self.destroy()
