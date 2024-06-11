import machine
import time

class LCD_2004:
    
    ENABLE = 0x04 #Set Entry Mode
    RS     = 0x01 # Register select bit
    WIDTH  = 20

    #initializes objects and lcd
    def __init__(self, i2c, slave_id=0x27):
        self.i2c     = i2c
        self.slave_id = slave_id
        self.BKLIGHT = 0x08 # Holds Backlight state, 0x08 ON, 0x00 OFF
        self.lcd_write(0x03)
        self.lcd_write(0x03)
        self.lcd_write(0x03)
        self.lcd_write(0x02)

        self.lcd_write(0x20 | 0x08 | 0x04 | 0x00) #Set Functions 2Line,5x8,4Bit Mode
        self.lcd_write(0x08 | 0x04) #Turn Display On
        self.lcd_write(0x01) #Clear Screen
        self.lcd_write(0x04 | 0x02) #Set Entry Mode Left -> Right
        time.sleep_ms(300)

    def lcd_strobe(self, data):
        dont_echo = self.i2c.writeto(self.slave_id,bytes([data | self.ENABLE | self.BKLIGHT]))
        time.sleep_ms(1)
        dont_echo = self.i2c.writeto(self.slave_id,bytes([(data & ~self.ENABLE) | self.BKLIGHT]))
        time.sleep_ms(1)

    def lcd_write_four_bits(self, data):
        dont_echo = self.i2c.writeto(self.slave_id,bytes([data | self.BKLIGHT]))
        self.lcd_strobe(data)

    # write a command to lcd
    def lcd_write(self, cmd, mode=0):
        self.lcd_write_four_bits(mode | (cmd & 0xF0))
        self.lcd_write_four_bits(mode | ((cmd << 4) & 0xF0))

    def set_line(self,line,col=0):
        if line == 1:
            self.lcd_write(0x80+col)
        if line == 2:
            self.lcd_write(0xC0+col)
        if line == 3:
            self.lcd_write(0x94+col)
        if line == 4:
            self.lcd_write(0xD4+col)

    def lcd_print(self, string, line=0, col=0):
        self.set_line(line,col)
        i = 1
        for char in string:
            if ((i > self.WIDTH) & (line < 4)):
                line = line + 1
                self.set_line(line,0)
                i = 1
            if ((i > self.WIDTH) & (line == 4)):
                break
            self.lcd_write(ord(char),self.RS)
            i = i + 1

    def lcd_off(self):
        self.lcd_write(0x08 | 0x00)

    def lcd_on(self):
        self.lcd_write(0x08 | 0x04)

    def lcd_clear(self):
        self.lcd_write(0x01) #Clear Screen
        self.lcd_write(0x02) #Set Home

    def lcd_backlight(self, on):
        if on:
            self.BKLIGHT=0x08
        else:
            self.BKLIGHT=0x00
        self.lcd_write(0)