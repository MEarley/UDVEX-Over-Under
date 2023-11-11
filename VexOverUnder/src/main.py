# ----------------------------------------------------------------------------- #
#                                                                               #              
#    Project:        Robotics Team 2 Robot 1                                    #
#    Module:         main.py                                                    #
#    Author:         UD Team 2                                                  #
#    Created:        9/29/2023                                                  #
#    Description:    UnderOver Robot 1 of the VEXU UD Team.                     #
#                                                                               #                                                                          
#                                                                               #
#                                                                               #                                                                          
# ----------------------------------------------------------------------------- #

# Library imports
from vex import *
import math

# Constants
EXPONENTIALCONSTANT = 21.71472409516259138255644594583
ROTATIONALOFFSET = 7.5

# Definitions 
# The Brain
brain = Brain()

# The Controller
controller = Controller()

global RotationPosition
RotationPosition = 0

# Axial1 Positioning
#               0
#               |
#   -100    ----O----    100
#               |
#               0

# Axial2 Positioning
#           100
#            |
#   0    ----O----    0
#            |
#          -100

# Motors
# Green Motor Cap 18:1 (200 rpm) | Blue Motor Cap 6:1 (600 rpm)
GREEN_MOTOR = GearSetting.RATIO_18_1
BLUE_MOTOR = GearSetting.RATIO_6_1
# Left Motors
left_motor_1 = Motor(Ports.PORT2, BLUE_MOTOR, True)
left_motor_2 = Motor(Ports.PORT4, BLUE_MOTOR, True)
left_motor_3 = Motor(Ports.PORT6, BLUE_MOTOR, True)
left_motor_4 = Motor(Ports.PORT8, BLUE_MOTOR, True)
left_motor_group = MotorGroup(left_motor_1,left_motor_2,left_motor_3,left_motor_4)

#Right Motors
right_motor_1 = Motor(Ports.PORT3, BLUE_MOTOR, False)
right_motor_2 = Motor(Ports.PORT5, BLUE_MOTOR, False)
right_motor_3 = Motor(Ports.PORT7, BLUE_MOTOR, False)
right_motor_4 = Motor(Ports.PORT9, BLUE_MOTOR, False)
right_motor_group = MotorGroup(right_motor_1,right_motor_2,right_motor_3,right_motor_4)

# Catapult Motor
catapult_motor = Motor(Ports.PORT1,BLUE_MOTOR,False)
catapult_motor.set_max_torque(100,PERCENT)

def pre_autonomous():
    brain.screen.clear_screen()
    brain.screen.print("Pre-auton Mode")
    wait(1, SECONDS)

def rotateTo(degrees):

    global RotationPosition
    isRotateRight = 1

    # flagging for left or right rotation
    if(RotationPosition < degrees):
        isRotateRight = -1
    
    if(degrees == 0):
        if(RotationPosition > 180):
            isRotateRight = -1
        else:
            isRotateRight = 1
        rotateBy = 360 - RotationPosition * isRotateRight   
    else:
        rotateBy = abs(degrees - RotationPosition)

    left_motor_group.spin_for(direction=FORWARD,rotation=rotateBy * isRotateRight * ROTATIONALOFFSET,units=RotationUnits.DEG,velocity=25,units_v=VelocityUnits.PERCENT,wait=False)
    right_motor_group.spin_for(direction=FORWARD,rotation=rotateBy * isRotateRight * -1 * ROTATIONALOFFSET,units=RotationUnits.DEG,velocity=25,units_v=VelocityUnits.PERCENT,wait=True)

    RotationPosition += rotateBy  * isRotateRight * -1 
    if(RotationPosition > 360):
        RotationPosition -= 360

    print(RotationPosition)
    print(" New RotationPosition")

# Forward is 0 degrees 
def goTo(x, y):
    if(x == 0 and y == 0):
        return
    if(x == 0):

        degrees = 0
        if(y < 0):
            degrees = 180
    elif(y == 0):
        degrees = 90
    else:
        degrees = (180.0 /  math.pi) * (math.atan(y/x))
    
    global RotationPosition
    RotationPosition += degrees
    degrees *= ROTATIONALOFFSET
    if(RotationPosition > 360):
        RotationPosition -= 360

    # If x is negative, robot will rotate towards the left
    if(x < 0 and y < 0):
        degrees -= 180 * ROTATIONALOFFSET
    elif(x < 0):
        degrees *= -1
    
    
    print(RotationPosition)

    # Rotate into the right direction
    left_motor_group.spin_for(direction=FORWARD,rotation=degrees,units=RotationUnits.DEG,velocity=25,units_v=VelocityUnits.PERCENT,wait=False)
    right_motor_group.spin_for(direction=FORWARD,rotation=degrees*-1,units=RotationUnits.DEG,velocity=25,units_v=VelocityUnits.PERCENT,wait=True)

    # Move Forward
    for i in range(int(round(math.sqrt(x**2 + y**2)))):
        left_motor_group.spin_for(direction=FORWARD,rotation=1080,units=RotationUnits.DEG,velocity=50,units_v=VelocityUnits.PERCENT,wait=False)
        right_motor_group.spin_for(direction=FORWARD,rotation=1080,units=RotationUnits.DEG,velocity=50,units_v=VelocityUnits.PERCENT,wait=True)

    

def autonomous():
    brain.screen.clear_screen(Color.CYAN)
    brain.screen.print("Autonomous Mode")


    goTo(0,1)
    rotateTo(90)
    goTo(0,1)
    rotateTo(180)
    goTo(0,1)
    rotateTo(270)
    goTo(0,1)
    rotateTo(0)
    goTo(0,1)
   

    return
    rotateTo(90)
    rotateTo(0)
    rotateTo(180)
    rotateTo(90)
    rotateTo(0)
    rotateTo(180)
    
    rotateTo(270)
    rotateTo(225)

    rotateTo(45)
    rotateTo(135)
    rotateTo(0)
    return
    #Diamond 
    goTo(1,1)
    goTo(1,0)
    goTo(1,0)
    goTo(1,0)

    #Square
    goTo(0,1)
    goTo(1,0)
    goTo(1,0)
    goTo(1,0)

    goTo(-1,2)
    goTo(0,-1)
    goTo(0,1)

    rotateTo(90)
    return

    goTo(-1,-1)
    wait(0.5, SECONDS)
    goTo(0,-1)
    wait(0.5,SECONDS)
    
    
    #Square Test
    goTo(0,1)
    wait(0.5, SECONDS)
    goTo(1,0)
    wait(0.5, SECONDS)
    goTo(1,0)
    wait(0.5, SECONDS)
    goTo(1,0)
    wait(0.5, SECONDS)

    goTo(0,-1)
    wait(1,SECONDS)

    # Reverse
    goTo(-1,0)
    wait(0.5, SECONDS)
    goTo(-1,0)
    wait(0.5, SECONDS)
    goTo(-1,0)
    wait(0.5, SECONDS)
    goTo(0,-1)
    wait(0.5, SECONDS)

    
    wait(0.5, SECONDS)
    #Diamond Test
    goTo(1,-1)
    wait(0.5, SECONDS)
    goTo(1,-1)
    wait(0.5, SECONDS)
    goTo(1,-1)
    wait(0.5, SECONDS)
    goTo(1,-1)
    wait(0.5, SECONDS)

    goTo(-1,-1)

    #left_motor_group.spin_to_position(rotation=180,units=RotationUnits.DEG,velocity=50,wait=False)
    #right_motor_group.spin_to_position(rotation=180,units=RotationUnits.DEG,velocity=50,wait=True)


def user_control():
    Control_Mode = True 
    while(True):
        # Switch between control modes
        if(controller.buttonUp.pressing()):
            Control_Mode = not Control_Mode
            wait(0.5,SECONDS)

        # Control Modes: 1 = Manual Tank Drive, 2 = Joystick control
        if(Control_Mode):
            brain.screen.clear_screen(Color.GREEN)
            brain.screen.print("Tank-Drive Control")
            L1 = controller.buttonL1.pressing()

            # Testing
            #if(L1 == 1):
              #  brain.screen.clear_screen(Color.BLUE) 
             #   brain.screen.print_at("Controller Position: %d" %(int)(50.0 * (math.log(abs(controller.axis3.position())+1,10))),x=100,y=40)
            #else:
                #brain.screen.clear_screen()
                #brain.screen.print_at("Controller Position: %d" %(int)(50.0 * (math.log(abs(controller.axis3.position())+1,10))),x=100,y=40)

            #left_speed = controller.axis3.position()

            # Controlelr joystick positions
            leftAxis_UpDwn = controller.axis3.position()
            rightAxis_UpDwn = controller.axis2.position()

            # Determines whether or not the robot should be going forward to backward
            isNegative_Left = False if leftAxis_UpDwn >= 0 else True
            isNegative_Right = False if rightAxis_UpDwn >= 0 else True

            # Calculate left velocity percentage based on logarithmic scale (0 < leftAxis_UpDwn <= 100)
            #left_speed = (int)(50.0 * (math.log(abs(leftAxis_UpDwn)+1,10)))

            left_speed = (int)(math.exp(abs(leftAxis_UpDwn) / EXPONENTIALCONSTANT))

            if(left_speed > 5):
                left_motor_group.spin(FORWARD)
                if(isNegative_Left):
                    left_speed *= -1
                #left_motor_group.set_velocity(left_speed,units=VoltageUnits)

                # Set the velocity depending on the axis position
                left_motor_group.set_velocity(left_speed,PERCENT)
            else:
                left_motor_group.stop(BRAKE)

            #right_speed = controller.axis2.position()

            # Calculate left velocity percentage based on logarithmic scale (0 < rightAxis_UpDwn <= 100)
            #right_speed = (int)(50.0 * (math.log(abs(rightAxis_UpDwn)+1,10)))

            right_speed = (int)(math.exp(abs(rightAxis_UpDwn) / EXPONENTIALCONSTANT))

            if(right_speed > 5):
                right_motor_group.spin(FORWARD)
                if(isNegative_Right):
                    right_speed *= -1

                # Set the velocity depending on the axis position
                right_motor_group.set_velocity(right_speed,PERCENT)
            else:
                right_motor_group.stop(BRAKE)
        else:
            brain.screen.clear_screen(Color.BLUE)
            brain.screen.print("Arcade-Drive Control")

            # Controls for Up-Down and Left-Right movement
            leftAxis_UpDwn = controller.axis3.position()
            leftAxis_LR = controller.axis4.position()

            # Determines whether or not the robot should be going forward or backward, left or right
            isNegativeY = False if leftAxis_UpDwn >= 0 else True
            isNegativeX = False if leftAxis_LR >= 0 else True

            # Calculate exponentional based speed
            ySpeed = (int)(math.exp(abs(leftAxis_UpDwn) / EXPONENTIALCONSTANT))
            xSpeed = (int)(math.exp(abs(leftAxis_LR) / EXPONENTIALCONSTANT))

            if(ySpeed > 5 or xSpeed > 5):
                left_motor_group.spin(FORWARD)
                right_motor_group.spin(FORWARD)

                if(isNegativeY):
                    ySpeed *= -1
                if(isNegativeX):
                    xSpeed *= -1

                # Set the velocity depending on the axis position
                left_motor_group.set_velocity(ySpeed + xSpeed,PERCENT)
                right_motor_group.set_velocity(ySpeed - xSpeed,PERCENT)
            else:
                left_motor_group.stop(BRAKE)
                right_motor_group.stop(BRAKE)


        wait(20, MSEC)

# Create Competition Instance
comp = Competition(user_control,autonomous)
pre_autonomous()
