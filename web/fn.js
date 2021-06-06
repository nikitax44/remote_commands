"use strict";

let ws;
let timerid;
let builded = false;
let pong = false;

function ping(){
	function pong_checker() {
		if (!pong){
			location.reload();
		};
		pong=false;
	};

	if (ws.readyState==1){
		ws.send('ping');
	}
	setTimeout(pong_checker, 5000);
}

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

	if (ws) {
		ws.close();
	};

	showScene(opening);

	function consume(data) {
		let buf=JSON.parse(data);
		builder(buf);
		buf.forEach(function(e) {
			let buf_=document.getElementById(e.keyName);
			buf_.setAttribute('key_id', e.keyCode);
			buf_.addEventListener("click", function() {
				ws.send("key " + buf_.getAttribute('key_id'));
			});
		});
	};

	ws = new WebSocket("ws://"+window.location.hostname+':'+(+window.location.port+1)+'/ws');
	ws.onmessage = function(evt) {
		if (evt.data=='pong') {
			pong = true;
			return;
		};
		if (!builded){
			ws.send('get');
		};

		clearTimeout(timerid);
		builded = true;
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
	};
};



window.addEventListener("load", function() {

	init();

	setInterval(ping, 5000);

	window.onpopstate = function() {
		showScene(keys);
	};


	document.getElementById("reloadbutton").addEventListener("click", function() {
		location.reload();
	});
});
