FROM python:3.6
LABEL author="binux <roy@binux.me>"
LABEL version="1.0"
LABEL description="Docker image for running"

# install phantomjs
# RUN mkdir -p /opt/phantomjs \
#         && cd /opt/phantomjs \
#         && wget -O phantomjs.tar.bz2 https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-2.1.1-linux-x86_64.tar.bz2 \
#         && tar xavf phantomjs.tar.bz2 --strip-components 1 \
#         && ln -s /opt/phantomjs/bin/phantomjs /usr/local/bin/phantomjs \
#         && rm phantomjs.tar.bz2
WORKDIR /opt/phantomjs
COPY phantomjs-2.1.1-linux-x86_64.tar.bz2 phantomjs.tar.bz2
RUN tar xavf phantomjs.tar.bz2 --strip-components 1 \
        && ln -s /opt/phantomjs/bin/phantomjs /usr/local/bin/phantomjs \
        && rm phantomjs.tar.bz2
# Fix Error: libssl_conf.so: cannot open shared object file: No such file or directory
ENV OPENSSL_CONF=/etc/ssl/

# install nodejs
# ENV NODEJS_VERSION=8.15.0 \
#     PATH=$PATH:/opt/node/bin
# WORKDIR /opt/node
# RUN apt-get -qq update && apt-get -qq install -y curl ca-certificates libx11-xcb1 libxtst6 libnss3 libasound2 libatk-bridge2.0-0 libgtk-3-0 --no-install-recommends && \
#     curl -sL https://nodejs.org/dist/v${NODEJS_VERSION}/node-v${NODEJS_VERSION}-linux-x64.tar.gz | tar xz --strip-components=1 && \
#     rm -rf /var/lib/apt/lists/*
# RUN npm install puppeteer express
# ENV PATH=$PATH:/opt/node/bin
# WORKDIR /opt/node
# COPY node-v8.15.0-linux-x64.tar.gz node-v8.15.0-linux-x64.tar.gz
# RUN tar -zxvf node-v8.15.0-linux-x64.tar.gz --strip-components=1 && \
#     npm config set registry https://registry.npm.taobao.org && \
#     npm config set electron_mirror https://npm.taobao.org/mirrors/electron/ && \
#     npm config set sass_binary_site https://npm.taobao.org/mirrors/node-sass/ && \
#     npm config set phantomjs_cdnurl https://npm.taobao.org/mirrors/phantomjs/ && \
#     npm install puppeteer@1.15.0 && \
#     npm install express@4.18.2

RUN mv /etc/apt/sources.list /etc/apt/sources.list.bakevan && \    
    echo "deb https://mirrors.aliyun.com/debian/ stretch main non-free contrib" >>/etc/apt/sources.list && \
    echo "deb-src https://mirrors.aliyun.com/debian/ stretch main non-free contrib" >>/etc/apt/sources.list && \
    echo "deb https://mirrors.aliyun.com/debian-security stretch/updates main" >>/etc/apt/sources.list && \
    echo "deb-src https://mirrors.aliyun.com/debian-security stretch/updates main" >>/etc/apt/sources.list && \
    echo "deb https://mirrors.aliyun.com/debian/ stretch-updates main non-free contrib" >>/etc/apt/sources.list && \
    echo "deb-src https://mirrors.aliyun.com/debian/ stretch-updates main non-free contrib" >>/etc/apt/sources.list && \
    echo "deb https://mirrors.aliyun.com/debian/ stretch-backports main non-free contrib" >>/etc/apt/sources.list && \
    echo "deb-src https://mirrors.aliyun.com/debian/ stretch-backports main non-free contrib" >>/etc/apt/sources.list 
RUN apt-get clean && apt-get update && apt-get install -y curl ca-certificates libx11-xcb1 libxtst6 libnss3 libasound2 libatk-bridge2.0-0 libgtk-3-0 --no-install-recommends && \ 
    rm -rf /var/lib/apt/lists/* 

# install requirements
COPY requirements.txt /opt/pyspider/requirements.txt
RUN pip config set global.index-url http://mirrors.aliyun.com/pypi/simple && \
    pip config set install.trusted-host mirrors.aliyun.com && \
    python -m pip install --upgrade pip && \
    pip install -r /opt/pyspider/requirements.txt

# add all repo
ADD ./ /opt/pyspider

# run test
WORKDIR /opt/pyspider
RUN pip install -e .[all]

# Create a symbolic link to node_modules
RUN ln -s /opt/node/node_modules ./node_modules

#VOLUME ["/opt/pyspider"]
ENTRYPOINT ["pyspider"]

EXPOSE 5000 23333 24444 25555 22222
