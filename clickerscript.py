# importing time and threading
import time
import math
import threading
import pytesseract
from pynput.mouse import Button, Controller
# pynput.keyboard is used to watch events of keyboard for start and stop of auto-clicker
from pynput.keyboard import Listener, KeyCode
# to capture screen
import pyscreenshot as ImageGrab

from imageinsideimage import find_insideimage

# PIXELS DEFINITIONS----------------------------------------------------
CLICK_PIX = (755,330)
HERO_BUTTON = (600,700)
UPG_HERO = (300,680)
MERC_BUTTON = (700,700)
UPG_MERC = (840,510)
AGAIN_BOSS = (815,100)
LOW_MENU = (900,435)
TEXT_BBOX = (525,445,925,700)
# ------------------------------------------------------------------------

# four variables are created to control the auto-clicker
# delay = 0.004 # human normally?
delay_attack = 0.005
delay_buy = 60
delay_buttons = 0.1
button = Button.left
start_stop_key = KeyCode(char='s')
exit_key = KeyCode(char='e')
onlyattack_key = KeyCode(char='a')


# threading.Thread is used to control clicks
class ClickAttack(threading.Thread):
	# this clas is only for the clicks to attack
	# delay and button is passed in class to check execution of auto-clicker
	def __init__(self, delay, button):
		super(ClickAttack, self).__init__()
		self.clicks = 0
		self.delay = delay
		self.button = button
		self.running = False
		self.program_running = True

	def start_clicking(self):
		self.running = True

	def stop_clicking(self):
		self.running = False

	def exit(self):
		self.stop_clicking()
		self.program_running = False
		print('clicks:', self.clicks)

	# method to check and run loop until it is true another loop will check
	# if it is set to true or not, for mouse click it set to button and delay.
	def run(self):
		while self.program_running:
			while self.running:
				# every delay time will click in screen
				mouse.position = CLICK_PIX
				mouse.click(self.button)
				self.clicks += 1
				time.sleep(self.delay)

# threading.Thread is used to control clicks
class ClickBuy(threading.Thread):
	# this is only to buy new things
	# delay and button is passed in class to check execution of auto-clicker
	def __init__(self, delay, button, attack_thread):
		super(ClickBuy, self).__init__()
		self.clicks = 0
		self.iteration = 1
		self.delay = delay
		self.button = button
		self.running = False
		self.program_running = True
		self.attack = attack_thread

	def start_clicking(self):
		self.running = True

	def stop_clicking(self):
		self.running = False
		print('clickss:', self.clicks)

	def exit(self):
		self.stop_clicking()
		self.program_running = False
		print('clicks:', self.clicks)

	# method to check and run loop until it is true another loop will check
	# if it is set to true or not, for mouse click it set to button
	# and delay.
	def run(self):
		while self.program_running:
			while self.running:
				self.attack.stop_clicking() #stops the attacking meanwhile
				time.sleep(delay_buttons)

				# every 3 times will check the hero, the other 3 times will check mercenaries
				if self.iteration % 7 == 0:
					# opens the hero menu
					mouse.position = HERO_BUTTON
					mouse.click(self.button)
					time.sleep(0.2)

					self.scrolldown_list((720, 520), 2)
					time.sleep(delay_buttons)
					self.check_allhero()

					# in the end clicks to lower the menu
					time.sleep(0.3)
					self.click(LOW_MENU, 1, delay_buttons)

					# will check the boss button and abilities only every 3 times
					pix2click = self.check_bossagain()
					if pix2click != None: # si ha encontrado algo para clickar, lo clicka
						self.click(pix2click, 1, delay_buttons)

					for i in range(6):
						self.click((560+65*i, 650), 1,delay_buttons)

				else:

					# every 10 times will check the higher mercenaries
					if self.iteration % 11 == 0:
						check_higher = True
					else:
						check_higher = False

					# opens the mercenary menu
					mouse.position = MERC_BUTTON
					mouse.click(self.button)
					time.sleep(delay_buttons)

					if check_higher:
						time.sleep(delay_buttons)
						self.check_allmercenaries(True)
						time.sleep(delay_buttons)

						self.scrolldown_list((720, 520), 4)
					else:
						time.sleep(delay_buttons)
						self.check_allmercenaries(False)
						time.sleep(delay_buttons)

						self.scrolldown_list((720, 520), 1)

					# in the end clicks to lower the menu
					time.sleep(0.3)
					self.click(LOW_MENU, 1, delay_buttons)

				self.iteration += 1
				self.attack.start_clicking() #reestarts the attacking
				time.sleep(self.delay) #waits until next call

	def click(self, position, times, delay):
		# function to click given a position, the number of times and a delay between clicks
		# if only 1 click, this will wait the delay before continuing
		mouse.position = position
		for i in range(times):
			mouse.click(self.button)
			time.sleep(delay)

	def move_smoothly(self, mx, my):
		for i in range(math.ceil(mx/2)):
			mouse.move(2, 0)
			time.sleep(0.0005)
		for i in range(math.ceil(my/2)):
			mouse.move(0, 2)
			time.sleep(0.0005)

	def slide(self, position_o, position_d, times, delay):
		# function to slide smoothly the mouse given origin position to destination position and the delay between slide
		mx = position_d[0] - position_o[0]
		my = position_d[1] - position_o[1]

		for i in range(times):
			mouse.position = position_o
			mouse.press(self.button)
			time.sleep(delay)
			self.move_smoothly(mx, my)
			time.sleep(delay)
			mouse.release(self.button)
			time.sleep(delay)

	def check_mercenaries(self, last_found):
		blue = (73, 158, 186)
		yellow = (247, 212, 28)

		captura = ImageGrab.grab()
		for i in range(last_found, 3):
			time.sleep(delay_buttons)
			pixel_mercenary = (800, 650-70*i)
			mouse.position = pixel_mercenary
			rgb = captura.getpixel(pixel_mercenary)

			for color in [blue, yellow]: # check any of both colors
				diff = sum([abs(x-y) for x, y in zip(color, rgb)])
				if diff < 10:
					return pixel_mercenary, i
		return None, 3

	def check_hero(self, last_found):
		orange = (238, 105, 20)
		yellow = (247, 209, 24)

		captura = ImageGrab.grab()
		for i in range(last_found, 3):
			pixel_hero = (800, 660-70*i)
			time.sleep(delay_buttons)
			mouse.position = pixel_hero
			rgb = captura.getpixel(pixel_hero)

			for color in [orange, yellow]: # check any of both colors
				diff = sum([abs(x-y) for x, y in zip(color, rgb)])
				if diff < 10:
					return pixel_hero, last_found
		return None, 3

	def check_bossagain(self):
		orange = (240, 110, 64)
		captura = ImageGrab.grab()
		pixel_boss = AGAIN_BOSS

		mouse.position = pixel_boss
		rgb = captura.getpixel(pixel_boss)

		diff = sum([abs(x-y) for x, y in zip(orange, rgb)])
		if diff < 10:
			return pixel_boss
		return None

	def check_abilities(self, it):
		mouse.position = (560+65*it, 650)
		time.sleep(delay_buttons)

		ability_found = find_insideimage('imagenes/ability'+str(it)+'.png', (520+65*it, 610, 600+65*it, 680))
		if ability_found != (0,0):
			return (560+65*it, 650)
		return None


	def scrolldown_list(self, position, times):
		# scroll down times times
		mouse.position = position
		time.sleep(delay_buttons)
		for i in range(times):
			mouse.scroll(0, -2)
			time.sleep(0.3)

	def check_allmercenaries(self, slide_bool):
		# check to upgrade the mercenary, if slide_bool try to slide up the list
		# (up max 10 times) if the first mercenary found, stop sliding

		if slide_bool:
			times = 2
		else:
			times = 1

		for i in range(times):
			pix2click = (0,0)
			last_found_merc = 0
			last_found_hero = 0

			while pix2click != None:
				if last_found_merc != 3: #if already checked all, not coming back
					pix2click, last_found_merc = self.check_mercenaries(last_found_merc)

					if pix2click != None: # si ha encontrado algo para clickar, lo clicka
						self.click(pix2click, 20, 0.005)

			time.sleep(delay_buttons)
			if slide_bool:
				isfirst = self.check_if_text(TEXT_BBOX, 'takeda')
				print('ii', isfirst)
				if isfirst:
					break
				else:
					self.slide((720, 520), (720, 725), 1, delay_buttons)
				time.sleep(delay_buttons)


	def check_if_text(self, bbox_used, text):
		with ImageGrab.grab(bbox = bbox_used) as rgba, rgba.convert(mode='RGB') as screenshot:
			texto = pytesseract.image_to_string(screenshot)
			print(texto)
			return text in texto.lower()

	def check_allhero(self):
		# check to upgrade the hero, then try to slide up the list
		# if the first mercenary found, stop sliding
		t = 3
		for i in range(t):
			pix2click = (0,0)
			last_found_merc = 0
			last_found_hero = 0

			while pix2click != None:
				if last_found_merc != 3: #if already checked all, not coming back
					pix2click, last_found_merc = self.check_hero(last_found_merc)

					if pix2click != None: # si ha encontrado algo para clickar, lo clicka
						self.click(pix2click, 20, 0.005)

			if i != t-1:
				time.sleep(delay_buttons)
				self.slide((720, 520), (720, 725), 1, delay_buttons)


# instance of mouse controller is created
mouse = Controller()
attack_thread = ClickAttack(delay_attack, button)
attack_thread.start()
buy_thread = ClickBuy(delay_buy, button, attack_thread)
buy_thread.start()

buy_thread.start_clicking()

# on_press method takes key as argument
def on_press(key):
	# start_stop_key will stop clicking if running flag is set to true
	if key == start_stop_key:
		if attack_thread.running or buy_thread.running:
			attack_thread.stop_clicking()
			buy_thread.stop_clicking()
		else:
			buy_thread.start_clicking()

	# here exit method is called and when key is pressed it terminates auto clicker
	elif key == exit_key:
		attack_thread.exit()
		buy_thread.exit()
		listener.stop()

	# here will indicate to only attack, ignore upgrades, to stop start_stop_key
	elif key == onlyattack_key:
		attack_thread.start_clicking()
		buy_thread.stop_clicking()


with Listener(on_press=on_press) as listener:
	listener.join()
