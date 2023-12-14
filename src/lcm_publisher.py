#Author: Mason Mitchell, J. Diego Caporale
#Email: masondm@seas.upenn.edu

import rclpy
from rclpy.node import Node
import sys
from argparse import ArgumentParser
import lcm
import importlib

sys.path.insert(1, '../include/')
from lcm_to_ros_tools import find_lcm_files, get_lcm_struct_name, get_lcm_variables_as_ros, generate_ros_message, read_ros_message,ros_message_name_to_package

parser = ArgumentParser(
                    prog='LCMPublisher',
                    description='This is a ROS2 node that listens for a specific ROS message, and publishes it as an LCM message.')

parser.add_argument('ros_topic_name',type=str,default='',help="Name of ROS topic which messages should be published as LCM")
parser.add_argument('lcm_channel_name',type=str,help="Name of LCM message type being published")
parser.add_argument('lcm_file_name',type=str,help="Folder to search for LCM file")
parser.add_argument('-n','--ros_node_name',type=str,default='lcm_publisher',help="Name of this ROS node")

args = parser.parse_args()

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

class LCMPublisher(Node):
    def __init__(self):
        super().__init__(args.ros_node_name)
        self.subscription_ = self.create_subscription(ros_class,str(args.ros_topic_name),self.listener_callback,10)

    def listener_callback(self,ros_msg):
        lcm_msg = lcm_class()
        
        for i in range(len(lcm_msg.__slots__)):
            variable_name = lcm_msg.__slots__[i]
            variable_type = lcm_msg.__typenames__[i]
            ros_variable = getattr(ros_msg,variable_name)

            lcm_msg.__setattr__(variable_name,ros_variable)

        lc = lcm.LCM()
        lc.publish(args.lcm_channel_name,lcm_msg.encode())

def main(args):
    
    #Standard ROS node spinup
    rclpy.init()    
    minimal_subscriber = LCMPublisher()

    rclpy.spin(minimal_subscriber)

    # Destroy the node explicitly
    minimal_subscriber.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main(args)
