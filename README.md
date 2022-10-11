# MiTV

## Frontend is written in Vue Js
### To run it:
  - npm run dev
### To build it:
  - npm run build

## Backend is in python (flask)
### To run it in debug mode:
  - pip install -r requirements.txt
  - python api_server.py
### To run it in production mode (still local):
  - waitress-serve --host 127.0.0.1 --port=5000 api_server:app
