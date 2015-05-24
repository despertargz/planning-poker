from flask import Flask, render_template, request, session, make_response
from flask_sockets import Sockets
import json
import yaml
import traceback

app = Flask('pp')
app.debug = True
app.secret_key = 'secret'
socket = Sockets(app)

devs = {
}

class Dev():
	def __init__(self):
		self.bid = 0
		self.status = 1


def display(retry=True):
	for dev in devs.values():
		print(dev)

	display_devs = []
	for (poker_id, dev) in devs.items():
		display_devs.append((poker_id, dev.bid))

	devs_json = json.dumps(display_devs)

	player_died = False 
	for poker_id in devs.keys():
		print("sending to socket...")
		try:
			print("devs json: " + devs_json)
			dev = devs[poker_id]
			if hasattr(dev, 'socket'):
				dev.socket.send(devs_json)

		except Exception as e:
			print("socket send error error")
			print(e)
			del devs[poker_id]
			player_died = True
	
	if player_died and retry:
		display(False)
		


@app.route('/')
def home():
	#todo: will be generated uuid
	poker_id = request.args.get('poker_id')
	devs[poker_id] = Dev()

	response = make_response(render_template('home.html'))
	response.set_cookie('poker_id', poker_id)
	return response

@socket.route('/poker')
def bid(ws):

	try:
		while True:
			text = ws.receive()
			if text is None:
				break

			print("text: " + text)
			msg = json.loads(text)
			
			if msg['action'] == 'register':
				devs[msg['poker_id']].socket = ws
				display()

			elif msg['action'] == 'bid':
				devs[msg['poker_id']].bid = int(msg['number'])
				display()

			elif msg['action'] == 'clear':
				for poker_id in devs:
					devs[poker_id].bid = 0

				display()

	except Exception as e:
		print('top level exception');
		print(e)
		traceback.print_exc()



