from flask import Flask, render_template, request
from flask_sockets import Sockets
import json
import yaml

app = Flask('pp')
app.debug = True
socket = Sockets(app)

devs = {
};

socks = []

@app.route('/')
def home():
	return render_template('home.html')

@socket.route('/poker')
def bid(ws):
	socks.append(ws)

	while True:
		text = ws.receive()
		print("text: " + text)
		msg = json.loads(text)
		
		if msg['action'] == 'register':
			devs[msg['name']] = 0
			for sock in socks:
				sock.send(json.dumps(devs))

		elif msg['action'] == 'bid':
			devs[msg['name']] = int(msg['number'])
			for sock in socks:
				sock.send(json.dumps(devs))



