FROM python:3.9-slim

# Install system dependencies for Conda and faster-whisper
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    bzip2 \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Define CONDA_DIR
ENV CONDA_DIR=/opt/conda
ENV PATH=$CONDA_DIR/bin:$PATH

# Download and install Miniconda
RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-py39_23.5.2-0-Linux-x86_64.sh -O /tmp/miniconda.sh && \
    /bin/bash /tmp/miniconda.sh -b -p $CONDA_DIR && \
    rm /tmp/miniconda.sh && \
    $CONDA_DIR/bin/conda clean --all --yes

# 使用 conda 安装所有 Python 包
RUN conda install -y -c conda-forge \
    fastapi \
    uvicorn \
    python-multipart \
    cudnn \
    && conda clean --all -y

# 使用 pip 安装不在 conda 中的包
RUN pip install faster-whisper modelscope

WORKDIR /opt/whisper

# download model
RUN modelscope download Systran/faster-whisper-tiny --local_dir /opt/whisper/models/Systran-faster-whisper-tiny && \
    modelscope download Systran/faster-whisper-base --local_dir /opt/whisper/models/Systran-faster-whisper-base && \
    modelscope download Systran/faster-whisper-small --local_dir /opt/whisper/models/Systran-faster-whisper-small && \
    modelscope download Systran/faster-whisper-medium --local_dir /opt/whisper/models/Systran-faster-whisper-medium && \
    modelscope download Systran/faster-whisper-large-v3 --local_dir /opt/whisper/models/Systran-faster-whisper-large-v3

COPY ../src/server.py /opt/whisper

ENV PORT=8000
EXPOSE 8000

ENTRYPOINT ["/opt/conda/bin/python3"]
CMD ["/opt/whisper/server.py"]