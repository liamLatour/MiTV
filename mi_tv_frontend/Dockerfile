# Variable for port ENV
ARG port PORT

# Base image
FROM node:17

# Create a user and give it permissions
RUN useradd -ms /bin/bash user
RUN apt -y update
RUN apt -y install sudo
RUN usermod -aG sudo user

# Change to user
USER user
WORKDIR /home/user

# Python ENV
ENV PATH="${PATH}:/home/user/.local/bin"

# Get MiTV
RUN git clone "https://github.com/liamLatour/MiTV.git"
RUN cd MiTV/mi_tv_frontend && npm i

# Port for front-end
EXPOSE $port
ENV PORT="$port"

# Start the front-end
RUN cd MiTV/mi_tv_frontend && npm run build