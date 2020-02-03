########    builder     ########
FROM ubuntu:18.04 as builder

ENV HOME=/root
ENV LIBSODIUM=libsodium-1.0.18
ENV SSR=shadowsocksr-3.2.2

COPY sources.list /etc/apt/sources.list
COPY lib/${SSR}.tar.gz ${HOME}/${SSR}.tar.gz
# install libsodium
COPY lib/${LIBSODIUM}.tar.gz /tmp/${LIBSODIUM}.tar.gz
RUN apt update && \
    apt install -y build-essential && \
    # prepare source code
    tar -xzf /tmp/${LIBSODIUM}.tar.gz -C /tmp && \
    cd /tmp/${LIBSODIUM} && \
    # configure and build
    ./configure && \
    make && make install && \
    # untar ssr
    tar -xzf ${HOME}/${SSR}.tar.gz -C ${HOME}

######## main docker file ########

FROM ubuntu:18.04

ENV HOME=/root
ENV LIBSODIUM=libsodium-1.0.18
ENV SSR=shadowsocksr-3.2.2

WORKDIR ${HOME}

# accelerate apt
COPY                sources.list                /etc/apt/sources.list
# make default config
COPY                config/default.json         /config/config.json
COPY                entry.sh                    entry.sh
COPY --from=builder ${HOME}/${SSR}              ${HOME}/${SSR}
COPY --from=builder /usr/local/lib/libsodium*   /usr/local/lib/


# install ssr
RUN apt update && \
    apt install -y python3-minimal

CMD [ "/root/entry.sh" ]
