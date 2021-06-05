import tkinter as tk
import client as ws

class window:
	def __init__(self):
		bheight=1
		bwidth =5
		self.window=tk.Tk()
		self.window.title('Remote Keys')

		# mouse keys
		key_left =tk.Button(self.window, text="LEFT" , width=bwidth, height=bheight, command=self.key_click_left )
		key_right=tk.Button(self.window, text="RIGHT", width=bwidth, height=bheight, command=self.key_click_right)
		key_up   =tk.Button(self.window, text="UP"   , width=bwidth, height=bheight, command=self.key_click_up   )
		key_down =tk.Button(self.window, text="DOWN" , width=bwidth, height=bheight, command=self.key_click_down )
		key_click=tk.Button(self.window, text="CLICK", width=bwidth, height=bheight, command=self.key_click_click)

		key_left .grid(column=0, row=1)
		key_right.grid(column=2, row=1)
		key_up   .grid(column=1, row=0)
		key_down .grid(column=1, row=2)
		key_click.grid(column=1, row=1)

		# info key
		key_info =tk.Button(self.window, text="INFO" , width=bwidth, height=bheight, command=self.key_click_info )

		key_info .grid(column=1, row=3)

		# nav keys
		key_back =tk.Button(self.window, text="BACK" , width=bwidth, height=bheight, command=self.key_click_back )
		key_full =tk.Button(self.window, text="FULL" , width=bwidth, height=bheight, command=self.key_click_full )
		key_forw =tk.Button(self.window, text="FORW" , width=bwidth, height=bheight, command=self.key_click_forw )

		key_back .grid(column=0, row=4)
		key_full .grid(column=1, row=4)
		key_forw .grid(column=2, row=4)

		# next/prev video
		key_prev =tk.Button(self.window, text="PREV" , width=bwidth, height=bheight, command=self.key_click_prev )
		key_pause=tk.Button(self.window, text="PAUSE", width=bwidth, height=bheight, command=self.key_click_pause)
		key_next =tk.Button(self.window, text="NEXT" , width=bwidth, height=bheight, command=self.key_click_next )

		key_prev .grid(column=0, row=5)
		key_pause.grid(column=1, row=5)
		key_next .grid(column=2, row=5)


		# sound
		key_lowv =tk.Button(self.window, text="LOWV" , width=bwidth, height=bheight, command=self.key_click_lowv )
		key_mute =tk.Button(self.window, text="MUTE" , width=bwidth, height=bheight, command=self.key_click_mute )
		key_higv =tk.Button(self.window, text="HIGV" , width=bwidth, height=bheight, command=self.key_click_higv )

		key_lowv .grid(column=0, row=6)
		key_mute .grid(column=1, row=6)
		key_higv .grid(column=2, row=6)

		# exit
		key_exit =tk.Button(self.window, text="EXIT" , width=bwidth, height=bheight, command=self.window.quit )

		key_exit .grid(column=1, row=7)


		self.init_ws()


		self.window.mainloop()

	def init_ws(self):
		self.ws=ws.wsc("ws://192.168.1.237:8081/ws")
		ws.thread.start_new_thread(ws.pinger,(self.ws,))

	def key_click_left (self):
#		print('left')
		self.ws.send('k16')
	def key_click_right(self):
#		print('right')
		self.ws.send('k17')
	def key_click_up   (self):
#		print('up')
		self.ws.send('k18')
	def key_click_down (self):
#		print('down')
		self.ws.send('k19')
	def key_click_click(self):
#		print('click')
		self.ws.send('k20')

	def key_click_info (self):
#		print('info')
		self.ws.send('k9')

	def key_click_back (self):
#		print('back')
		self.ws.send('k6')
	def key_click_full (self):
#		print('full')
		self.ws.send('k8')
	def key_click_forw (self):
#		print('forw')
		self.ws.send('k7')

	def key_click_prev (self):
#		print('prev')
		self.ws.send('k4')
	def key_click_pause(self):
#		print('pause')
		self.ws.send('k3')
	def key_click_next (self):
#		print('next')
		self.ws.send('k5')

	def key_click_lowv (self):
#		print('lowv')
		self.ws.send('k1')
	def key_click_mute (self):
#		print('mute')
		self.ws.send('k0')
	def key_click_higv (self):
#		print('higv')
		self.ws.send('k2')

if __name__=='__main__':
	window()
