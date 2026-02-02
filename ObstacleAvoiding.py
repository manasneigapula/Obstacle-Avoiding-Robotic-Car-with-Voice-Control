# Final Obstacle Avoiding Car with Voice Control
# version: 4.0 - Robust Exploration & Hardware Stability Fix
# description: Uses move-stop-scan logic with robust servo pulse management.

import RPi.GPIO as GPIO
import time
import speech_recognition as sr
import threading
import sys

# --- Pin Configuration (Physical Board Numbering) ---
ENA, ENB = 12, 16
IN1, IN2, IN3, IN4 = 7, 11, 13, 15
TRIG, ECHO = 29, 31
SERVO_PIN = 33
PIR_PIN = 18

# --- Global State ---
car_running = False
stop_listening = None
mic = None
r = sr.Recognizer()

# --- Hardware Initialization ---
def setup_hardware():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    
    # Motors
    for pin in [ENA, ENB, IN1, IN2, IN3, IN4]:
        GPIO.setup(pin, GPIO.OUT)
    
    # Sensors
    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)
    GPIO.setup(SERVO_PIN, GPIO.OUT)
    GPIO.setup(PIR_PIN, GPIO.IN)

setup_hardware()

# --- PWM Setup ---
pwmA = GPIO.PWM(ENA, 100)
pwmB = GPIO.PWM(ENB, 100)
pwmA.start(0)
pwmB.start(0)

servo = GPIO.PWM(SERVO_PIN, 50)
servo.start(0)

# --- Helper Functions ---

def set_speed(speed):
    pwmA.ChangeDutyCycle(speed)
    pwmB.ChangeDutyCycle(speed)

def motor_control(left_fwd, left_rev, right_fwd, right_rev):
    GPIO.output(IN1, left_fwd)
    GPIO.output(IN2, left_rev)
    GPIO.output(IN3, right_fwd)
    GPIO.output(IN4, right_rev)

def stop():
    motor_control(0, 0, 0, 0)
    set_speed(0)

def set_servo_angle(angle):
    """Uses the exact logic from the working test script."""
    duty = angle / 18 + 2
    GPIO.output(SERVO_PIN, True) # Force pin high before PWM
    servo.ChangeDutyCycle(duty)
    time.sleep(0.6)              # Allow time to turn
    servo.ChangeDutyCycle(0)     # Stop the jitter
    GPIO.output(SERVO_PIN, False)# Release pin
    time.sleep(0.1)

def measure_distance():
    # Ensure pin is low before pulse
    GPIO.output(TRIG, False)
    time.sleep(0.01)
    
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)
    
    pulse_start = time.time()
    pulse_end = time.time()
    
    timeout = time.time() + 0.5
    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()
        if pulse_start > timeout: return 999
        
    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()
        if pulse_end > timeout: return 999
        
    duration = pulse_end - pulse_start
    distance = (duration * 34300) / 2
    return distance

# --- Voice Logic ---
def voice_callback(recognizer, audio):
    global car_running
    try:
        command = recognizer.recognize_google(audio).lower()
        print(f"-> Heard: {command}")
        if any(word in command for word in ["start", "go", "move"]):
            if not car_running:
                print("ACTION: STARTING")
                car_running = True
        elif any(word in command for word in ["stop", "halt", "wait"]):
            if car_running:
                print("ACTION: STOPPING")
                car_running = False
    except:
        pass

# --- Main Program ---
def main():
    global stop_listening, mic, car_running
    
    print("Initializing Microphone...")
    try:
        mic = sr.Microphone()
        with mic as source:
            r.adjust_for_ambient_noise(source, duration=1)
        stop_listening = r.listen_in_background(mic, voice_callback)
        print("Ready! Say 'Start' to begin exploration.")
    except Exception as e:
        print(f"Audio Error: {e}. Check USB Mic connection.")
        # We continue even if mic fails so the robot isn't a brick
    
    # Set initial position
    set_servo_angle(90)

    try:
        while True:
            if not car_running:
                stop()
                time.sleep(0.5)
                continue

            # 1. PIR Safety Check (Highest Priority)
            if GPIO.input(PIR_PIN):
                print("!!! Motion Detected !!!")
                motor_control(0, 1, 0, 1) # Backward
                set_speed(30)
                time.sleep(1.5)
                stop()
                time.sleep(1)
                continue

            # 2. Scanning Mode
            print("--- Scanning ---")
            stop() # Motors must be off for a clean scan
            
            set_servo_angle(180) # Left
            l_dist = measure_distance()
            
            set_servo_angle(90)  # Center
            c_dist = measure_distance()
            
            set_servo_angle(0)   # Right
            r_dist = measure_distance()
            
            print(f"L:{l_dist:.0f} | C:{c_dist:.0f} | R:{r_dist:.0f}")

            # 3. Decision Logic
            CRIT = 20.0 # Distance in cm
            
            if c_dist < CRIT and l_dist < CRIT and r_dist < CRIT:
                print("TRAPPED - Backing out")
                motor_control(0, 1, 0, 1) # Back
                set_speed(30)
                time.sleep(1)
            elif c_dist >= l_dist and c_dist >= r_dist and c_dist > CRIT:
                print("Forward path best.")
                motor_control(1, 0, 1, 0) # Fwd
                set_speed(40)
                time.sleep(0.6)
            elif l_dist > r_dist:
                print("Turning Left.")
                motor_control(0, 1, 1, 0) # Spin Left
                set_speed(40)
                time.sleep(0.4)
            else:
                print("Turning Right.")
                motor_control(1, 0, 0, 1) # Spin Right
                set_speed(40)
                time.sleep(0.4)
            
            stop() # Stop before next scan
            time.sleep(0.1)

    except KeyboardInterrupt:
        print("\nUser stopped program.")
    finally:
        print("Cleaning up hardware...")
        if stop_listening: stop_listening(wait_for_stop=False)
        stop()
        servo.stop()
        pwmA.stop()
        pwmB.stop()
        GPIO.cleanup()

if __name__ == "__main__":
    main()