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
RUN mkdir -p /media/people_ref /media/photos && chown -R user:picvol /media

# Tensorflow dependency folder
RUN mkdir -p /usr/local/image_metadata && chown -R user:picvol /usr/local/image_metadata

# Change to user
USER user
WORKDIR /home/user

# Python ENV
ENV PATH="${PATH}:/home/user/.local/bin"

# Get MiTV
RUN git clone "https://github.com/liamLatour/MiTV.git"
RUN cd MiTV/mi_tv_backend && pip install cmake
RUN cd MiTV/mi_tv_backend && pip install -r requirements.txt
RUN cd MiTV/mi_tv_backend && pip install ./image_metadata

# Symlinks for medias
RUN ln -s /media/people_ref /home/user/MiTV/mi_tv_backend/ && ln -s /media/photos /home/user/MiTV/mi_tv_backend/

# Tensorflow
RUN cp -R MiTV/mi_tv_backend/image_metadata/image_metadata/efficientnet_lite0_feature-vector_2 /usr/local/image_metadata/

# Video processor
RUN wget https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-linux64-gpl.tar.xz
RUN tar -xf ffmpeg-master-latest-linux64-gpl.tar.xz && mv /home/user/ffmpeg-master-latest-linux64-gpl/bin/* /home/user/.local/bin/

# Set CMD to start the front-end
CMD cd MiTV/mi_tv_backend && meta_data_creation --prerun --continuous --immediate ./people_ref ./photos