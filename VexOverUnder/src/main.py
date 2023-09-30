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

brain = Brain()
controller = Controller()

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
        brain.screen.clear_screen()
        if(L1 == 1):
            brain.screen.clear_screen(Color.BLUE) 
        wait(1, SECONDS)

# Create Competition Instance
comp = Competition(user_control,autonomous)
pre_autonomous()
