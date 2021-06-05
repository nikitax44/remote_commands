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
		else:
			self.query.append(message)		
#		print(message)

	def on_error(self, ws, error):
		if error=='Connection to remote host was lost.':
			restart(self)
		elif '[Errno 111]' in error:
			time.sleep(5)
		else:
			print('error:',error)

	def on_close(self, ws):
		pass
#		print("### closed ###")

	def on_open(self, ws):
		pass
#		print("### open ###")

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
		self.query=[]
		thread.start_new_thread(self.ws.run_forever, ())
	def send(self, value, ttl=5):
		try:
			return self.ws.send(value)
		except:
			restart(self)
			if ttl==0:
				return
			return self.send(value, ttl-1)
	def close(self):
		self.ws.close()
		self.on_close(self.ws)

	def recv(self, timeout=None, interval=0.01):
		i=0
		while not len(self.query):
			time.sleep(interval)
			if timeout != None and i>=timeout/interval:
				break
			i+=1
		try:
			return self.query.pop(0)
		except:
			pass
def pinger(ws):
	while True:
		time.sleep(5)
		ws.send('ping')
		time.sleep(5)
		if not ws.pong:
			restart(ws)

def restart(ws):
	ws.close()
	ws.__init__(ws.url)
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
