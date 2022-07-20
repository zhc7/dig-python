### Miniconda base image ###
# Taken from https://github.com/ContinuumIO/docker-images/blob/af4978ee1ebf0bfc4b5db4a1e81ef17909193829/miniconda3/debian/Dockerfile

FROM debian:bullseye-slim

ENV LANG=C.UTF-8 LC_ALL=C.UTF-8

# hadolint ignore=DL3008
RUN apt-get update -q && \
    apt-get install -q -y --no-install-recommends \
        bzip2 \
        ca-certificates \
        git \
        libglib2.0-0 \
        libsm6 \
        libxext6 \
        libxrender1 \
        mercurial \
        openssh-client \
        procps \
        subversion \
        wget \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

ENV PATH /opt/conda/bin:$PATH

# Leave these args here to better use the Docker build cache
# Python 3.7 needed
ARG CONDA_VERSION="py37_4.12.0"

RUN set -x && \
    UNAME_M="$(uname -m)" && \
    if [ "${UNAME_M}" = "x86_64" ]; then \
        MINICONDA_URL="https://repo.anaconda.com/miniconda/Miniconda3-${CONDA_VERSION}-Linux-x86_64.sh"; \
        SHA256SUM="4dc4214839c60b2f5eb3efbdee1ef5d9b45e74f2c09fcae6c8934a13f36ffc3e"; \
    elif [ "${UNAME_M}" = "s390x" ]; then \
        MINICONDA_URL="https://repo.anaconda.com/miniconda/Miniconda3-${CONDA_VERSION}-Linux-s390x.sh"; \
        SHA256SUM="8401eb61094297cc53709fec4654695d59652b3adde241963d3d993a6d760ed5"; \
    elif [ "${UNAME_M}" = "aarch64" ]; then \
        MINICONDA_URL="https://repo.anaconda.com/miniconda/Miniconda3-${CONDA_VERSION}-Linux-aarch64.sh"; \
        SHA256SUM="47affd9577889f80197aadbdf1198b04a41528421aaf0ec1f28b04a50b9f3ab8"; \
    elif [ "${UNAME_M}" = "ppc64le" ]; then \
        MINICONDA_URL="https://repo.anaconda.com/miniconda/Miniconda3-${CONDA_VERSION}-Linux-ppc64le.sh"; \
        SHA256SUM="c99b66a726a5116f7c825f9535de45fcac9e4e8ae825428abfb190f7748a5fd0"; \
    fi && \
    wget "${MINICONDA_URL}" -O miniconda.sh -q && \
    echo "${SHA256SUM} miniconda.sh" > shasum && \
    if [ "${CONDA_VERSION}" != "latest" ]; then sha256sum --check --status shasum; fi && \
    mkdir -p /opt && \
    sh miniconda.sh -b -p /opt/conda && \
    rm miniconda.sh shasum && \
    ln -s /opt/conda/etc/profile.d/conda.sh /etc/profile.d/conda.sh && \
    echo ". /opt/conda/etc/profile.d/conda.sh" >> ~/.bashrc && \
    echo "conda activate base" >> ~/.bashrc && \
    find /opt/conda/ -follow -type f -name '*.a' -delete && \
    find /opt/conda/ -follow -type f -name '*.js.map' -delete && \
    /opt/conda/bin/conda clean -afy

### Project-specific content ###

WORKDIR /usr/src

# Install dependencies
ADD conda-env.yml ./

RUN conda env update -f conda-env.yml --prune -n base && \
    conda clean -ay

# Add source
ADD game.py model.py trainer.py flask_server.py ./

ENV FLASK_APP=flask_server.py

ENTRYPOINT ["flask", "run", "-h", "0.0.0.0", "-p", "80"]

EXPOSE 80

# Add model
# To save space, the path to the model is hard-coded.
# Please update this line when a new model is available.
ADD models/model1603714489.h5 models/
