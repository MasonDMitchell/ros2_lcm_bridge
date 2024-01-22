# ros2_lcm_bridge

The main function of this ROS2 Humble package is to serve as an intermediary between an LCM channel and a ROS2 topic. To achieve this, two types of nodes are offered. An lcm_publisher and an lcm_subscriber. The function of both of these nodes is intentionally fairly simple, to allow for maximum flexibility in practice.

# lcm_publisher
This node has one feature with two primary functions, a ROS2 subscriber which will subscribe to a given ROS2 topic, and an LCM publisher which will publish each ROS2 message to a given LCM channel. Together these functions allow for translation of a message from some ROS2 topic, to an LCM channel.

# lcm_listener
Similarly to the publisher, this node has two main processes but they are inverted in comparison. There is an LCM listener which will listen to a given LCM channel, and a ROS2 publisher that will publish each LCM message to a given ROS2 topic.

# How do we do this translation?
There are a few tools behind the scenes that allow for the translation, and they have some quirks. First and foremost, desired messages from LCM to ROS2 (and vice versa) must have the same information contained within each of them. This is ensured by a message generator that is run when the package is built that translates all given LCM messages to identical-in-content (i.e. variable names and types) ROS2 messages. These are the only ROS2 messages that are supported by the package. This means that a severe limitation of this package in its current state is that it can not translate ROS2 messages that are not automatically generated from one of the user-created LCM message types inside the package.

This automatic ROS2 message generation is executed when you build your package, i.e. run `colcon build`. Because of this, most of the automation is in the CMake code and has a couple not fully supported methods for sourcing so be wary with specialized implementations.

# Package dependencies
Ubuntu 22.04 (has not been tested on other flavors of Linux or versions of Ubuntu, or Mac, or Windows)
ROS2 Humble		Install link: https://docs.ros.org/en/humble/Installation.html
LCM		            Install link: http://lcm-proj.github.io/lcm/content/build-instructions.html

# How to use this package
Clone this repository into your `src` directory inside your ROS2 repository.

There must be an `.lcm` file in the `lcm_messages` directory before building the package to prevent a build crash. You can follow this structure to build an LCM file: http://lcm-proj.github.io/lcm/content/tutorial-lcmgen.html. However due to some custom ReGeX to translate from LCM to ROS, please make these LCM data types in as standard a format as possible, and do not add a package in your message definition. PascalCase or camelCase is verified to work for LCM data type names, but any LCM data type name must also be an eligible ROS2 message name. Please do not use LCM-standard snake_case for your data type name. Please check the example message in the repository for reference. NOTE: Do not run lcm-gen after creating your `.lcm` file the message generator will do this for you when building the package.

(Re)build your repository from your ros2_ws directory
`cd ../..`
`colcon build`

There should now be a `.msg` file inside the `msg` repository with the same content that each LCM message has in `lcm_messages`, but translated for ROS. If you have issues building the package, attempt building clean by removing your ‘build’ and ‘install’ directories inside your repository, and then run `colcon build` again. When you delete any `.lcm` files, it is also probably a good idea to build clean.

You can now run either node using the following commands:

`ros2 run ros2_lcm_bridge lcm_listener.py *lcm channel name* *lcm file name*` or
`ros2 run ros2_lcm_bridge lcm_publisher.py *ros topic name* *lcm channel name* *lcm file name*`

with a user-filled `channel name`, `lcm file name`, and `ros topic name` where applicable. NOTE: These -must- be run inside the src directory inside the package. Otherwise there are dependency failures. 
