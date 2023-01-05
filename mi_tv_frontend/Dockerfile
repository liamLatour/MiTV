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

# Get MiTV
RUN git clone "https://github.com/liamLatour/MiTV.git"
RUN cd MiTV/mi_tv_frontend && npm i
RUN cd MiTV/mi_tv_frontend && npm run build

# Port for front-end
EXPOSE 5173

# Set CMD to start the front-end
CMD cd MiTV/mi_tv_frontend && npm run dev