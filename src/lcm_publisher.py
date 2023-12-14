#Import ros & node class
import rclpy
from rclpy.node import Node

#import lcm_to_ros helper
import sys
sys.path.insert(1, '../include/')
from lcm_to_ros_tools import find_lcm_files, get_lcm_struct_name, get_lcm_variables_as_ros, generate_ros_message, read_ros_message

#Import lcm & lcm message type
import lcm
sys.path.insert(1, '../lcm_messages/')
#TODO Make this import any lcm message name (requires package)
from exlcm import ros_to_lcm

#Import corresponding ROS message type
from ros2_lcm_bridge.msg import LCMSend

#Create arguments for non-default usage of the node
from argparse import ArgumentParser

#Parse Arguments
parser = ArgumentParser(
                    prog='LCMPublisher',
                    description='This is a ROS2 node that listens for a specific ROS message, and publishes it as an LCM message.')

parser.add_argument('-m','--lcm_file_name',type=str,default='ros_to_lcm',help="Name of LCM message type being published")
parser.add_argument('-f','--lcm_msg_folder',type=str,default='../lcm_messages',help="Folder to search for LCM file")
parser.add_argument('-n','--lcm_node_name',type=str,default='EXAMPLE',help="Name of LCM node to send messages")
args = parser.parse_args()

#If a file extension is added to lcm file name, remove it.
if(args.lcm_file_name[-4:]==".lcm"):
    args.lcm_file_name = args.lcm_file_name[:-4]

class LCMPublisher(Node):
    def __init__(self):
        super().__init__('lcm_publisher')
        #Change the name of the node that this is subscribing to
        #TODO Allow custom topic name?
        self.subscription_ = self.create_subscription(LCMSend,'lcm_publish',self.listener_callback,10)

    def listener_callback(self,ros_msg):
        #Send LCM Message
        lcm_msg = ros_to_lcm()
        
        for i in range(len(lcm_msg.__slots__)):
            variable_name = lcm_msg.__slots__[i]
            variable_type = lcm_msg.__typenames__[i]
            ros_variable = getattr(ros_msg,variable_name)

            lcm_msg.__setattr__(variable_name,ros_variable)
            lc = lcm.LCM()
            lc.publish(args.lcm_node_name,lcm_msg.encode())


def main(args):
    #Look in given directory for all lcm files, and return lists
    lcm_file_names, lcm_file_paths = find_lcm_files(search_folder=args.lcm_msg_folder)

    #Get file path of lcm file that matches given lcm file name
    lcm_file_path = lcm_file_paths[lcm_file_names.index(args.lcm_file_name)]

    new_ros_message = get_lcm_variables_as_ros(lcm_file_path)
    try:
        current_ros_message = read_ros_message("../msg/LCMSend.msg")
        if(new_ros_message != current_ros_message):
            generate_ros_message(new_ros_message,"../msg/LCMSend.msg")
            raise ModuleNotFoundError("Current ROS message does not match the given LCM message and the lcm_bridge package needs rebuilt to fully generate the new ROS message. This is expected behaviour if you are using a new LCM message.")
    except:
        generate_ros_message(new_ros_message,"../msg/LCMSend.msg")
        raise ModuleNotFoundError("No corresponding ROS message was found, and the lcm_bridge package needs rebuilt to fully generate the new ROS message. This is expected behaviour if you are using a new LCM message.")


    rclpy.init()    
    minimal_subscriber = LCMPublisher()

    rclpy.spin(minimal_subscriber)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_subscriber.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main(args)
