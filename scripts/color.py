#!/bin/python3
import cv2
import numpy as np

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSHistoryPolicy, QoSProfile
from example_interfaces.msg import Int32MultiArray

class warning_gui(Node):

    def __init__(self):
        super().__init__('warning_gui')
        self.img = np.zeros((360, 640, 3), np.uint8)
        cv2.namedWindow("window",cv2.WINDOW_AUTOSIZE)
        sub_qos = QoSProfile(history=QoSHistoryPolicy.KEEP_LAST, depth=1)

        self.create_subscription(Int32MultiArray,'warning_laser',self.sub_warning,sub_qos)
        
    def sub_warning(self,data:Int32MultiArray):
        self.img = cv2.rectangle(self.img,(0,0),(213,360),self.return_color(data.data[0]),-1)
        self.img = cv2.rectangle(self.img,(213,0),(426,360),self.return_color(data.data[1]),-1)
        self.img = cv2.rectangle(self.img,(426,0),(639,360),self.return_color(data.data[2]),-1)
        cv2.imshow("window", self.img)
        cv2.waitKey(1)

    def return_color(self, level):
        if(level == 0):
            return [0,0,0]
        elif(level == 1):
            return [0,255,0] # green
        elif(level == 2):
            return [0,255,255] # yellow
        elif(level == 3):
            return [0,0,255] # red
        else:
            return [255,255,255]

def ros_main(args = None):
    rclpy.init(args=args)
    ros_class = warning_gui()
    rclpy.spin(ros_class)

    ros_class.destroy_node()
    cv2.destroyAllWindows()
    rclpy.shutdown()

if __name__=='__main__':
    ros_main()