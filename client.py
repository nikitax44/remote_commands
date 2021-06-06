#!/usr/bin/env python3
import websocket
try:
	import thread
except ImportError:
	import _thread as thread
import time

class wsc:
	def on_message(self, ws, message):
		if message=='pong':
			self.pong=True
		elif message.strip()=='':
			pass
		else:
			self.queue.append(message)

	def on_error(self, ws, error):
		pass

	def on_close(self, ws):
		self.state=2

	def on_open(self, ws):
		self.state=1

	def __init__(self, url):
		self.ws = websocket.WebSocketApp(url,
			on_open = self.on_open,
			on_message = self.on_message,
			on_error = self.on_error,
			on_close = self.on_close
		)
		self.pong=True
		self.url=url
		self.queue=[]
		self.state=0
		thread.start_new_thread(self.ws.run_forever, ())

	def send(self, value):
		try:
			return self.ws.send(value)
		except:
			restart(self)
	def close(self):
		self.ws.close()
		self.on_close(self.ws)

	def recv(self, timeout=None, interval=0.01):
		i=0
		while not len(self.queue):
			time.sleep(interval)
			if timeout != None and i>=timeout/interval:
				self.ping()
				break # break on timeout
			i+=1
		try:
			return self.queue.pop(0)
		except:
			pass
	def queue_len(self):
		return len(self.queue)

	def ping(self):
		self.send('ping')
		time.sleep(2)
		if not self.pong:
			restart(self)
			
	def wait2connect(self):
		while self.state!=1:
			time.sleep(0.01)

def pinger(ws):
	while True:
		time.sleep(5)
		ws.ping()

def restart(ws):
	ws.close()
	ws.__init__(ws.url)
	time.sleep(0.5)

if __name__ == "__main__":
	ws=wsc("ws://192.168.1.237:8081/ws")
	thread.start_new_thread(pinger,(ws,))
	while True:
		com=input('command: ')
		if com=='quit':
			break
		ws.send(com)
		print(ws.queue)
		time.sleep(0.01)
		feedback=ws.recv(0.1)
		if feedback:
			print(feedback)
