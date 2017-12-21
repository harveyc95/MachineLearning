import pyautogui

clicked = False

def mouse(_x, _y, click, activate):
	global clicked
	if not activate:
		return
	if (click and not clicked):
		clicked = True
		pyautogui.mouseDown(x=_x, y=_y, button='left')
	if (not click and clicked):
		clicked = False
		pyautogui.mouseUp(x=_x, y=_y, button='left')
	pyautogui.moveTo(_x, _y)

def test():
	for i in range (150, 250, 10):
		for j in range (150, 250, 10):
			mouse(i, j, j != 240, 1)

test()