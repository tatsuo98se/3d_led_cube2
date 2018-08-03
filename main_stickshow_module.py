import sys
import libled.util.logger as logger
import traceback
from libled.stick_sdk import STICK

while True:
    g0 = STICK.get_accel()
    line = int(g0[1] * 8.0 / 0x8000) + 8
    STICK.show_line(line)

    
