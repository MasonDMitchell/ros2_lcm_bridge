#Author: Mason Mitchell
#Email: masondm@seas.upenn.edu

#import lcm_to_ros helper
from lcm_to_ros_tools import find_lcm_files, get_lcm_variables_as_ros, generate_ros_message, read_ros_message, get_lcm_struct_name

#Find all LCM files
lcm_file_names, lcm_file_paths = find_lcm_files(search_folder=".")

ros_file_names = []
#For each set of LCM files, generate a ROS message
for i in range(len(lcm_file_paths)):
    lcm_file_path = lcm_file_paths[i]
    lcm_file_name = lcm_file_names[i]
    ros_file_name = get_lcm_struct_name(lcm_file_path)+".msg"
    new_ros_message = get_lcm_variables_as_ros(lcm_file_path)
    generate_ros_message(new_ros_message,ros_file_name)
    print("msg/"+str(ros_file_name),end=" ")

