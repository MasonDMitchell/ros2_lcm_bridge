#Author: Mason Mitchell
#Email: masondm@seas.upenn.edu

import os
import re

#Finds all LCM files inside the given search folder and it's child folders 
#Inputs
#search_folder = String() representing the desired folder to search. If none is given, "/" is chosen and the entire machine is searched.
#Outputs
#lcm_filenames = List() filenames (without the '.lcm' extension) of all the lcm messages found
#lcm_filepaths = List() filepaths of all lcm messages found 
def find_lcm_files(search_folder="/"):

    #Array initializations
    lcm_filenames = []
    lcm_filepaths = []

    #Find all LCM files in given folder
    for root, dirs, files in os.walk(search_folder):
        for file in files:
            if file.endswith(".lcm"):
                lcm_filenames.append(file[:-4])
                lcm_filepaths.append(os.path.join(root,file))

    return lcm_filenames, lcm_filepaths

def get_lcm_struct_name(lcm_message_filepath):
    #Open lcm file and place contents into a string
    open_file = open(lcm_message_filepath,"r")
    lcm_file = open_file.read()

    #Close lcm file after reading
    if not open_file.closed:
        open_file.close()

    #Remove all newlines, tabs, and returns from string
    lcm_file = lcm_file.replace('\n', '').replace('\r', '').replace('\t','')

    #Find the first appearance of "struct" and get the name of the struct for file recognition after lcm_gen.
    struct_occurance = [m.end() for m in re.finditer("struct",lcm_file)]
    struct_name = lcm_file[struct_occurance[0]:(struct_occurance[0]+lcm_file[struct_occurance[0]:].find('{'))].replace(' ','')

    return struct_name

def get_lcm_variables_as_ros(lcm_message_filepath):
    #Open lcm file and place contents into a string
    open_file = open(lcm_message_filepath,"r")
    lcm_file = open_file.read()

    #Close lcm file after reading
    if not open_file.closed:
        open_file.close()

    #Remove all newlines, tabs, and returns from string
    lcm_file = lcm_file.replace('\n', '').replace('\r', '').replace('\t','')
    lcm_types = ['int64_t','int32_t','int16_t','int8_t','float','double','string','boolean','byte']
    ros_types = ['int64','int32','int16','int8','float32','float64','string','bool','byte']    

    ros_variables = []
    #Go through the string and find all variables of each type
    for i in range(len(lcm_types)):
        lcm_type = lcm_types[i]
        ros_type = ros_types[i]
        #Get the end index of each occurance of the lcm_type in the lcm_file
        type_occurance = [m.end() for m in re.finditer(lcm_type,lcm_file)] 
        
        #For each found type occurance, find all characters (except spaces) after the end of the type name, before the next ';' in the string. These should be variable names of that type.
        type_variables = []
        for j in range(len(type_occurance)):
            type_variables.append(lcm_file[type_occurance[j]:(type_occurance[j]+lcm_file[type_occurance[j]:].find(';'))].replace(' ',''))
        
        #How many variables found of a type?
        #print(str(len(type_variables)) + " variables of type: '" + lcm_type + "' found!")

        #Process each variable to add to ros variables list
        for variable in type_variables:
            #True if the variable is a list 
            if(variable[-1] == ']' and variable.rfind('[') != -1):
                #Get the size of the array
                size_begin = variable.rfind('[')+1
                array_size = variable[size_begin:-1]

                #True if the list a set size
                if(array_size.isdigit()):
                    #print("One is a fixed-size list of size:",array_size)
                    ros_variables.append(ros_type+"[" + str(array_size) + "]"+ " " + variable[:size_begin-1])

                #True if the list is dynamic
                else:
                    #print("One is an 'unbounded' list")
                    ros_variables.append(ros_type+"[]"+ " " + variable[:size_begin-1])

            #True if the variable is not a list
            else:
                #print("One is not a list")
                ros_variables.append(ros_type + " " + variable)

    return ros_variables
def generate_ros_message(ros_variables,ros_message_filepath):
    with open(ros_message_filepath, mode='wt', encoding='utf-8') as ros_msg_file:
        ros_msg_file.write('\n'.join(ros_variables))

    if not ros_msg_file.closed:
        ros_msg_file.close()
def read_ros_message(ros_message_filepath):
    open_file = open(ros_message_filepath,"r")
    ros_file = open_file.read()

    #Close lcm file after reading
    if not open_file.closed:
        open_file.close()

    return ros_file.splitlines()

if __name__ == "__main__":
    x,y = find_lcm_files()
