import time
from pynput.mouse import Button, Controller
from pynput.keyboard import Listener, KeyCode

mouse = Controller()
# for i in range(6):
#     time.sleep(1)
#     mouse.position = (560+65*i, 650)
#     print('pos:', 560+65*i, 650)

time.sleep(0.5)
mouse.position = (525, 480)
time.sleep(0.5)
mouse.position = (600, 600)
time.sleep(0.5)
