#!/usr/bin/env python3
'''
GUI for client
Copyright (C) 2021 nikita_x44 <nikita@okic.ru>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''
import tkinter as tk
import client as ws
import json



class window:
	def __init__(self, url):
		bheight=2
		bwidth =10
		self.url=url
		self.window=tk.Tk()
		self.window.title('Remote Keys')
		self.init_ws()


		for i in range(5): # read first 5 messages
			self.ws.send('get')
			raw_comms=self.ws.recv(1) # wait 5 seconds
			try:
				buf=json.loads(raw_comms)
				comms={}
				for i in buf:
					try:
						comms[str(i.get('keyCode'))]=(i.get('Name'),i.get('pos'))
					except:
						pass
				# if data is valid json
				break
			except Exception as ex:
				pass
		else:
			print('fatal error: cannot find and/or parse config')
			exit(1)

		maxy=-1 # used to place EXIT button
		for id in comms:
			text, buf=comms[id]
			x=buf['x']
			y=buf['y']
			if y>maxy:
				maxy=y
			def wrapper(i): # wrapper runction
				tk.Button(
					self.window, text=text , width=bwidth, height=bheight, # create button with text and size
					command=(lambda: self.ws.send('key '+str(i))) # send command to server on click
				).grid(column=x, row=y) # place button at (x; y)

			wrapper(id)

		# exit button
		key_exit=tk.Button(self.window, text="EXIT", width=bwidth, height=bheight, command=self.window.quit)
		key_exit.grid(column=1, row=maxy+1) # place exit button after the last line

		try:
			self.window.mainloop()
		except:
			self.window.quit()

	def init_ws(self):
		self.ws=ws.wsc(self.url)
		ws.thread.start_new_thread(ws.pinger,(self.ws,))
		self.ws.wait2connect()

if __name__=='__main__':
	window("ws://localhost:8081/ws")
