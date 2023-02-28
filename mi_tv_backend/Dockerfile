# Base image
FROM python:3.10.8

# Create a user and give it permissions
RUN useradd -ms /bin/bash user
RUN apt -y update
RUN apt -y install sudo
RUN usermod -aG sudo user
RUN passwd -d user

# Permissions for picture folders
VOLUME /media
RUN groupadd -r picvol && usermod -aG picvol user
RUN mkdir -p /media && chown -R user:picvol /media

# Change to user
USER user
WORKDIR /home/user

# Python ENV
ENV PATH="${PATH}:/home/user/.local/bin"

# Get MiTV
RUN git clone "https://github.com/liamLatour/MiTV.git"
RUN cd MiTV/mi_tv_backend && python -m pip install cmake
RUN cd MiTV/mi_tv_backend && python -m pip install -r requirements.txt
RUN cd MiTV/mi_tv_backend && python -m pip install ./image_metadata

# Symlinks for medias
RUN mkdir -p /media/people_ref /media/photos
RUN ln -s /media/people_ref /home/user/MiTV/mi_tv_backend/ && ln -s /media/photos /home/user/MiTV/mi_tv_backend/

# Port for front-end
EXPOSE 5000

# Set CMD to start the front-end
CMD cd MiTV/mi_tv_backend && waitress-serve --port=5000 api_server:app