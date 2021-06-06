#!/usr/bin/env python3.6
import pulsectl as pc

def get_sinks():
	pulse=pc.Pulse()
	sinks=pulse.sink_list()
	return pulse, sinks

#volume
def set_volume(value, sink=None):
	if sink==None: # if <sink> is None, set <sinks> to [<sink>], else list of all sinks
		pulse, sinks=get_sinks()
	else:
		sinks=[sink]

	for sink in sinks:
		sink.volume.value_flat=value
		pulse.volume_set(sink, sink.volume)

def mod_volume(value, sink=None):
	if sink==None:
		pulse, sinks=get_sinks()
	else:
		sinks=[sink]
	for sink in sinks:
		sink.volume.value_flat+=value
		pulse.volume_set(sink, sink.volume)

def get_volume(sink=None):
	if sink==None:
		pulse, sinks=get_sinks()
	else:
		sinks=[sink]
	out={}
	for sink in sinks:
		out[sink]=sink.volume.value_flat
	return out

#mute
def set_mute(mute, sink=None): # if <mute> is 2, toggle mute, else set to <mute>
	if sink==None:
		pulse, sinks=get_sinks()
	else:
		sinks=[sink]
	for sink in sinks:
		if mute==2:
			mute=not sink.mute
		pulse.mute(sink, mute)

def get_mute(sink=None):
	if sink==None:
		pulse, sinks=get_sinks()
	else:
		sinks=[sink]
	out={}
	for sink in sinks:
		out[sink]=sink.mute
	return out
