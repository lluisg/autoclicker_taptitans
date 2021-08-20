import time
from pynput.mouse import Button, Controller
from pynput.keyboard import Listener, KeyCode

mouse = Controller()

pos_o = (720, 520)
# pos_d = (720, 655)
pos_d = (720, 725)
mov_x = pos_d[0] - pos_o[0]
mov_y = pos_d[1] - pos_o[1]
# pos_o = (1358, 200)
# pos_d = (1358, 450)

# time.sleep(0.5)
# mouse.position = pos_o
#
# time.sleep(0.5)
# mouse.scroll(0, -2)
# time.sleep(0.5)
# mouse.scroll(0, -2)
# time.sleep(0.5)
# mouse.scroll(0, -2)

from imageinsideimage import find_insideimage

def move_smoothly(mx, my):
    for i in range(mx):
        mouse.move(1, 0)
        time.sleep(0.003)
    for i in range(my):
        mouse.move(0, 1)
        time.sleep(0.003)


time.sleep(0.5)
image_found = find_insideimage('imagenes/mercenary_up.png', (525, 460, 600, 600))
# this image is the one when there is no mercenary bought still
# image_found2 = find_insideimage('imagenes/mercenary_up.png', (525, 480, 600, 550))
image_found2 = (0,0)

# move up until finds the first mercenary
while(image_found == (0,0) and image_found2 == (0,0)):

    mouse.position = pos_o
    time.sleep(0.5)
    mouse.press(Button.left)
    move_smoothly(mov_x, mov_y)
    time.sleep(0.5)
    mouse.release(Button.left)
    time.sleep(1.5)

    ## NO PASA RES PER EL TEMPS JA QUE DE NORMAL FARA LA CAPTURA E INTENTARA PUJAR DE NIVELL ABANS DE TORNAR A BAIXAR
    image_found = find_insideimage('imagenes/mercenary_up.png', (515, 450, 650, 690))
    image_found2 = (0,0)
    print(image_found, image_found2)
    time.sleep(0.5)


print('done')
