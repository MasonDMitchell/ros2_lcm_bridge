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
from exlcm import lcm_to_ros

#Import corresponding ROS message type
from lcm_bridge.msg import LCMReceived

#Create arguments for non-default usage of the node
from argparse import ArgumentParser

#Parse Arguments
parser = ArgumentParser(
                    prog='LCMListener',
                    description='This is a ROS2 node that listens for a specific LCM message, and publishes it as a ROS message.')

parser.add_argument('-m','--lcm_file_name',type=str,default='lcm_to_ros',help="Name of LCM message type being published")
parser.add_argument('-f','--lcm_msg_folder',type=str,default='../lcm_messages',help="Folder to search for LCM file")
parser.add_argument('-n','--lcm_node_name',type=str,default='EXAMPLE',help="Name of LCM node to listen for messages")
args = parser.parse_args()
#If a file extension is added to lcm file name, remove it.
if(args.lcm_file_name[-4:]==".lcm"):
    args.lcm_file_name = args.lcm_file_name[:-4]

class LCMListener(Node):
    def __init__(self):
        #Standard ROS node & subscriber initialization
        super().__init__('lcm_listener')
        self.publisher_ = self.create_publisher(LCMReceived,'lcm_receiver',10) 

        timer_period = 0.5 #seconds
        self.timer = self.create_timer(timer_period,self.timer_callback)

    def timer_callback(self):
        #Setting up an LCM connection and listener
        lc = lcm.LCM()
        subscription = lc.subscribe(args.lcm_node_name,self.lcm_handler)
        
        #Spin while listening for a new LCM message
        while True:
            lc.handle()

    #Handle LCM message, and publish a ROS message
    def lcm_handler(self, channel, data):
        lcm_msg = lcm_to_ros.decode(data)
        ros_msg = LCMReceived()

        #This fails if package isn't rebuilt
        for i in range(len(lcm_msg.__slots__)):
            variable_name = lcm_msg.__slots__[i]
            variable_type = lcm_msg.__typenames__[i]
            lcm_variable = getattr(lcm_msg,variable_name)
            
            ros_msg.__setattr__(variable_name,lcm_variable)

        #Publish ROS message
        self.publisher_.publish(ros_msg)
        
def main(args):
    
    #Look in given directory for all lcm files, and return lists
    lcm_file_names, lcm_file_paths = find_lcm_files(search_folder=args.lcm_msg_folder) 

    #TODO Probably try-except this
    #Get file path of lcm file that matches given lcm file name
    lcm_file_path = lcm_file_paths[lcm_file_names.index(args.lcm_file_name)]

    new_ros_message = get_lcm_variables_as_ros(lcm_file_path)
    current_ros_message = read_ros_message("../msg/LCMReceived.msg")
    if(new_ros_message != current_ros_message):
        generate_ros_message(new_ros_message,"../msg/LCMReceived.msg")
        raise ModuleNotFoundError("Current ROS message does not match the given LCM message and the lcm_bridge package needs rebuilt to fully generate the new ROS message. This is expected behaviour if you are using a new LCM message.")
    
    #Standard ROS node spinup
    rclpy.init()

    LCM_Listener = LCMListener()
    rclpy.spin(LCM_Listener)

    #Destroy the node expicitly
    LCM_Listener.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main(args)
