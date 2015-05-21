from flask import Flask, render_template, request
from flask_sockets import Sockets
import json
import yaml
import traceback

app = Flask('pp')
app.debug = True
socket = Sockets(app)

devs = {
};

socks = {
}

@app.route('/')
def home():
	return render_template('home.html')

@socket.route('/poker')
def bid(ws):
	print("connecting..." + str(len(socks)))
	socks.append(ws)

	try:
		while True:
			text = ws.receive()
			if text is None:
				break

			print("text: " + text)
			msg = json.loads(text)
			
			if msg['action'] == 'register':
				devs[msg['name']] = 0
				for sock in socks:
					try:
						print("sending to socket...")
						sock.send(json.dumps(devs.items()))
					except Exception as e:
						print("register error")
						print(e)
						traceback.print_exc()

			elif msg['action'] == 'bid':
				devs[msg['name']] = int(msg['number'])
				for sock in socks:
					try:
						sock.send(json.dumps(devs.items()))
					except Exception as e:
						print("bid error")
						print(e)
						traceback.print_exc()
	except Exception as e:
		print('top level exception');
		print(e)
		traceback.print_exc()



