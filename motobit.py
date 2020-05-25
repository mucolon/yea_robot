from microbit import *


class MotoBit():
    '''Initialize moto:bit hardware.
    Args:
        invert_left (bool): Invert left motor polarity. (default: False)
        invert_right (bool): Invert right motor polarity. (default: False)
    '''
    I2C_ADDR = 0x59         # 89
    CMD_ENABLE = 0x70       # 112
    CMD_SPEED_LEFT = 0x21   # 33
    CMD_SPEED_RIGHT = 0x20  # 32
    DUTY_MIN = 0x00         # 0
    DUTY_NEG_CTE = 0x7f     # 127
    DUTY_POS_CTE = 0x80     # 128
    DUTY_MAX = 0xff         # 255

    def __init__(self, invert_left=False, invert_right=False):
        self.invert_left = invert_left
        self.invert_right = invert_right
        self.INVERT = (invert_left, invert_right)

    def enable(self):
        '''Enable motor driver.
        '''
        i2c.write(self.I2C_ADDR, bytes([self.CMD_ENABLE, 0x01]))

    def disable(self):
        '''Disable motor driver.
        '''
        i2c.write(self.I2C_ADDR, bytes([self.CMD_ENABLE, 0x00]))

    def drive(self, speed_left, speed_right):
        '''Drive motors based on 100 point scale.
        Args:
            speed_left (int|float): motor power value [-100, 100]
            speed_right (int|float): motor power value [-100, 100]
        '''
        speeds = [speed_left, speed_right]
        for i in range(len(speeds)):
            if self.INVERT[i] == True:
                speeds[i] = -1 * speeds[i]
            if speeds[i] < 0:
                if speeds[i] < -100:
                    speeds[i] = -100
                speeds[i] = round(speeds[i] * 127 / 100) + self.DUTY_NEG_CTE
            elif speeds[i] > 0:
                if speeds[i] > 100:
                    speeds[i] = 100
                speeds[i] = round(speeds[i] * 127 / 100) + self.DUTY_POS_CTE
            else:
                speeds[i] = self.DUTY_POS_CTE
        i2c.write(self.I2C_ADDR, bytes([self.CMD_SPEED_LEFT, speeds[0]]))
        i2c.write(self.I2C_ADDR, bytes([self.CMD_SPEED_RIGHT, speeds[1]]))

    def drive_duty(self, speed_left, speed_right):
        '''Drive motors based on duty cycle values.
        Args:
            speed_left (int): duty cycle value [0, 255]
            speed_right (int): duty cycle value [0, 255]
        '''
        speeds = [speed_left, speed_right]
        for i in range(len(speeds)):
            if self.INVERT[i] == True:
                speeds[i] = self.DUTY_MAX - speeds[i]
        i2c.write(self.I2C_ADDR, bytes([self.CMD_SPEED_LEFT, speeds[0]]))
        i2c.write(self.I2C_ADDR, bytes([self.CMD_SPEED_RIGHT, speeds[1]]))