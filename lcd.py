#!/usr/bin/env python3 

#import
import RPi.GPIO as GPIO
import time

class LCD_Display():

    # Define some device constants
    LCD_WIDTH = 16    # Maximum characters per line
    LCD_CHR = True
    LCD_CMD = False
    LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
    LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line
 
    # Timing constants
    E_PULSE = 0.0005
    E_DELAY = 0.0005
 
    def __init__(self, LCD_RS=26, LCD_E=19, LCD_D4=13, LCD_D5=6, LCD_D6=5, LCD_D7=16):
        # Setup Pins
        self.LCD_RS = LCD_RS
        self.LCD_E  = LCD_E
        self.LCD_D4 = LCD_D4
        self.LCD_D5 = LCD_D5
        self.LCD_D6 = LCD_D6
        self.LCD_D7 = LCD_D7
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)       # Use BCM GPIO numbers
        GPIO.setup(self.LCD_E, GPIO.OUT)
        GPIO.setup(self.LCD_RS, GPIO.OUT)
        GPIO.setup(self.LCD_D4, GPIO.OUT)
        GPIO.setup(self.LCD_D5, GPIO.OUT)
        GPIO.setup(self.LCD_D6, GPIO.OUT)
        GPIO.setup(self.LCD_D7, GPIO.OUT)

        # Initialise display
        self.lcd_byte(0x33, self.LCD_CMD) # 110011 Initialise
        self.lcd_byte(0x32, self.LCD_CMD) # 110010 Initialise
        self.lcd_byte(0x06, self.LCD_CMD) # 000110 Cursor move direction
        self.lcd_byte(0x0C, self.LCD_CMD) # 001100 Display On,Cursor Off, Blink Off
        self.lcd_byte(0x28, self.LCD_CMD) # 101000 Data length, number of lines, font size
        self.lcd_byte(0x01, self.LCD_CMD) # 000001 Clear display
        time.sleep(self.E_DELAY)

    def lcd_byte(self, bits, mode):
    # Send byte to data pins
    # bits = data
    # mode = True  for character
    # False for command

        GPIO.output(self.LCD_RS, mode) # RS

        # High bits
        GPIO.output(self.LCD_D4, False)
        GPIO.output(self.LCD_D5, False)
        GPIO.output(self.LCD_D6, False)
        GPIO.output(self.LCD_D7, False)
        if bits&0x10==0x10:
            GPIO.output(self.LCD_D4, True)
        if bits&0x20==0x20:
            GPIO.output(self.LCD_D5, True)
        if bits&0x40==0x40:
            GPIO.output(self.LCD_D6, True)
        if bits&0x80==0x80:
            GPIO.output(self.LCD_D7, True)
 
        # Toggle 'Enable' pin
        self.lcd_toggle_enable()
 
        # Low bits
        GPIO.output(self.LCD_D4, False)
        GPIO.output(self.LCD_D5, False)
        GPIO.output(self.LCD_D6, False)
        GPIO.output(self.LCD_D7, False)
        if bits&0x01==0x01:
            GPIO.output(self.LCD_D4, True)
        if bits&0x02==0x02:
            GPIO.output(self.LCD_D5, True)
        if bits&0x04==0x04:
            GPIO.output(self.LCD_D6, True)
        if bits&0x08==0x08:
            GPIO.output(self.LCD_D7, True)
 
        # Toggle 'Enable' pin
        self.lcd_toggle_enable()
 
    def lcd_toggle_enable(self):
  # Toggle enable
        time.sleep(self.E_DELAY)
        GPIO.output(self.LCD_E, True)
        time.sleep(self.E_PULSE)
        GPIO.output(self.LCD_E, False)
        time.sleep(self.E_DELAY)
 
    def lcd_string(self, message, line_num):
        if line_num == 2:
            line = self.LCD_LINE_2
        else:
            line = self.LCD_LINE_1
        # Send string to display
  
        message = message.ljust(self.LCD_WIDTH," ")
 
        self.lcd_byte(line, self.LCD_CMD)
 
        for i in range(self.LCD_WIDTH):
            self.lcd_byte(ord(message[i]), self.LCD_CHR)




if __name__ == '__main__':
    try:
        lcd = LCD_Display()
        while True:
            # Send some test
            lcd.lcd_string("Rasbperry Pi", 1)
            lcd.lcd_string("16x2 LCD Test", 2)
            time.sleep(3) # 3 second delay

            # Send some text
            lcd.lcd_string("1234567890123456", 1)
            lcd.lcd_string("abcdefghijklmnop", 2)
            time.sleep(3) # 3 second delay

    except KeyboardInterrupt:
        pass

    finally:
        lcd.lcd_byte(0x01, False)
        lcd.lcd_string("Goodbye!", 1)
        GPIO.cleanup()
