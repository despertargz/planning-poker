from flask import Flask, render_template, request, session, make_response
from flask_sockets import Sockets
import json
import yaml
import traceback

app = Flask('pp')
app.debug = True
app.secret_key = 'secret'
socket = Sockets(app)

bids = {
};

socks = {
}

def display():
	for sock in socks.values():
		try:
			print("sending to socket...")
			sock.send(json.dumps(bids.items()))
		except Exception as e:
			print("register error")
			print(e)
			traceback.print_exc()
	


@app.route('/')
def home():
	#todo: will be generated uuid
	poker_id = request.args.get('poker_id')
	bids[poker_id] = 0

	response = make_response(render_template('home.html'))
	response.set_cookie('poker_id', poker_id)
	return response

@socket.route('/poker')
def bid(ws):
	print("connecting..." + str(len(socks)))

	try:
		while True:
			text = ws.receive()
			if text is None:
				break

			print("text: " + text)
			msg = json.loads(text)
			
			if msg['action'] == 'register':
				socks[msg['poker_id']] = ws
				display()

			elif msg['action'] == 'bid':
				bids[msg['poker_id']] = int(msg['number'])
				display()

			elif msg['action'] == 'clear':
				for poker_id in bids:
					bids[poker_id] = 0

				display()

	except Exception as e:
		print('top level exception');
		print(e)
		traceback.print_exc()



