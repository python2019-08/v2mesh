FROM ubuntu:24.04

# 增加 ca-certificates 解决 git 证书问题
RUN apt-get update && apt-get install -y --no-install-recommends \
    git g++ build-essential cmake make zip unzip tar curl ca-certificates \
    pkg-config autoconf automake libtool linux-libc-dev libgl1-mesa-dev \
    python3-dev libpng-dev libjpeg-dev libtiff-dev libglu1-mesa-dev \
    libboost-iostreams-dev libboost-program-options-dev libboost-system-dev libboost-serialization-dev \
    libopencv-dev libcgal-dev libcgal-qt5-dev \
    libatlas-base-dev libsuitesparse-dev

WORKDIR /opt

# 建议分两步 RUN 方便利用 Docker 缓存，且增加重试配置
RUN git config --global http.postBuffer 524288000 && \
    git clone --depth 1 https://github.com/cdcseacave/VCG.git vcglib && \
    git clone --branch 3.4 --depth 1 https://gitlab.com/libeigen/eigen.git && \
    cd eigen && cmake -S. -B build && cmake --build build && \
    cmake --install build --prefix /opt/my_lib

RUN git clone https://github.com/cdcseacave/openMVS.git && \
    cd openMVS && \
    git checkout v2.3.0 && \
    git submodule update --init --recursive && \
    mkdir -p libs && mv /opt/vcglib libs/ && \
    mkdir build01 && cd build01 && \
    cmake .. -DCMAKE_BUILD_TYPE=Release \
             -DVCG_ROOT="/opt/openMVS/libs/vcglib" \
             -DEigen3_DIR="/opt/my_lib/share/eigen3/cmake" \
             -DCMAKE_CXX_FLAGS="-w" && \
    make -j$(nproc)
