from ctypes import windll
dc= windll.user32.GetDC(0)

# def getpixel(x,y):
#     # return windll.gdi32.GetPixel(dc,x,y)
#     return tuple(int.to_bytes(windll.gdi32.GetPixel(dc,x,y), 3, "little"))
#
# print(getpixel(100, 0))
# print(getpixel(255, 0))
# print(getpixel(640, 254))
# print(getpixel(325, 265))
import pyscreenshot as ImageGrab

import time
time.sleep(2)

# im=ImageGrab.grab(bbox=(10,10,510,510)) # X1,Y1,X2,Y2
# im.show()
image = ImageGrab.grab() #Define an area to capture.
rgb = image.getpixel((528, 221)) #What pixel do we want?
print(rgb)
