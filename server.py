#!/usr/bin/env python
import asyncio
import websockets
import pyautogui as pg
import pulse
import json
import time
#from time import sleep

try:
	with open('rules.json') as f:
		raw_comms=f.read()
	buf=json.loads(raw_comms)
	comms={}
	for i in buf:
		try:
			comms[str(i.get('keyCode'))]=i.get('exec','print("unhandled key")')
		except:
			pass
except:
	print('fatal error: cannot find and/or parse rules.json')
	exit(1)



async def client_consumer(w,p):
	'''
	commands must be in format:
	<command> <arg1> <arg2> etc.
	
	eg:
	ping
	or
	key 0
	or
	text hi hello
	'''
	await w.send('')
	try:
		async for m in w:
#		print(m)
			try:
				command, *args=m.split()
				if command=='ping':
					await w.send('pong')
				elif command=='key':
					ret=consume(args)
					if ret!=None:
						try:
							await w.send(ret)
						except Exception as ex:
							print(type(ex), ex)
				elif command=='get':
					ret=get_val(args)
					if ret!=None:
						try:
							await w.send(ret)
						except Exception as ex:
							print(type(ex), ex)
				else:
					raise ValueError('unknown command: '+str(m)) # if it raises, it will be catched
			except (websockets.exceptions.ConnectionClosedError,):
				pass
			except Exception as ex:																	# < by this except 
				print(type(ex),ex)
	except (websockets.exceptions.ConnectionClosedError,):
		pass
	except Exception as ex:
		print(type(ex),ex)

def consume(m):
	try:
		m=list(m)
		code=str(m.pop(0))
		command=comms.get(code, "print('error: unknown keycode')")
		print('start command:',command)
		exec(command, {'args':m, 'pulse':pulse, 'pg':pg, 'time':time})
	except pg.FailSafeException:
		pass
	except pulse.pc.pulsectl.PulseError:
		print('Failed to connect to pulseaudio server')
	except Exception as ex:
		print('error:',m,type(ex),ex)

def get_val(args):
	return raw_comms


if __name__=='__main__':
	try:	
		start_server = websockets.serve(client_consumer, "0.0.0.0", 8081)
		asyncio.get_event_loop().run_until_complete(start_server)
		asyncio.get_event_loop().run_forever()
	except KeyboardInterrupt:
		pass
