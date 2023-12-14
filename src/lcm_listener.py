#Author: Mason Mitchell, J. Diego Caporale
#Email: masondm@seas.upenn.edu

import rclpy
from rclpy.node import Node
import sys
from argparse import ArgumentParser
import lcm
import importlib

sys.path.insert(1, '../include/')
from lcm_to_ros_tools import find_lcm_files, get_lcm_struct_name, get_lcm_variables_as_ros, generate_ros_message, read_ros_message, ros_message_name_to_package 

parser = ArgumentParser(
                    prog='LCMListener',
                    description='This is a ROS2 node that listens for a specific LCM message, and publishes it as a ROS message.')

parser.add_argument('lcm_channel_name',type=str,help="Name of LCM channel to listen for messages")
parser.add_argument('lcm_file_name',type=str,help="LCM message-description filename (*.lcm)")
parser.add_argument('-r','--ros_topic_name',type=str,default='',help="Name of ros topic to publish messages from")
parser.add_argument('-n','--ros_node_name',type=str,default='lcm_listener',help="Name of this ros node")

args = parser.parse_args()

#If a ros node name is not given, default to lcm channel name
if(args.ros_topic_name==''):
    args.ros_topic_name=args.lcm_channel_name

#If a file extension is added to lcm file name, remove it.
if(args.lcm_file_name[-4:]==".lcm"):
    args.lcm_file_name = args.lcm_file_name[:-4]

#Import LCM & ROS messages dynamically
sys.path.insert(1, '../')
lcm_struct_name = get_lcm_struct_name("../lcm_messages/"+args.lcm_file_name+".lcm")
lcm_class = importlib.import_module("lcm_messages."+lcm_struct_name)
lcm_class = getattr(lcm_class,lcm_struct_name)
ros_class = importlib.import_module("ros2_lcm_bridge.msg."+ros_message_name_to_package(lcm_struct_name))
ros_class = getattr(ros_class,lcm_struct_name)

class LCMListener(Node):
    def __init__(self):
        #Standard ROS node & subscriber initialization
        super().__init__(args.ros_node_name)
        self.publisher_ = self.create_publisher(ros_class,str(args.ros_topic_name),10) 

        timer_period = 0.5 #seconds
        self.timer = self.create_timer(timer_period,self.timer_callback)

    def timer_callback(self):
        #Setting up an LCM connection and listener
        lc = lcm.LCM()
        subscription = lc.subscribe(args.lcm_channel_name,self.lcm_handler)
        
        #Spin while listening for a new LCM message
        while True:
            lc.handle()

    #Handle LCM message, and publish a ROS message
    def lcm_handler(self, channel, data):
        lcm_msg = lcm_class.decode(data)
        ros_msg = ros_class()

        #This fails if package isn't rebuilt
        for i in range(len(lcm_msg.__slots__)):
            variable_name = lcm_msg.__slots__[i]
            variable_type = lcm_msg.__typenames__[i]
            lcm_variable = getattr(lcm_msg,variable_name)
            
            ros_msg.__setattr__(variable_name,lcm_variable)

        #Publish ROS message
        self.publisher_.publish(ros_msg)
        
def main(args):
    
    #Standard ROS node spinup
    rclpy.init()

    LCM_Listener = LCMListener()
    rclpy.spin(LCM_Listener)

    #Destroy the node expicitly
    LCM_Listener.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main(args)
