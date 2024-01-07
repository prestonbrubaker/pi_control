import RPi.GPIO as GPIO
import time

motorPins = (12, 16, 18, 22)    # Define pins connected to four phases ABCD of stepper motor
CCWStep = (0x01, 0x02, 0x04, 0x08) # Define power supply order for rotating anticlockwise
CWStep = (0x08, 0x04, 0x02, 0x01)  # Define power supply order for rotating clockwise

def setup():
    GPIO.setmode(GPIO.BOARD)       # Use PHYSICAL GPIO Numbering
    for pin in motorPins:
        GPIO.setup(pin, GPIO.OUT)

def moveOnePeriod(direction, ms):
    if ms < 3:     # Ensure the delay is not less than 3ms
        ms = 3

    stepSequence = CCWStep if direction == 1 else CWStep

    for j in range(4):          # Cycle for power supply order
        for i in range(4):      # Assign to each pin
            GPIO.output(motorPins[i], GPIO.HIGH if stepSequence[j] & (1 << i) else GPIO.LOW)
        time.sleep(ms * 0.001)

def moveSteps(direction, ms, steps):
    for _ in range(steps):
        moveOnePeriod(direction, ms)

def motorStop():
    for pin in motorPins:
        GPIO.output(pin, GPIO.LOW)

def loop():
    itC = 0
    while itC < 10000000:
        print("Switch Closed")
        moveSteps(1, 3, 360)
        time.sleep(10)
        moveSteps(0, 3, 360)
        print("Switch Open")
        time.sleep(10)
        print(str(itC))
        itC += 1

def destroy():
    motorStop()
    GPIO.cleanup()             # Release resource

if __name__ == '__main__':
    print('Program is starting...')
    setup()
    try:
        loop()
    except KeyboardInterrupt:  # Press ctrl-c to end the program.
        destroy()
