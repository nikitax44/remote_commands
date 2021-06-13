#!/usr/bin/env python3.6
'''
pulse wrap
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
