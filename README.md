# Robotframework Load Balancer (in-dev)

Warning, this project is in development phase!

This software allows the user to distribute test cases on multiple instances of the system under test.
The provided test runner `robotlb` is inplace replacement for the original test runner `robot`.

## Introduction

The goal of this software is to reduce the test duration of a given project.

When using robotframework in general the system under test is connected to the test runner through various interfaces and there respective libraries.
This interfaces are identified by various names or definitions. For instance a serial interface might be identified by the port number (COM1, COM2, /dev/ttyUSB0). A network interface might be identified by the ip address of the device and son on.

With the approach of the *Robotframework Load Balancer*, the test cases have to be stated in system independent way (system interfaces are not hardcoded in the test case).
This gives to possibility to run run different test cases on different systems.

### Example

The system under test is embedded-iot-device which has the following system interfaces (existing libraries for that interface in braces):

    - REST Interface (RESTinstance)
    - UART Interface (SerialLibrary)

Both libraries are using a parameter during instantiation for locating the system under test.

    Library    SerialLibrary    /dev/ttyUSB0
    Library    REST             https://10.0.0.1

*Robotframework Load Balancer* needs to have this system interface definitions abstracted by a variable.

    Library    SerialLibrary    ${SERIAL_PORT}
    Library    REST             ${REST_IP}
    
With following given configuration (see also usage), *Robotframework Load Balancer* would be capable of distribution all test cases between the pre definied maschines `test-rig-1` and `test-rig-2`. 
    
    maschines:
      test-rig-1:
        variables:
          SERIAL_PORT: COM1
          REST_IP: https://10.0.0.1 
      test-rig-2:
        variables:
          SERIAL_PORT: COM2
          REST_IP: https://10.0.0.2


### Benefits

    1. Save Time
    
## Installation

    pip install robotframework-load-balancer

## Usage

The robot framework load balancer is started from the command line using the `robotlb` script or by executing 
the robot module directly like `python -m robotlb`. This command is a inplace replacement for the existing `robot` test runner

Command to start the balanced test runner: 

    python -m robotlb
    
### Confguration

In addition a configuration files `config.yaml` needs to be placed in the working directory of execution. The `maschines` section holds a list of system under test instances. The key can be choosen by the user and acts as an identifier.
The list of `variables` should be used to identify the system interfaces of the parent `maschines`. The list `blacklist-tags` identifies tags that can not run on this particular system under test.


    maschines:
      test-rig-1:
        blacklist-tags:
        - cant_run_on_rig_1
        - cant_run_anywhere
        variables:
          serial_port: COM1
          dummy_var:  10.1.1.1
    
      test-rig-2:
        blacklist-tags:
        - cant_run_on_rig_2
        - cant_run_anywhere
        variables:
          serial_port: COM2
          dummy_var:  10.1.1.2