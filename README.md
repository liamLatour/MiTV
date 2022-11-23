
# MiTV

This project is a complete 'drive' like system.  
The frontend is a website to access the drive's content in a user friendly way.  
The backend has a storage api but it also generates usefull metadata of the media.

## Features

- face recognition
- image similarity detection and grouping
- image conversion (to jpeg)
- video thumbnailization
- pre-treatment for optimization
## Documentation

[Documentation](https://github.com/liamLatour/MiTV/wiki)


## Installation

Start by cloning the repository

```bash
  git clone https://github.com/liamLatour/MiTV.git
  cd MiTV
```

Install MiTV frontend with npm

```bash
  cd mi_tv_frontend
  npm i
```

Install MiTV backend with python

```bash
  cd mi_tv_backend
  pip install -r requirements.txt
```
## Deployment

To deploy the frontend, first build it:

```bash
  npm run build
```

To deploy the backend run:

```bash
  waitress-serve --host 127.0.0.1 --port=5000 api_server:app
```

## Authors

- [@liamLatour](https://www.github.com/liamLatour)
- [@Sceeker](https://www.github.com/Sceeker)
