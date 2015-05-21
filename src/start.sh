gunicorn -k flask_sockets.worker -b vps.sonyar.info:8000 app:app
