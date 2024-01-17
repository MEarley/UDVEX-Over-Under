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
from enum import Enum

# Constants
WHEELSIZE = 2.75    # Inches Diameter
TILEDISTANCE = (2 * 12) # 2 feet
TILEREVOLUTIONS = TILEDISTANCE / (math.pi * WHEELSIZE)  # Revolutions per Tile (S / (PI)*Diameter = Revolutions )
EXPONENTIALCONSTANT = 21.71472409516259138255644594583
ROTATIONALOFFSET = 7.5
KP = 0.01

class mode(Enum):
    TANK = 1
    ARCADE = 2
    ARCADE_SPEED = 3
    WINTER = 4


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
#left_motor_4 = Motor(Ports.PORT8, BLUE_MOTOR, True)
left_motor_group = MotorGroup(left_motor_1,left_motor_2,left_motor_3)

#Right Motors
right_motor_1 = Motor(Ports.PORT3, BLUE_MOTOR, False)
right_motor_2 = Motor(Ports.PORT5, BLUE_MOTOR, False)
right_motor_3 = Motor(Ports.PORT7, BLUE_MOTOR, False)
#right_motor_4 = Motor(Ports.PORT9, BLUE_MOTOR, False)
right_motor_group = MotorGroup(right_motor_1,right_motor_2,right_motor_3)

# Catapult Motor
catapult_motor_FW = Motor(Ports.PORT8,BLUE_MOTOR,False)
catapult_motor_BW = Motor(Ports.PORT9,BLUE_MOTOR,True)
catapult_motor_FW.set_max_torque(100,PERCENT)
catapult_motor_BW.set_max_torque(100,PERCENT)
catapult_motor = MotorGroup(catapult_motor_FW,catapult_motor_BW)

# Intake motor
intake_motor = Motor(Ports.PORT10, GREEN_MOTOR, True)
intake_motor.set_velocity(100,PERCENT)

def PIDControl(target, position):
    # Proportional Control
    error = target - position
    return error * KP


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

    # No movement
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
        #left_motor_group.__spin_for_distance()
        left_motor_group.spin_for(direction=FORWARD,rotation=1080,units=RotationUnits.DEG,velocity=50,units_v=VelocityUnits.PERCENT,wait=False)
        right_motor_group.spin_for(direction=FORWARD,rotation=1080,units=RotationUnits.DEG,velocity=50,units_v=VelocityUnits.PERCENT,wait=True)

def left_spin_volt(direction, voltage):
    left_motor_1.spin(direction,voltage,VOLT)
    left_motor_2.spin(direction,voltage,VOLT)
    left_motor_3.spin(direction,voltage,VOLT)
    #left_motor_4.spin(direction,voltage,VOLT)
    return

def right_spin_volt(direction,voltage):
    right_motor_1.spin(direction,voltage,VOLT)
    right_motor_2.spin(direction,voltage,VOLT)
    right_motor_3.spin(direction,voltage,VOLT)
    #right_motor_4.spin(direction,voltage,VOLT)
    return

def pre_autonomous():
    brain.screen.clear_screen()
    brain.screen.print("Pre-auton Mode")
    wait(1, SECONDS)    
    

def autonomous():
    brain.screen.clear_screen(Color.CYAN)
    brain.screen.print("Autonomous Mode")
    t = TILEREVOLUTIONS * 360       # Convert revs to degrees
    pos = 0

    while(not(pos < t + 1 and pos > t - 1)):
        pos = ((left_motor_group.position() + right_motor_group.position()) / 2)    # Average motor position
        drive = PIDControl(t,pos)   #drive based on error between postion and target position
        print("Rotational Position: ",end="")
        print(pos)
        print("Set Drive: ",end="")
        print(drive)
        print("Target Position: ",end="")
        print(t)
        left_spin_volt(FORWARD,drive)
        right_spin_volt(FORWARD,drive)
        

    return
    # Go To Test
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


def tank_drive():
    brain.screen.clear_screen(Color.GREEN)
    brain.screen.print("Tank-Drive Control")

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
        left_motor_group.stop(COAST)

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
        right_motor_group.stop(COAST)    

    return

def arcade_drive():
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
        left_motor_group.stop(COAST)
        right_motor_group.stop(COAST)

    return

def arcade_speed_drive():
    brain.screen.clear_screen(Color.PURPLE)
    brain.screen.print("Arcade-Drive-Speed Control")

    # Controls for Up-Down and Left-Right movement
    leftAxis_UpDwn = controller.axis3.position()
    leftAxis_LR = controller.axis4.position()

    # Determines whether or not the robot should be going forward or backward, left or right
    isNegativeY = False if leftAxis_UpDwn >= 0 else True
    isNegativeX = False if leftAxis_LR >= 0 else True

    # Calculate exponentional based speed
    ySpeed = abs(leftAxis_UpDwn) 
    xSpeed = abs(leftAxis_LR)

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
        left_motor_group.stop(COAST)
        right_motor_group.stop(COAST)

    return

def user_control():
    Control_Mode = mode.TANK
    print(TILEREVOLUTIONS)
    print(TILEDISTANCE)
    while(True):
        # Switch between control modes
        if(controller.buttonUp.pressing()): # D-pad Up
            Control_Mode = mode.TANK
        elif(controller.buttonRight.pressing()): # D-pad Right
            Control_Mode = mode.ARCADE
        elif(controller.buttonDown.pressing()): # D-pad Down
            Control_Mode = mode.ARCADE_SPEED
        elif(controller.buttonLeft.pressing()): # D-pad Left
            Control_Mode = mode.TANK # Extra mode slot
        wait(0.5,SECONDS)

        R1 = bool(controller.buttonR1.pressing())
        R2 = bool(controller.buttonR2.pressing())

        # Intake control
        if(R1 == True and R2 == False):
            print("Forward")
            intake_motor.spin(REVERSE)
        elif ((R2 == True) and (R1 == False)):
            print("Reverse")
            intake_motor.spin(FORWARD)
        else:
            intake_motor.stop()
        

        L1 = bool(controller.buttonL1.pressing)
        # Catapult Controls
        if(L1 == True):
            catapult_motor.spin(FORWARD)
        else:
            catapult_motor.stop()

        # Control Modes: 1 = Manual Tank Drive, 2 = Joystick control, 3 = Joystick control at max speed
        match Control_Mode :
            case mode.TANK :
                tank_drive()
            case mode.ARCADE :
                arcade_drive()
            case mode.ARCADE_SPEED:
                arcade_speed_drive()

        wait(20, MSEC)

# Create Competition Instance
comp = Competition(user_control,autonomous)
pre_autonomous()
