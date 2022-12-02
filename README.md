
# MiTV

This project is a complete "drive" like system for photos and videos.  
It has been intended for Dockerization on an OpenMediaVault NAS, and the public shared folders are the one available through this system.  
The frontend consists of a website to access the drive's content in a user friendly way.  
The backend has a storage API but it also generates useful media metadata.  

## Features

• Face recognition  
• Image similarity detection and grouping  
• Image conversion and compression (JPEG)  
• Video thumbnailization and compression (AV1)  
• Pre-treatment for optimization 

## Documentation

[Documentation](https://github.com/liamLatour/MiTV/wiki)

## Manual installation without docker

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

Install MiTV backend with Python and install the metadata module

```bash
  cd mi_tv_backend
  pip install -r requirements.txt
  pip install ./image_metadata
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
