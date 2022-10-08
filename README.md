# MiTV

## Frontend is written in Flutter (dart)
#To run it:
  - flutter run
#To build it:
  - flutter build web --release -v

##Backend is in python (flask)
#To run it in debug mode:
  - install requirements.txt (in a venv preferably)
  - launch server.py
  
#To run it in production mode (still local):
  - waitress-serve --host 127.0.0.1 --port=5000 server:app
