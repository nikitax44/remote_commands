"use strict";
/*
web client: GUI in a web browser
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
*/

let ws;
let builded = false;


function builder(data){
	let keys=document.getElementById('keys');
	function add_element(el){
		while (keys.childElementCount<=el.pos.y) {
			let buf=document.createElement('div');
			buf.setAttribute('class', 'buttons');
			keys.appendChild(buf);
		};
		let hor=keys.children[el.pos.y];
		while (hor.childElementCount<=el.pos.x) {
			let buf=document.createElement('button');
			hor.appendChild(buf);
		};
		let elem=hor.children[el.pos.x];
		elem.setAttribute('id', el.keyName);
		elem.setAttribute('key_id', el.keyCode);
		elem.addEventListener("click", function() {
			ws.send("key " + el.keyCode);
		});

		elem.innerText=el.Name;
	};
	function remove_unused(block){
		function remove_unused_local(bt){
			if (bt.getAttribute('id')==undefined){
				bt.parentElement.removeChild(bt);
			};
		};

		Array.from(block.children).forEach(remove_unused_local)
	};
	data.forEach(add_element);
	Array.from(keys.children).forEach(remove_unused)
};

function init(){
	let opening = document.getElementById("opening");
	let closed = document.getElementById("closed");
	let keys = document.getElementById("keys");


	function showScene(scene) {
		[opening, closed, keys].forEach(function(e) {
			e.classList.toggle("hidden", e != scene);
		});
	};


	showScene(opening);

	function consume(data) {
		let buf=JSON.parse(data);
		builder(buf);
	};

	let resttimer=setTimeout(() => { // reload if connection is failsed
		location.reload();
	}, 10000);

	ws = new WebSocket("ws://"+window.location.hostname+':'+(+window.location.port+1)+'/ws');
	ws.onmessage = function(evt) {
		if (!builded){
			ws.send('get');
		};

		builded = true;
		clearTimeout(resttimer)
		showScene(keys);

		if (evt.data.trim()=='') {
			return;
		};
		if (evt.data[0]=='['){
			consume(evt.data);
		};
	};

	ws.onclose = function() {
		showScene(closed);
		location.reload();
	};
};



window.addEventListener("load", function() {

	init();

	window.onpopstate = function() {
		showScene(keys);
	};


	document.getElementById("reloadbutton").addEventListener("click", function() {
		location.reload();
	});
});
