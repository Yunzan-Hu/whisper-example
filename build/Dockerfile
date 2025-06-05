#FROM conda/miniconda3:24.5.0
FROM python:3.9-slim

# Install system dependencies for Conda and faster-whisper
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    bzip2 \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Define CONDA_DIR
ENV CONDA_DIR=/opt/conda

# Download and install Miniconda
RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-py39_23.5.2-0-Linux-x86_64.sh -O /tmp/miniconda.sh && \
    /bin/bash /tmp/miniconda.sh -b -p $CONDA_DIR && \
    rm /tmp/miniconda.sh && \
    $CONDA_DIR/bin/conda clean --all --yes && \
    ln -s $CONDA_DIR/bin/conda /usr/local/bin/conda && \
    ln -s $CONDA_DIR/bin/activate /usr/local/bin/activate

# Initialize Conda in bash
RUN echo ". $CONDA_DIR/etc/profile.d/conda.sh" >> ~/.bashrc && \
    /opt/conda/bin/conda init bash

RUN /usr/local/bin/pip install faster-whisper fastapi uvicorn python-multipart
RUN /usr/local/bin/conda install cudnn -y

WORKDIR /opt/whisper

#download model
RUN pip install modelscope && \
    modelscope download Systran/faster-whisper-tiny --local_dir /opt/whisper/models/Systran-faster-whisper-tiny && \
    modelscope download Systran/faster-whisper-base --local_dir /opt/whisper/models/Systran-faster-whisper-base && \
    modelscope download Systran/faster-whisper-small --local_dir /opt/whisper/models/Systran-faster-whisper-small && \
    modelscope download Systran/faster-whisper-medium --local_dir /opt/whisper/models/Systran-faster-whisper-medium && \
    modelscope download Systran/faster-whisper-large-v3 --local_dir /opt/whisper/models/Systran-faster-whisper-large-v3

COPY ../src/*.py ./

ENV PORT=8000
EXPOSE 8000

ENTRYPOINT ["/opt/conda/bin/python3"]
CMD ["/opt/whisper/server.py"]