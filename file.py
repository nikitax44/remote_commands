#!/usr/bin/env python3
from flask import Flask, send_from_directory, redirect
app=Flask(__name__)

@app.route('/')
def root():
	return redirect('/main.html')

@app.route('/<path>')
def render(path):
	return send_from_directory('web', path)

if __name__=='__main__':
	app.run(host='0.0.0.0',port=8080)
