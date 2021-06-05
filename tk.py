#!/usr/bin/env python3.6
import tkinter as tk
import client as ws
import json



class window:
	def __init__(self):
		bheight=2
		bwidth =10
		self.window=tk.Tk()
		self.window.title('Remote Keys')

		self.init_ws()

		self.ws.send('get')
		for i in range(5):
			raw_comms=self.ws.recv(5)
			try:
				buf=json.loads(raw_comms)
				comms={}
				for i in buf:
					try:
						comms[str(i.get('keyCode'))]=(i.get('Name'),i.get('pos'))
					except:
						pass
				break
			except Exception as ex:
				pass
		else:
			print('fatal error: cannot find and/or parse rules.json')
			exit(1)

		maxy=-1
		for id in comms:
			text, buf=comms[id]
			x=buf['x']
			y=buf['y']
			if y>maxy:
				maxy=y
			def buf(i):
				tk.Button(
					self.window, text=text , width=bwidth, height=bheight,
					command=(lambda: self.ws.send('key '+str(i)))
				).grid(column=x, row=y)
			buf(id)

		# exit button
		key_exit=tk.Button(self.window, text="EXIT" , width=bwidth, height=bheight, command=self.window.quit )

		key_exit.grid(column=1, row=maxy+1)

		self.window.mainloop()

	def init_ws(self):
		self.ws=ws.wsc("ws://192.168.1.237:8081/ws")
		ws.thread.start_new_thread(ws.pinger,(self.ws,))

if __name__=='__main__':
	window()
