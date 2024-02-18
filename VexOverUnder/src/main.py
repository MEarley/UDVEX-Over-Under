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
WHEELSIZE = 2.75    # Inches Diameter
TILEDISTANCE = (2 * 12) # 2 feet
TILEREVOLUTIONS = 1400
#TILEDISTANCE / (math.pi * WHEELSIZE)  # Revolutions per Tile (S / (PI)*Diameter = Revolutions )
ROTATE90 = 600
AUTOMAXVOLTAGE = 8
AUTOMINVOLTAGE = 5
EXPONENTIALCONSTANT = 21.71472409516259138255644594583
ROTATIONALOFFSET = 7.5
KP = 0.01
LR_KP = 0.05

class mode():
    TANK = 1
    ARCADE = 2
    ARCADE_SPEED = 3
    EXPERIMENTAL = 4


# Definitions 
# The Brain
brain = Brain()

# The Controller
controller = Controller()

# Limit Switch
switch = Limit(brain.three_wire_port.a)

global RotationPosition
RotationPosition = 180

global field
field = [['X','O','O','O','^','X'],
         ['O','O','O','O','O','O'],
         ['X','O','O','O','O','X'],
         ['X','O','O','O','O','X'],
         ['O','O','O','O','O','O'],
         ['X','O','O','O','O','X']]

global robotPosition
robotPosition = [0,4]

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
RED_MOTOR = GearSetting.RATIO_36_1
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
catapult_motor_FW = Motor(Ports.PORT8,RED_MOTOR,False)
catapult_motor_BW = Motor(Ports.PORT9,RED_MOTOR,True)
catapult_motor_FW.set_max_torque(100,PERCENT)
catapult_motor_BW.set_max_torque(100,PERCENT)
catapult_motor = MotorGroup(catapult_motor_FW,catapult_motor_BW)

# Intake motor
intake_motor = Motor(Ports.PORT10, BLUE_MOTOR, True)
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

def autoDriveForward(tiles):

    t = int(TILEREVOLUTIONS * tiles)
    avg_pos = 0
    left_motor_group.set_position(value=0.0,units=DEGREES)
    right_motor_group.set_position(value=0.0,units=DEGREES)

    while(not(avg_pos < t + 1 and avg_pos > t - 1)):
        left_pos = left_motor_group.position()
        right_pos = right_motor_group.position()
        avg_pos = ((left_pos  + right_pos ) / 2)    # Average motor position
        drive = PIDControl(t,avg_pos)   #drive based on error between postion and target position
        
        # Dont allow drive to go below minimum voltage/speed
        if(drive < AUTOMINVOLTAGE and drive > 0):
            drive = AUTOMINVOLTAGE
        elif(drive > (-1 * AUTOMINVOLTAGE) and drive < 0):
            drive = -1 * AUTOMINVOLTAGE

        # Don't allow drive to go above maximum voltage/speed
        if(drive > AUTOMAXVOLTAGE):
            drive = AUTOMAXVOLTAGE
        elif(drive < (-1 * AUTOMAXVOLTAGE)):
            drive = -1 * AUTOMAXVOLTAGE

        # P-control between left and right motors
        left_drive = drive
        right_drive = drive
        if(left_pos  > right_pos ):
            left_drive += (right_pos - left_pos ) * LR_KP
        else:
            right_drive += (left_pos - right_pos ) * LR_KP
            


        print("Rotational Position: ",end="")
        print(avg_pos)
        print("Set Drive: ",end="")
        print(drive)
        print(left_drive)
        print(right_drive)
        print("Target Position: ",end="")
        print(t)
        print("Left & Right Position: ",end="")
        print(left_pos )
        print(right_pos )
        left_spin_volt(FORWARD,left_drive)
        right_spin_volt(FORWARD,right_drive)
    left_motor_group.stop(BRAKE)
    right_motor_group.stop(BRAKE)
    #field[start[0]][start[1]] = 'O'
    #start[1] -= 1
    #field[start[0]][start[1]] = 'S'
    return

# Rotates robot using P-Control
def rotateBy(t: int):

    isNegative = bool(t < 0) 
    t = abs(t)
    avg_pos = 0
    left_motor_group.set_position(value=0.0,units=DEGREES)
    right_motor_group.set_position(value=0.0,units=DEGREES)

    while(not(avg_pos < t + 1 and avg_pos > t - 1)):
        left_pos = abs(left_motor_group.position())
        right_pos = abs(right_motor_group.position())
        avg_pos = ((left_pos + right_pos) / 2)    # Average motor position
        drive = PIDControl(t,avg_pos)   #drive based on error between postion and target position
        
        # Dont allow drive to go below minimum voltage/speed
        if(drive < AUTOMINVOLTAGE and drive > 0):
            drive = AUTOMINVOLTAGE
        elif(drive > (-1 * AUTOMINVOLTAGE) and drive < 0):
            drive = -1 * AUTOMINVOLTAGE

        # Don't allow drive to go above maximum voltage/speed
        if(drive > AUTOMAXVOLTAGE):
            drive = AUTOMAXVOLTAGE
        elif(drive < (-1 * AUTOMAXVOLTAGE)):
            drive = -1 * AUTOMAXVOLTAGE

        # P-control between left and right motors
        left_drive = drive
        right_drive = drive
        if(left_pos > right_pos):
            left_drive += (right_pos - left_pos) * LR_KP
        else:
            right_drive += (left_pos - right_pos) * LR_KP
            


        print("Rotational Position: ",end="")
        print(avg_pos)
        print("Set Drive: ",end="")
        print(drive)
        print(left_drive)
        print(right_drive)
        print("Target Position: ",end="")
        print(t)
        print("Left & Right Position: ",end="")
        print(left_pos)
        print(right_pos)

        # Negative = counter-clockwise
        # Positive = clockwise
        if(isNegative == True):
            left_spin_volt(REVERSE,left_drive)
            right_spin_volt(FORWARD,right_drive)
        else:
            left_spin_volt(FORWARD,left_drive)
            right_spin_volt(REVERSE,right_drive)
            

    left_motor_group.stop(BRAKE)
    right_motor_group.stop(BRAKE)


    return

# Traverses by x (horizontal) first. then y (vertical) (P-Control)
def goToPosition(x,y):

    # Drive to position x
    global RotationPosition
    if(x > robotPosition[0]):
        # If need to move backwards, face 180 degrees
        if(RotationPosition > 180):
            turns = 0
            while(RotationPosition != 180):
                RotationPosition -= 90
                turns -= 1
            rotateBy(ROTATE90 * turns)
        elif(RotationPosition < 180):
            turns = 0
            while(RotationPosition != 180):
                RotationPosition += 90
                turns += 1
            rotateBy(ROTATE90 * turns)
        autoDriveForward(x-robotPosition[0])
    else:   
        autoDriveForward(robotPosition[0]-x)
    robotPosition[0] = x

    # Drive to position y
    if(y > robotPosition[1]):
        # If need to move right, face 90 degrees
        if(RotationPosition > 90):
            turns = 0
            while(RotationPosition != 90):
                RotationPosition -= 90
                turns -= 1
            rotateBy(ROTATE90 * turns)
        elif(RotationPosition < 90):
            turns = 0
            while(RotationPosition != 90):
                RotationPosition += 90
                turns += 1
            rotateBy(ROTATE90 * turns)
        autoDriveForward(y-robotPosition[1])
    else: 
        # If need to move left, face 270 degrees
        if(RotationPosition > 270):
            turns = 0
            while(RotationPosition != 270):
                RotationPosition -= 90
                turns -= 1
            rotateBy(ROTATE90 * turns)
        elif(RotationPosition < 270):
            turns = 0
            while(RotationPosition != 270):
                RotationPosition += 90
                turns += 1
            rotateBy(ROTATE90 * turns)
        autoDriveForward(robotPosition[1]-y)
    robotPosition[1] = y
    

    return

def automControllerDisplay():
    controller.screen.clear_screen()
    for w in range(6):
        controller.screen.set_cursor(w,0)
        for h in range(6):
            controller.screen.print(field[w][h])
    return

def toggleIntake(toggle: bool):
    if(toggle == True):
        intake_motor.spin(REVERSE)
    else:
        intake_motor.stop()


def pre_autonomous():
    brain.screen.clear_screen()
    brain.screen.print("Pre-auton Mode")
    wait(1, SECONDS)    
    

def autonomous():
    brain.screen.clear_screen(Color.CYAN)
    brain.screen.print("Autonomous Mode")
    
    controller.screen.clear_screen()
    for w in range(6):
        controller.screen.set_cursor(w,0)
        for h in range(6):
            controller.screen.print(field[w][h])
    
    
    
    
    #      0   1   2   3   4   5
    #  0 ['X','O','O','O','O','X']
    #  1 ['O','O','O','O','O','O']
    #  2 ['X','O','O','O','O','X']
    #  3 ['X','O','O','O','O','X']
    #  4 ['O','O','O','O','O','O']
    #  5 ['X','^','O','O','O','X']
    #autoDriveForward(2)
    #rotateBy(ROTATE90)
    #rotateBy(-1 * ROTATE90)
    #autoDriveForward(1)

    while(not switch.pressing()):
        catapult_motor.spin(FORWARD)
    catapult_motor.stop()
  
    autoDriveForward(0.3)
    rotateBy(int(ROTATE90 / -2)) 
    autoDriveForward(0.5)
    rotateBy(int(-1* ROTATE90)) 
    toggleIntake(True) 
    autoDriveForward(0.65)
    wait(1, SECONDS)
    autoDriveForward(-0.65)
    wait(2, SECONDS)
    toggleIntake(False)
    

    #autoDriveForward(1.25)
    #rotateBy(int(ROTATE90 / 1.5) + (ROTATE90 * 2)) 
    #toggleIntake(True) 
    #autoDriveForward(1.15)
    #wait(0.5, SECONDS)
    #autoDriveForward(-1.15)
    #wait(0.5, SECONDS)
    #toggleIntake(False)

    while(switch.pressing()):
        catapult_motor.spin(FORWARD)

    while(not switch.pressing()):
        catapult_motor.spin(FORWARD)
    catapult_motor.stop()


    controller.screen.clear_screen()
    for w in range(6):
        controller.screen.set_cursor(w,0)
        for h in range(6):
            controller.screen.print(field[w][h])

    return

    goToPosition(2,4)
    goToPosition(2,3)
    goToPosition(2,4)
    goToPosition(0,4)

    return 
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
    field[start[0]][start[1]] = 'O'
    start[1] -= 1
    field[start[0]][start[1]] = 'S'

    controller.screen.clear_screen()
    for w in range(5):
        for h in range(5):
            controller.screen.set_cursor(w,h)
            controller.screen.print(field[w][h])


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

def experimental_drive():
    brain.screen.clear_screen(Color.ORANGE)
    brain.screen.print("Experimental Control")

    # Controls for Up-Down and Left-Right movement
    leftAxis_UpDwn = controller.axis3.position()
    rightAxis_LR = controller.axis1.position()

    # Motor speed percentage based on axis
    ySpeed = leftAxis_UpDwn 
    xSpeed = rightAxis_LR

    if(abs(ySpeed) > 5 or abs(xSpeed) > 5):
        left_motor_group.spin(FORWARD)
        right_motor_group.spin(FORWARD)

        # Set the velocity depending on the axis position
        left_motor_group.set_velocity(ySpeed + xSpeed,PERCENT)
        right_motor_group.set_velocity(ySpeed - xSpeed,PERCENT)
    else:
        left_motor_group.stop(COAST)
        right_motor_group.stop(COAST)

    return


def controllerDisplay(ctrl_mode):
    controller.screen.clear_screen()
    controller.screen.set_cursor(1,0)
    if(ctrl_mode == mode.TANK):
        controller.screen.print("Tank Mode")
    elif(ctrl_mode == mode.ARCADE):
        controller.screen.print("Arcade Mode")
    elif(ctrl_mode == mode.ARCADE_SPEED):
        controller.screen.print("Arcade-Speed Mode")
    elif(ctrl_mode == mode.EXPERIMENTAL):
        controller.screen.print("Experimental Mode")

    controller.screen.set_cursor(1,19)
    controller.screen.print(brain.battery.capacity())
    controller.screen.set_cursor(2,0)
    controller.screen.print("R1: %d R2: %d R3: %d" %(right_motor_1.temperature(), right_motor_2.temperature(),right_motor_3.temperature()))
    controller.screen.set_cursor(3,0)
    controller.screen.print("L1: %d L2: %d L3: %d" %(left_motor_1.temperature(), left_motor_2.temperature(),left_motor_3.temperature()))
    
    return


#TODO: (Done) Have the catapult auto-retract after firing, without needing to hold down the button.

#TODO: (Done) Add the ability to turn while moving, without needing to stop and turn in place.

#TODO: (Done) Change the catapult launch button from Y to a different button, ideally X or the left trigger. Currently the most ergonomic position has my thumb on x, and I have to reach for Y.

#TODO: (Done) Make arcade the default drive mode instead of tank.

def user_control():
    Control_Mode = mode.ARCADE
    count = 0
    print(TILEREVOLUTIONS)
    print(TILEDISTANCE)

    while(True):
        count += 20

        # Switch between control modes
        if(controller.buttonUp.pressing()): # D-pad Up
            Control_Mode = mode.TANK
        elif(controller.buttonRight.pressing()): # D-pad Right
            Control_Mode = mode.ARCADE
        elif(controller.buttonDown.pressing()): # D-pad Down
            Control_Mode = mode.ARCADE_SPEED
        elif(controller.buttonLeft.pressing()): # D-pad Left
            Control_Mode = mode.EXPERIMENTAL # Extra mode slot
        

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
        

        # Automatically wind up catapult. Launch using L1
        L1 = bool(controller.buttonL1.pressing())
        if(switch.pressing() == False or L1 == True):
            catapult_motor.spin(FORWARD)
        elif(L1 == False):
            catapult_motor.stop()
        
        #if(switch.pressing() == True and L1 == True):
            #if(switch.pressing() == True):
                #catapult_motor.spin(FORWARD) # loop until switch is released and catapult is fired
            #catapult_motor.stop()
        #controller.buttonY.pressed(launchCatapult,arg=tuple([True]))
    
        if(count == 1000):
            controllerDisplay(Control_Mode)
            count = 0
        
        # Catapult Controls and (allowLaunch or (not switch.pressing()))
        #if((L1 == True and (switch.pressing() == False)) or controller.buttonY.pressing() == True):
            #print(catapult_motor_FW.position() % 360)
            #catapult_motor.spin(FORWARD)
        #else:
            #catapult_motor.stop()

        

        # Control Modes: 1 = Manual Tank Drive, 2 = Joystick control, 3 = Joystick control at max speed
        if(Control_Mode == mode.TANK):
            tank_drive()
        elif(Control_Mode == mode.ARCADE):
            arcade_drive()
        elif(Control_Mode == mode.ARCADE_SPEED):
            arcade_speed_drive()
        elif(Control_Mode == mode.EXPERIMENTAL):
            experimental_drive()
        
        
        #match Control_Mode :
            #case mode.TANK :
                #tank_drive()
            #case mode.ARCADE :
                #arcade_drive()
            #case mode.ARCADE_SPEED:
                #arcade_speed_drive()

        wait(20, MSEC)

# Create Competition Instance
comp = Competition(user_control,autonomous)
pre_autonomous()
