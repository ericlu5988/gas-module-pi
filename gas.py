#!/usr/bin/env python3
from mq import *
import RPi.GPIO as GPIO
import sys, buzzer, lcd, time

# define light mapping
GREEN = 27
RED = 17

# define GPIO to LCD mapping
LCD_RS = 26
LCD_E  = 19
LCD_D4 = 13
LCD_D5 = 6
LCD_D6 = 5
LCD_D7 = 16

def init_system():
    # basic setup
    GPIO.setmode(GPIO.BCM) # set the board numbering system to BCM
    # setup LED
    GPIO.setup(GREEN,GPIO.OUT)
    GPIO.setup(RED,GPIO.OUT)
    # setup sound
    buzz = buzzer.Buzzer()
    # setup LCD screen
    display = lcd.LCD_Display(LCD_RS, LCD_E, LCD_D4, LCD_D5, LCD_D6, LCD_D7)
    return buzz, display

def init_gas_module(display):
    # Initialize Gas Module
    print("Press CTRL+C to abort.")
    display.lcd_string(f"Gas Module", 1)
    display.lcd_string(f"Calibrating...", 2)
    mq = MQ();
    GPIO.output(GREEN,GPIO.HIGH)
    return mq

def start_alert(buzz):
    GPIO.output(GREEN,GPIO.LOW)
    GPIO.output(RED,GPIO.HIGH)
    buzz.play(4)

def stop_alert():
    GPIO.output(GREEN,GPIO.HIGH)
    GPIO.output(RED,GPIO.LOW)

def display_console_status(lpg, co, smoke): 
    sys.stdout.write("\r")
    sys.stdout.write("\033[K")
    sys.stdout.write(f"LPG:    {lpg} ppm | CO:    {co} ppm | Smoke:   {smoke} ppm")
    sys.stdout.flush()
 
def display_lcd_status(display, lpg, co, smoke):
    display.lcd_string(f"LPG:{lpg} CO:{co}", 1)
    display.lcd_string(f"Smoke: {smoke}", 2)
    return display

# Main
def main():
    buzz, display = init_system()
    mq = init_gas_module(display)

    try:
        # Start Monitoring
        while True:
            perc = mq.MQPercentage()
            # Alert if over threshold
            if perc["GAS_LPG"] > 50 or perc["SMOKE"] > 100:
                start_alert(buzz)  
            # Else do not alert
            else:
                stop_alert()
            # Display status
            lpg = '{:>4}'.format(round(perc["GAS_LPG"]))
            smoke = '{:>5}'.format(round(perc["CO"]))
            co = '{:>4}'.format(round(perc["SMOKE"]))
            display = display_lcd_status(display, lpg, co, smoke)
            display_console_status(lpg, co, smoke)
            time.sleep(0.1)

    except:
        print("\nAbort by user")
        display.lcd_string(f"", 1)
        display.lcd_string(f"", 2)
        GPIO.cleanup()

if __name__ == "__main__":
    main()
