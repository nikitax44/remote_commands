#!/usr/bin/env python3.6
import asyncio
import websockets
import pyautogui as pg
import pulse
#from time import sleep


async def print_all(w,p):
	await w.send('')
	try:
		async for m in w:
#		print(m)
			if m=='ping':
				await w.send('pong')
			else:
				consume(m)
	except:
		pass

def consume(m):
	try:
		if False: pass
		elif m.startswith('k'):
			code=int(m[1:])
			if code==0:
				print('mute')
				pulse.set_mute(2)
			elif code==1:
				print('volumedown')
				pulse.mod_volume(-0.1)
			elif code==2:
				print('volumeup')
				pulse.mod_volume(0.1)
			elif code==3:
				print('pause')
				pg.press('space')
			elif code==4:
				print('previous video')
				pg.hotkey('shift','p')
			elif code==5:
				print('next video')
				pg.hotkey('shift','n')
			elif code==6:
				print('left')
				pg.press('left')
			elif code==7:
				print('right')
				pg.press('right')
			elif code==8:
				print('fullscreen')
				pg.press('f')
			elif code==9:
				print('info')
				pg.move(1, 0)
				pg.move(-1, 0)
			elif code==16:
				print('mouse left')
				pg.move(-10,0)
			elif code==17:
				print('mouse right')
				pg.move(10,0)
			elif code==18:
				print('mouse up')
				pg.move(0,-10)
			elif code==19:
				print('mouse down')
				pg.move(0,10)
			elif code==20:
				print('mouse click')
				pg.click()
			else:
				print('error: unknow keycode',m)
		else:
			print('invaud command',m)
	except pg.FailSafeException:
		pass
	except Exception as ex:
		print('error:',m,type(ex),ex)


if __name__=='__main__':
	try:
		start_server = websockets.serve(print_all, "0.0.0.0", 8081)
		asyncio.get_event_loop().run_until_complete(start_server)
		asyncio.get_event_loop().run_forever()
	except KeyboardInterrupt:
		pass
