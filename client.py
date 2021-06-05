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
#		print(message)

	def on_error(self, ws, error):
		if error=='Connection to remote host was lost.':
			restart(self)
		print('error:',error)

	def on_close(self, ws):
		print("### closed ###")

	def on_open(self, ws):
		print("### open ###")

	def __init__(self, url):
#	websocket.enableTrace(True)
		self.ws = websocket.WebSocketApp(url,
			on_open = self.on_open,
			on_message = self.on_message,
			on_error = self.on_error,
			on_close = self.on_close
		)
		self.pong=True
		self.url=url
		thread.start_new_thread(self.ws.run_forever, ())
	def send(self, value, n=5):
		try:
			return self.ws.send(value)
		except:
			restart(self)
			if n==0:
				return
			return self.send(value, n-1)
	def close(self):
		self.ws.close()
		self.on_close(self.ws)

def pinger(ws):
	while True:
		time.sleep(5)
		ws.send('ping')
		time.sleep(5)
		if not ws.pong:
			restart(ws)

def restart(ws):
	ws.close()
	ws.ws=websocket.WebSocketApp(ws.url,
		on_open = ws.on_open,
		on_message = ws.on_message,
		on_error = ws.on_error,
		on_close = ws.on_close
	)
	ws.pong=True
	thread.start_new_thread(ws.ws.run_forever, ())
	time.sleep(0.5)

if __name__ == "__main__":
	with open('README') as f:
		print(f.read())
	ws=wsc("ws://192.168.1.237:8081/ws")
	thread.start_new_thread(pinger,(ws,))
#	print(1)
	while True:
		ws.send(input())
		time.sleep(0.01)
