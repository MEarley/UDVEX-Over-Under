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
AUTOMINVOLTAGE = 6
EXPONENTIALCONSTANT = 21.71472409516259138255644594583
ROTATIONALOFFSET = 7.5
KP = 0.01
LR_KP = 0.05
SHIFT_TURN_SPEED_RATIO = 0.50
TURN_SPEED_RATIO = 0.75
SLOWED_INTAKE_SPEED = 100
TIMEOUT_TIME = 2
CONTROLLER_DISPLAY_INTERVAL = 10000


class mode():
    TANK = 1
    ARCADE = 2
    DUAL_STICK = 3
    EXPERIMENTAL = 4


# Definitions 
# The Brain
brain = Brain()

# The Controller
controller = Controller()

# Limit Switch
switch = Limit(brain.three_wire_port.a)

# Bumper
bumper = Bumper(brain.three_wire_port.b)

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

global firingMode
firingMode = True

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
#left_motor_3 = Motor(Ports.PORT6, BLUE_MOTOR, True)
#left_motor_4 = Motor(Ports.PORT8, BLUE_MOTOR, True)
left_motor_group = MotorGroup(left_motor_1,left_motor_2)

#Right Motors
right_motor_1 = Motor(Ports.PORT3, BLUE_MOTOR, False)
right_motor_2 = Motor(Ports.PORT5, BLUE_MOTOR, False)
#right_motor_3 = Motor(Ports.PORT7, BLUE_MOTOR, False)
#right_motor_4 = Motor(Ports.PORT9, BLUE_MOTOR, False)
right_motor_group = MotorGroup(right_motor_1,right_motor_2)

# Catapult Motor
catapult_motor_FW = Motor(Ports.PORT8,RED_MOTOR,False)
catapult_motor_BW = Motor(Ports.PORT9,RED_MOTOR,True)
catapult_motor_FW.set_max_torque(100,PERCENT)
catapult_motor_BW.set_max_torque(100,PERCENT)
catapult_motor = MotorGroup(catapult_motor_FW,catapult_motor_BW)

# Intake motor
intake_motor = Motor(Ports.PORT10, BLUE_MOTOR, True)
intake_motor.set_velocity(100,PERCENT)
intake_motor.set_max_torque(100,PERCENT)

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
    #left_motor_3.spin(direction,voltage,VOLT)
    #left_motor_4.spin(direction,voltage,VOLT)
    return

def right_spin_volt(direction,voltage):
    right_motor_1.spin(direction,voltage,VOLT)
    right_motor_2.spin(direction,voltage,VOLT)
    #right_motor_3.spin(direction,voltage,VOLT)
    #right_motor_4.spin(direction,voltage,VOLT)
    return

def autoDriveForward(tiles, launchCatapult: bool):

    t = int(TILEREVOLUTIONS * tiles)
    avg_pos = 0
    left_motor_group.set_position(value=0.0,units=DEGREES)
    right_motor_group.set_position(value=0.0,units=DEGREES)
    start_time = brain.timer.time(SECONDS)

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
            
        if(launchCatapult == True and (avg_pos < t + 100 and avg_pos > t - 100)):
            catapult_motor.spin(FORWARD)

        left_spin_volt(FORWARD,left_drive)
        right_spin_volt(FORWARD,right_drive)
        elapsed_time = brain.timer.time(SECONDS) - start_time
        if(elapsed_time > TIMEOUT_TIME):
            break # Fail safe (shutdown if robot gets stuck and can't move)

    left_motor_group.stop(BRAKE)
    right_motor_group.stop(BRAKE)

    if(launchCatapult == True):
        wait(500, MSEC)

        # Lower catapult
        while(not switch.pressing()):
            catapult_motor.spin(FORWARD)
        catapult_motor.stop()

    #field[start[0]][start[1]] = 'O'
    #start[1] -= 1
    #field[start[0]][start[1]] = 'S'
    return

# Rotates robot using P-Control (<0 = counter-clockwise, >0 = clockwise)
def rotateBy(t: int):

    isNegative = bool(t < 0) 
    t = abs(t)
    avg_pos = 0
    left_motor_group.set_position(value=0.0,units=DEGREES)
    right_motor_group.set_position(value=0.0,units=DEGREES)
    start_time = brain.timer.time(SECONDS)

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
            

        # Negative = counter-clockwise
        # Positive = clockwise
        if(isNegative == True):
            left_spin_volt(REVERSE,left_drive)
            right_spin_volt(FORWARD,right_drive)
        else:
            left_spin_volt(FORWARD,left_drive)
            right_spin_volt(REVERSE,right_drive)

        if(brain.timer.time(SECONDS) - start_time > TIMEOUT_TIME):
            break # Fail safe (shutdown if robot gets stuck and can't move)
            

    left_motor_group.stop(BRAKE)
    right_motor_group.stop(BRAKE)


    return

def skidsteer_auto(tiles, direction: bool):
    t = int(TILEREVOLUTIONS * tiles) # Target position
    avg_pos = 0
    left_motor_group.set_position(value=0.0,units=DEGREES)   # Reset motor position
    right_motor_group.set_position(value=0.0,units=DEGREES)
    start_time = brain.timer.time(SECONDS)
    if(direction == True):
        while(not(avg_pos < t + 1 and avg_pos > t - 1)):
            left_pos = left_motor_group.position() * 0.7
            right_pos = right_motor_group.position() * 1.22
            avg_pos = (((left_pos / 0.7)  + (right_pos / 1.22) ) / 2)    # Average motor position
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
            if((left_pos / 0.7)  > (right_pos / 1.22) ):
                left_drive += (right_pos - left_pos ) * LR_KP
            else:
                right_drive += (left_pos - right_pos ) * LR_KP

            left_spin_volt(FORWARD,left_drive)
            right_spin_volt(FORWARD,right_drive)

            elapsed_time = brain.timer.time(SECONDS) - start_time # Autom time out
            if(elapsed_time > TIMEOUT_TIME):
                break # Fail safe (shutdown if robot gets stuck and can't move)
    else:
        while(not(avg_pos < t + 1 and avg_pos > t - 1)):
            left_pos = left_motor_group.position() * 1.22
            right_pos = right_motor_group.position() * 0.7
            avg_pos = (((left_pos / 1.22)  + (right_pos / 0.7) ) / 2)    # Average motor position
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
            if((left_pos / 1.22)  > (right_pos / 0.7) ):
                left_drive += (right_pos - left_pos ) * LR_KP
            else:
                right_drive += (left_pos - right_pos ) * LR_KP

            left_spin_volt(FORWARD,left_drive)
            right_spin_volt(FORWARD,right_drive)

            elapsed_time = brain.timer.time(SECONDS) - start_time # Autom time out
            if(elapsed_time > TIMEOUT_TIME):
                break # Fail safe (shutdown if robot gets stuck and can't move)

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
        autoDriveForward(x-robotPosition[0], False)
    else:   
        autoDriveForward(robotPosition[0]-x, False)
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
        autoDriveForward(y-robotPosition[1], False)
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
        autoDriveForward(robotPosition[1]-y, False)
    robotPosition[1] = y
    

    return

def automControllerDisplay():
    controller.screen.clear_screen()
    for w in range(6):
        controller.screen.set_cursor(w,0)
        for h in range(6):
            controller.screen.print(field[w][h])
    return

def toggleIntake(toggle: bool,direct,percent):
    if(toggle == True):
        intake_motor.spin(direct,percent,PERCENT)
    else:
        intake_motor.stop()


def pre_autonomous():
    brain.screen.clear_screen()
    brain.screen.print("Pre-auton Mode")
    wait(1, SECONDS)    
    

def skills_auto():
    auto_start_time = brain.timer.time(SECONDS)

    # Release intake
    toggleIntake(True, FORWARD,100)
    wait(2.5, SECONDS)
    toggleIntake(False, FORWARD,100)
    

    # Go to corner turn
    autoDriveForward(0.3, False)
    rotateBy(int(ROTATE90 / -2))
    wait(120, MSEC)
    autoDriveForward(0.4, False)
    wait(120, MSEC)

    # Rotate towards corner
    rotateBy(int(-ROTATE90))
    autoDriveForward(-0.3, False) # back up to avoid climb pole
    
    # Rotate catapult towards the goal
    rotateBy(int(ROTATE90 / 2)) 
    wait(250, MSEC)

    # Launch Preload
    while(switch.pressing()):
        catapult_motor.spin(FORWARD)
    catapult_motor.stop()

    # Rotate catapult back to original position
    rotateBy(int(-ROTATE90 / 2))

    autoDriveForward(-0.05, False)
    
    while(brain.timer.time(SECONDS) - auto_start_time  <= 61): # Launch for the duration of the match
        # Lower catapult
        while(not switch.pressing()):
            catapult_motor.spin(FORWARD)
        catapult_motor.stop()

        # Grab Triball
        toggleIntake(True, REVERSE, SLOWED_INTAKE_SPEED) 
        autoDriveForward(0.85, False)
        wait(125,MSEC)

        # Back up
        autoDriveForward(-0.85, False)
        toggleIntake(False, REVERSE,SLOWED_INTAKE_SPEED)

        # Rotate towards goal
        rotateBy(int(ROTATE90 / 2))

        # Fire Triball
        while(switch.pressing()):
            catapult_motor.spin(FORWARD)
        catapult_motor.stop()

        # Rotate towards original position
        rotateBy(int(ROTATE90 / -2))


    return

def match_auto():
    auto_start_time = brain.timer.time(SECONDS)

    # Release intake
    toggleIntake(True, FORWARD,100)
    wait(1.5, SECONDS)
    toggleIntake(False, FORWARD,100)
    

    # Go to corner turn
    autoDriveForward(0.3, False)
    rotateBy(int(ROTATE90 / -2))
    wait(120, MSEC)
    autoDriveForward(0.4, False)
    wait(120, MSEC)

    # Rotate towards corner
    rotateBy(int(-ROTATE90))
    autoDriveForward(-0.3, False) # back up to avoid climb pole
    
    # Rotate catapult towards the goal
    rotateBy(int(ROTATE90 / 2)) 
    wait(250, MSEC)

    # Launch Preload
    while(switch.pressing()):
        catapult_motor.spin(FORWARD)
    catapult_motor.stop()

    # Rotate catapult back to original position
    rotateBy(int(-ROTATE90 / 2))

    # Grab Triball
    toggleIntake(True, REVERSE,SLOWED_INTAKE_SPEED)
    autoDriveForward(0.90, False) 
    wait(250,MSEC)
    autoDriveForward(-0.20, False)
    toggleIntake(False, REVERSE,SLOWED_INTAKE_SPEED)
    autoDriveForward(-0.55, False)
    

    # Release ball
    rotateBy(int(ROTATE90))
    toggleIntake(True,FORWARD,100)
    wait(1, SECONDS)
    toggleIntake(False,FORWARD,100)
    rotateBy(int(-ROTATE90))
    autoDriveForward(-0.05, False)
    
    while(brain.timer.time(SECONDS) - auto_start_time  <= 30): # Launch until the final 15 seconds of the match
        # Lower catapult
        while(not switch.pressing()):
            catapult_motor.spin(FORWARD)
        catapult_motor.stop()

        # Grab Triball
        toggleIntake(True, REVERSE, SLOWED_INTAKE_SPEED) 
        autoDriveForward(0.85, False)
        wait(125,MSEC)

        # Back up
        autoDriveForward(-0.85, False)
        toggleIntake(False, REVERSE,SLOWED_INTAKE_SPEED)

        # Rotate towards goal
        rotateBy(int(ROTATE90 / 2))

        # Fire Triball
        while(switch.pressing()):
            catapult_motor.spin(FORWARD)
        catapult_motor.stop()

        # Rotate towards original position
        rotateBy(int(ROTATE90 / -2))

    """
    # Red triball
    autoDriveForward(0.3, False) # Drive Towards red Triball
    rotateBy(ROTATE90)
    wait(125,MSEC)
    skidsteer_auto(1,True) # Push red triball into goal

    # Straighten Against wall
    autoDriveForward(-0.3, False)
    autoDriveForward(0.2, False)
    rotateBy(ROTATE90)
    autoDriveForward(-0.3, False)

    # Drive to Black Bar
    autoDriveForward(2.5, False)
    autoDriveForward(-0.2,False)

    # Rotate into elevation bar
    rotateBy(int(ROTATE90 / 2))
    """


    
    #Hang bar is in the way
    # Turn around
    rotateBy(ROTATE90 * 2)
    autoDriveForward(-0.3, False) # back up to corner
    rotateBy(ROTATE90)
    wait(125,MSEC)
    skidsteer_auto(-0.80,False)

    # Straighten Against wall
    autoDriveForward(0.08, False)
    rotateBy(int(-ROTATE90) )
    autoDriveForward(-0.3, False)

    # Drive to Black Bar
    autoDriveForward(2.5, False)
    autoDriveForward(-0.2,False)

    # Rotate and drive to elevation bar
    rotateBy(int(ROTATE90 / 2))
    

    """
    # Turn around
    rotateBy(ROTATE90 * 2)
    autoDriveForward(-0.3, False) # back up to corner

    # Turn back towards triball
    rotateBy(int(ROTATE90))
    autoDriveForward(-0.5, False) # back up to triball

    # Turn closer to triball
    rotateBy(int(ROTATE90 / 2))
    autoDriveForward(-0.6, False) # push triball into goal 
    """

    # Lower catapult
    while(not switch.pressing()):
        catapult_motor.spin(FORWARD)
    catapult_motor.stop()
    
    return

def autonomous():
    brain.screen.clear_screen(Color.CYAN)
    brain.screen.print("Autonomous Mode")
    
    """
    controller.screen.clear_screen()
    for w in range(6):
        controller.screen.set_cursor(w,0)
        for h in range(6):
            controller.screen.print(field[w][h])
    """
    
    #skidsteer_auto(-2, False)
    
    SKILLS = False
    if(SKILLS  == True):
        skills_auto()
    else:
        match_auto()
        
    return
    
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

    
    
    """
    #Push Alliance triball to goal
    rotateBy(int(ROTATE90 / -2)) 
    autoDriveForward(-1)
    rotateBy(int(ROTATE90 / 2))
    autoDriveForward(0.5)

    return

    #Push Alliance triball to goal
    autoDriveForward(0.3)
    rotateBy(int(ROTATE90 / -2)) 
    autoDriveForward(1)
    rotateBy(int(ROTATE90 / 2))
    autoDriveForward(0.5)

    #Go to corner
    autoDriveForward(-0.5)
    rotateBy(int(ROTATE90 / 2) + ROTATE90)
    autoDriveForward(0.5)
    rotateBy(ROTATE90)
    toggleIntake(True) 
    autoDriveForward(0.55)

    # Pick up triball
    wait(1, SECONDS)
    autoDriveForward(-0.65)
    wait(2, SECONDS)
    toggleIntake(False)

    # Launch triball
    while(switch.pressing()):
        catapult_motor.spin(FORWARD)

    while(not switch.pressing()):
        catapult_motor.spin(FORWARD)
    catapult_motor.stop()
    
    return
    """
    # Release intake
    toggleIntake(True, FORWARD,50)
    wait(1, SECONDS)
    toggleIntake(False, FORWARD, 75)

    
    # Lower catapult
    while(not switch.pressing()):
        catapult_motor.spin(FORWARD)
    catapult_motor.stop()

    
    # Raise catapult
    while(switch.pressing()):
        catapult_motor.spin(FORWARD)
    catapult_motor.stop()

    

    # Grab corner triball from start
    autoDriveForward(0.3, False)
    rotateBy(int(ROTATE90 / -2))
    wait(250, MSEC)
    autoDriveForward(0.6, False)
    wait(250, MSEC)
    rotateBy(int(-1.1* ROTATE90)) 
    wait(250, MSEC)
    toggleIntake(True, REVERSE) 
    autoDriveForward(0.55, False)
    wait(1, SECONDS)
    autoDriveForward(-1.5, False)
    wait(1, SECONDS)
    toggleIntake(False, REVERSE)

    # Go to goal
    rotateBy(int(ROTATE90 / 2) + int(ROTATE90 * 1.1)) 
    wait(250, MSEC)
    autoDriveForward(0.7, False)
    wait(250, MSEC)
    rotateBy(int(-ROTATE90 * 1.1))
    toggleIntake(True, FORWARD,50)

    # Push into goal
    autoDriveForward(0.8, False)
    wait(0.5, SECONDS)
    autoDriveForward(-0.5, False)
    toggleIntake(False, FORWARD, 75)

    # Turn around and shove into goal
    rotateBy(ROTATE90 * 2)
    wait(250, MSEC)
    autoDriveForward(-0.6, False)
    wait(500, MSEC)
    autoDriveForward(0.3, False)

    
    # Touch Elevation Bar
    autoDriveForward(1.3, False)
    autoDriveForward(-0.3, False)
    rotateBy(ROTATE90)
    autoDriveForward(1.2, False)
    rotateBy(int(-ROTATE90/2))
    autoDriveForward(0.5, False)
    
    # Lower catapult
    while(not switch.pressing()):
        catapult_motor.spin(FORWARD)
    catapult_motor.stop()
    

    return

    #autoDriveForward(1.25)
    #rotateBy(int(ROTATE90 / 1.5) + (ROTATE90 * 2)) 
    #toggleIntake(True) 
    #autoDriveForward(1.15)
    #wait(0.5, SECONDS)
    #autoDriveForward(-1.15)
    #wait(0.5, SECONDS)
    #toggleIntake(False)
    """
    # Launch tri ball 
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
    """


def tank_drive():

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

    # Controls for Up-Down and Left-Right movement
    leftAxis_UpDwn = controller.axis3.position() / 100.0
    leftAxis_LR = controller.axis4.position() / 100.0

    # Calculate exponentional based speed
    ySpeed = leftAxis_UpDwn ** 3
    xSpeed = (leftAxis_LR * TURN_SPEED_RATIO) ** 3

    if(abs(ySpeed) > 0.05 or abs(xSpeed) > 0.05):

        # Set the velocity depending on the axis position
        left_motor_group.set_velocity(ySpeed + xSpeed,PERCENT)
        right_motor_group.set_velocity(ySpeed - xSpeed,PERCENT)

        left_motor_group.spin(FORWARD)
        right_motor_group.spin(FORWARD)
    else:
        left_motor_group.stop(COAST)
        right_motor_group.stop(COAST)

    return

def dual_stick_drive():

    # Controls for Up-Down and Left-Right movement
    leftAxis_UpDwn = controller.axis3.position() / 100.0
    rightAxis_LR = controller.axis1.position() / 100.0

    # Motor speed percentage based on cubed function
    ySpeed = leftAxis_UpDwn ** 3
    xSpeed = (rightAxis_LR * TURN_SPEED_RATIO) ** 3

    if(controller.buttonL2.pressing()):
        xSpeed = (rightAxis_LR * SHIFT_TURN_SPEED_RATIO) ** 3


    if(abs(ySpeed) > 0.05 or abs(xSpeed) > 0.05):

        # Set the velocity depending on the axis position
        left_motor_group.set_velocity((ySpeed + xSpeed) * 100,PERCENT)
        right_motor_group.set_velocity((ySpeed - xSpeed) * 100,PERCENT)

        left_motor_group.spin(FORWARD)
        right_motor_group.spin(FORWARD)
    else:
        left_motor_group.stop(COAST)
        right_motor_group.stop(COAST)
    
    return

def experimental_drive():

    # Controls for Up-Down and Left-Right movement
    leftAxis_UpDwn = controller.axis3.position() / 100
    rightAxis_LR = controller.axis1.position() / 100

    # Motor speed percentage based on cubed function
    ySpeed = leftAxis_UpDwn ** 3
    xSpeed = (rightAxis_LR * TURN_SPEED_RATIO) ** 3

    if(controller.buttonL2.pressing()):
        xSpeed = (rightAxis_LR * SHIFT_TURN_SPEED_RATIO) ** 3


    if(abs(ySpeed) > 0.01 or abs(xSpeed) > 0.01):
        left_motor_group.spin(FORWARD)
        right_motor_group.spin(FORWARD)

        # Set the velocity depending on the axis position
        left_motor_group.set_velocity((ySpeed + xSpeed) * 100,PERCENT)
        right_motor_group.set_velocity((ySpeed - xSpeed) * 100,PERCENT)
    else:
        left_motor_group.stop(COAST)
        right_motor_group.stop(COAST)
    return


def controllerDisplay(ctrl_mode):
    controller.screen.clear_screen()
    controller.screen.set_cursor(1,0)

    # Mode
    if(ctrl_mode == mode.TANK):
        controller.screen.print("Tank Mode")
    elif(ctrl_mode == mode.ARCADE):
        controller.screen.print("Arcade Mode")
    elif(ctrl_mode == mode.DUAL_STICK):
        controller.screen.print("Dual-Stick Mode")
    elif(ctrl_mode == mode.EXPERIMENTAL):
        controller.screen.print("Experimental Mode")

    # Battery Percentage
    controller.screen.set_cursor(1,19)
    batteryPercentage = str(brain.battery.capacity()) + "%"
    controller.screen.print(batteryPercentage)

    # Display temperature
    controller.screen.set_cursor(2,0)
    controller.screen.print("R1: %d C" %(right_motor_1.temperature()))
    controller.screen.set_cursor(2,10)
    controller.screen.print("Ct: %d C" %(catapult_motor.temperature()))
    controller.screen.set_cursor(3,0)
    controller.screen.print("L1: %d C" %(left_motor_1.temperature()))
    
    controller.screen.set_cursor(3, 10)
    if(firingMode == True):
        controller.screen.print("auto")
    else:
        controller.screen.print("manual")

    # Check for Overheating
    if(right_motor_1.temperature() >= 50):
        controller.screen.set_cursor(2,19)
        controller.screen.print("HOT")
    if(left_motor_1.temperature() >= 50):
        controller.screen.set_cursor(3,19)
        controller.screen.print("HOT")
    
    return

def user_control():
    
    Control_Mode = mode.DUAL_STICK
    global firingMode
    count = CONTROLLER_DISPLAY_INTERVAL
    wait(20, MSEC)

    while(True):   

        # Switch between control modes
        if(controller.buttonUp.pressing()): # D-pad Up
            Control_Mode = mode.TANK
            brain.screen.clear_screen(Color.GREEN)
            brain.screen.print("Tank-Drive Control")
            count = CONTROLLER_DISPLAY_INTERVAL
        elif(controller.buttonRight.pressing()): # D-pad Right
            Control_Mode = mode.ARCADE
            brain.screen.clear_screen(Color.BLUE)
            brain.screen.print("Arcade-Drive Control")
            count = CONTROLLER_DISPLAY_INTERVAL
        elif(controller.buttonDown.pressing()): # D-pad Down
            Control_Mode = mode.DUAL_STICK
            brain.screen.clear_screen(Color.PURPLE)
            brain.screen.print("Dual-Stick Drive Control")
            count = CONTROLLER_DISPLAY_INTERVAL
        elif(controller.buttonLeft.pressing()): # D-pad Left
            Control_Mode = mode.EXPERIMENTAL
            brain.screen.clear_screen(Color.ORANGE)
            brain.screen.print("Experimental Control")
            count = CONTROLLER_DISPLAY_INTERVAL
        

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
        
        if(firingMode == True):
            # Automatically wind up catapult. Launch using L1
            L1 = bool(controller.buttonL1.pressing())
            if(switch.pressing() == False or L1 == True):
                catapult_motor.spin(FORWARD)
            elif(L1 == False):
                catapult_motor.stop()
        else:
            # Manual wind and fire mode (Recommended for emergency use)
            if(controller.buttonL1.pressing()):
                catapult_motor.spin(FORWARD)
            else:
                catapult_motor.stop()

        # Switch between Auto-wind and Manual-Wind
        if(controller.buttonB.pressing() and (count % 20 == 0)):
            firingMode = not firingMode
            count = CONTROLLER_DISPLAY_INTERVAL

        # Control Modes: 1 = Manual Tank Drive, 2 = Joystick Drive, 3 = Dual-stick Drive 4 = Experimental
        
        if(Control_Mode == mode.TANK):
            tank_drive()
        elif(Control_Mode == mode.ARCADE):
            arcade_drive()
        elif(Control_Mode == mode.DUAL_STICK):
            dual_stick_drive()
        elif(Control_Mode == mode.EXPERIMENTAL):
            experimental_drive()

        if(bumper.pressing()):
            print("ow")

        if(count >= CONTROLLER_DISPLAY_INTERVAL):
            controllerDisplay(Control_Mode)
            count = 0

        wait(20, MSEC)
        count += 20

# Create Competition Instance
comp = Competition(user_control,autonomous)
pre_autonomous()