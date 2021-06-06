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
			# comms is {<keyCode1>:<exec1>, <keyCode2>:<exec2>, ...}
		except:
			pass
except:
	print('fatal error: cannot find and/or parse rules.json')
	exit(1)



async def client_consumer(ws, path): # path is unused
	'''
	commands must be in format:
	<command> [<arg1>] [<arg2>] ...
	
	eg:
	ping
	or
	key 0
	or
	text hi hello
	'''

	await ws.send('') # init
	try:
		async for msg in ws:
			try:
				command, *args=msg.split()
				func=commands.get(command, None)
				if func!=None:
					ret=func(args)
					if ret!=None:
						try:
							await ws.send(ret)
						except Exception as ex:
							print(type(ex), ex)
				else:
					raise ValueError('unknown command: '+str(msg)) # if it raises, it will be catched
			except websockets.exceptions.ConnectionClosedError:
				pass
			except Exception as ex:																	# < by this except 
				print(type(ex),ex)
	except websockets.exceptions.ConnectionClosedError:
		pass
	except Exception as ex:
		print(type(ex),ex)

def consume(args):
	try:
		args=list(args)
		code=str(args.pop(0))
		command=comms.get(code, "print('error: unknown keycode')")
		print('start command:',command)
		exec(command, {'args':args, 'pulse':pulse, 'pg':pg, 'time':time})
	except pg.FailSafeException:
		pass
	except pulse.pc.pulsectl.PulseError:
		print('Failed to connect to pulseaudio server')
	except Exception as ex:
		print('error:', [code]+args, type(ex), ex)

def get_rules(args):
	with open('rules.json') as f:
		return f.read()

commands={
	'ping':(lambda _: 'pong'),
	'key':consume,
	'get':get_rules,
}


if __name__=='__main__':
	try:	
		start_server = websockets.serve(client_consumer, "0.0.0.0", 8081)
		asyncio.get_event_loop().run_until_complete(start_server)
		asyncio.get_event_loop().run_forever()
	except KeyboardInterrupt:
		pass
