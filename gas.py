#!/usr/bin/env python3
import RPi.GPIO as GPIO
import mq1, mq2, sys, buzzer, lcd, time

# define threshold
LPG_THRESH = 2000
CO_THRESH = 100
SMOKE_THRESH = 200

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
BUTTON_BACK = 23
BUTTON_NEXT_ITEM = 24
BUTTON_ENTER = 25
option = None
selection = None

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
    # setup buttons
    GPIO.setup(BUTTON_BACK, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(BUTTON_NEXT_ITEM, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(BUTTON_ENTER, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    return buzz, display

def init_gas_module(menu, display):
    display.lcd_string(f"{menu[selection]}", 1)
    display.lcd_string(f"Calibrating...", 2)
    if selection == 0:
        mq = mq2.MQ()
    else:
        mq = mq1.MQ()
    GPIO.output(GREEN,GPIO.HIGH)
    return mq, display

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

def main_menu(display): 
    global selection
    global option
    selection = None
    menu = ["MQ2:LPG,CO,Smoke","MQ1:LPG,CO,Smoke"]
    option = 0

    def button_callback(button):
        global option
        global selection
        if button == BUTTON_ENTER:
            selection = option
        elif button == BUTTON_NEXT_ITEM:
            option = (option + 1) % len(menu)

    display.lcd_string(f"Select Module", 1)    
    display.lcd_string(menu[option], 2)
    GPIO.remove_event_detect(BUTTON_NEXT_ITEM)
    GPIO.remove_event_detect(BUTTON_ENTER)
    GPIO.add_event_detect(BUTTON_NEXT_ITEM,GPIO.RISING,callback=button_callback)
    GPIO.add_event_detect(BUTTON_ENTER,GPIO.RISING,callback=button_callback)
    while selection == None: 
        display.lcd_string(menu[option], 2)    
        time.sleep(0.05)
    return menu, display

def cleanup(display):
    display.lcd_string(f"", 1)
    display.lcd_string(f"", 2)
    GPIO.cleanup()

def main():
    print("Select Gas Module to run using the button and LCD screen")
    print("Button Layout:")
    print("|  Back (Menu)  |  Next Item  |  Enter  |")
    print("Press CTRL+C to abort")
    try:
        while True:
            # initialize buzzer
            buzz, display = init_system()
            # display menu and wait for users to select a module
            menu, display = main_menu(display)
            # start calibration on selected module
            mq, display = init_gas_module(menu, display)
            # Start Monitoring
            while True:
                perc = mq.MQPercentage()
                # Alert if over threshold
                if perc["GAS_LPG"] > LPG_THRESH or perc["CO"] > CO_THRESH or perc["SMOKE"] > SMOKE_THRESH:
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
                if GPIO.input(BUTTON_BACK) == GPIO.HIGH:
                    print("\nReturn to main menu\n")
                    GPIO.cleanup()
                    break
    except:
         print("\nAbort by User")
         cleanup(display)

if __name__ == "__main__":
    main()
