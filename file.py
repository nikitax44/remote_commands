#!/usr/bin/env python3
'''
file server: server serving static files
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
