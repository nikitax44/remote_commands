"use strict";
/*
 *	Copyright (c) 2018-2019 Unrud <unrud@outlook.com>
 *
 *	This file is part of Remote-Touchpad.
 *
 *	Remote-Touchpad is free software: you can redistribute it and/or modify
 *	it under the terms of the GNU General Public License as published by
 *	the Free Software Foundation, either version 3 of the License, or
 *	(at your option) any later version.
 *
 *	Remote-Touchpad is distributed in the hope that it will be useful,
 *	but WITHOUT ANY WARRANTY; without even the implied warranty of
 *	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *	GNU General Public License for more details.
 *
 *	You should have received a copy of the GNU General Public License
 *	along with Remote-Touchpad.  If not, see <http://www.gnu.org/licenses/>.
 */


const KEY_VOLUME_MUTE = 0;
const KEY_VOLUME_DOWN = 1;
const KEY_VOLUME_UP = 2;
const KEY_MEDIA_PLAY_PAUSE = 3;
const KEY_MEDIA_PREV_TRACK = 4;
const KEY_MEDIA_NEXT_TRACK = 5;
const KEY_BACK = 6;
const KEY_FORWARD = 7;
const KEY_FULLSCREEN = 8;
const KEY_INFO = 9;

const KEY_LEFT = 16;
const KEY_RIGHT = 17;
const KEY_UP = 18;
const KEY_DOWN = 19;
const KEY_CLICK = 20;


let ws;
let timerid;
let authenticated = false;
let pong = false;

function ping(){
	function pong_() {
		if (!pong){
			init();
		};
		pong=false;
	};

	if (ws.readyState==1){
		ws.send('ping');
	}
	setTimeout(pong_, 5000);
}

function init(){
	let opening = document.getElementById("opening");
	let closed = document.getElementById("closed");
	let keys = document.getElementById("keys");

	showScene(opening);

	function showScene(scene) {
		[opening, closed, keys].forEach(function(e) {
			e.classList.toggle("hidden", e != scene);
		});
	}
	if (ws) {
		ws.close();
	};

	ws = new WebSocket("ws://"+window.location.hostname+':'+(+window.location.port+1)+'/ws');
	ws.onmessage = function(evt) {
		if (evt.data=='pong') {
			pong = true;
		};
		clearTimeout(timerid)
		authenticated = true;
		showScene(keys)
	};
	ws.onclose = function() {
		authenticated = false;
		showScene(closed);
	};

	[
		{id: "back", key: KEY_BACK},
		{id: "fullscreen", key: KEY_FULLSCREEN},
		{id: "forward", key: KEY_FORWARD},
		{id: "prevtrackbutton", key: KEY_MEDIA_PREV_TRACK},
		{id: "playpausebutton", key: KEY_MEDIA_PLAY_PAUSE},
		{id: "nexttrackbutton", key: KEY_MEDIA_NEXT_TRACK},
		{id: "volumedownbutton", key: KEY_VOLUME_DOWN},
		{id: "volumemutebutton", key: KEY_VOLUME_MUTE},
		{id: "volumeupbutton", key: KEY_VOLUME_UP},
		{id: "infobutton", key: KEY_INFO},
		{id: "left", key: KEY_LEFT},
		{id: "right", key: KEY_RIGHT},
		{id: "up", key: KEY_UP},
		{id: "down", key: KEY_DOWN},
		{id: "click", key: KEY_CLICK},
	].forEach(function(o) {
		document.getElementById(o.id).addEventListener("click", function() {
			ws.send("k" + o.key);
		});
	});



};





window.addEventListener("load", function() {

	init();
//	setInterval(init, 5000);

	setInterval(ping, 5000);

	window.onpopstate = function() {
		showScene(keys)
	};
	document.getElementById("reloadbutton").addEventListener("click", function() {
		location.reload();
	});
});
