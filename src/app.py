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
	'buu': {
	},
	'cell': {
	}
}

class Dev():
	def __init__(self):
		self.bid = 0
		self.status = 1


def display(msg, retry=True):
	room_id = msg['room_id']

	display_devs = []
	for (user_id, dev) in devs[room_id].items():
		display_devs.append({ 'name': user_id, 'bid': dev.bid, 'status': dev.status })

	devs_json = json.dumps(display_devs)

	player_died = False 
	for (user_id,dev) in devs[room_id].items():
		print("sending to socket to ...")
		try:
			print("devs json: " + devs_json)
			if hasattr(dev, 'socket'):
				dev.socket.send(devs_json)

		except Exception as e:
			print("socket send error")
			print(e)
			del devs[room_id][user_id]
			player_died = True
	
	if player_died and retry:
		display(msg, False)
		


def get_dev(msg):
	room_id = msg['room_id']
	user_id = msg['user_id']
	return devs[room_id][user_id]
		

@app.route('/')
def home():
	#todo: will be generated uuid
	user_id = request.args.get('user_id')

	response = make_response(render_template('home.html'))
	response.set_cookie('user_id', user_id)
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
				user_id = msg['user_id']
				room_id = msg['room_id']
				dev = Dev()
				dev.socket = ws
				devs[room_id][user_id] = dev
				display(msg)

			elif msg['action'] == 'bid':
				dev = get_dev(msg)
				dev.bid = int(msg['number'])
				display(msg)

			elif msg['action'] == 'clear':
				room_id = msg['room_id']
				room = devs[room_id]
				for user_id in room:
					devs[room_id][user_id].bid = 0

				display(msg)

			elif msg['action'] == 'spectate':
				dev = get_dev(msg)
				dev.status = 2
				dev.bid = 0
				display(msg)

			elif msg['action'] == 'unspectate':
				dev = get_dev(msg)
				dev.status = 1 
				dev.bid = 0
				display(msg)

					
	except Exception as e:
		print('top level exception');
		print(e)
		traceback.print_exc()


#@app.route('/create_room')
#def create_room():
#	name = request.args.get('name')












