FROM ubuntu:22.04


ARG DEBIAN_FRONTEND=noninteractive


RUN apt update && apt install -y \
    python3 python3-pip \
    curl wget git htop nano unzip \
    net-tools iputils-ping \
    tmux screen neofetch \
    && apt clean


RUN pip3 install --no-cache-dir jupyter



RUN mkdir -p /app/notebooks


EXPOSE 8888


CMD ["bash", "-c", "neofetch && jupyter notebook --ip=0.0.0.0 --port=8888 --no-browser --allow-root"]
