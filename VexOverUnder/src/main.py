# ----------------------------------------------------------------------------- #
#                                                                               #              
#    Project:        Robotics Team 2 Robot 1                                    #
#    Module:         main.py                                                    #
#    Author:         VEX                                                        #
#    Created:        9/29/2023                                                  #
#    Description:                                                               #
#                                                                               #                                                                          
#                                                                               #
#                                                                               #                                                                          
# ----------------------------------------------------------------------------- #

# Library imports
from vex import *

# Definitions 
# The Brain
brain = Brain()

# The Controller
controller = Controller()

# Axial2 Positioning
#           100
#            |
#   0    ----O----  0
#            |
#           100

# Motors
# Green Motor Cap 18:1 (200 rpm) | Blue Motor Cap 6:1 (600 rpm)
# Left Motors
left_motor_1 = Motor(Ports.PORT2, GearSetting.RATIO_18_1, False)
left_motor_2 = Motor(Ports.PORT4, GearSetting.RATIO_18_1, False)
left_motor_3 = Motor(Ports.PORT6, GearSetting.RATIO_18_1, False)
left_motor_4 = Motor(Ports.PORT8, GearSetting.RATIO_18_1, False)
left_motor_group = MotorGroup(left_motor_1,left_motor_2,left_motor_3,left_motor_4)

#Right Motors
right_motor_1 = Motor(Ports.PORT3, GearSetting.RATIO_18_1, True)
right_motor_2 = Motor(Ports.PORT5, GearSetting.RATIO_18_1, True)
right_motor_3 = Motor(Ports.PORT7, GearSetting.RATIO_18_1, True)
right_motor_4 = Motor(Ports.PORT9, GearSetting.RATIO_18_1, True)
right_motor_group = MotorGroup(right_motor_1,right_motor_2,right_motor_3,right_motor_4)

def pre_autonomous():
    brain.screen.clear_screen()
    brain.screen.print("Pre-auton code")
    wait(1, SECONDS)


def autonomous():
    brain.screen.clear_screen()
    brain.screen.print("Auton code")
    wait(1, SECONDS)


def user_control():
    
    while(True):
        #brain.screen.clear_screen()
        #brain.screen.print("User-control")
        L1 = controller.buttonL1.pressing()

        if(L1 == 1):
            brain.screen.clear_screen(Color.BLUE) 
            brain.screen.print_at("Controller Position: %d" %(controller.axis3.position()),x=100,y=40)
        else:
            brain.screen.clear_screen()
            brain.screen.print_at("Controller Position: %d" %(controller.axis3.position()),x=100,y=40)

        left_speed = controller.axis3.position()
        if(left_speed > 5 or left_speed < -5):
            left_motor_group.set_velocity(left_speed,PERCENT)
            left_motor_group.spin(FORWARD)
        else:
            left_motor_group.stop()


        wait(20, MSEC)

# Create Competition Instance
comp = Competition(user_control,autonomous)
pre_autonomous()
