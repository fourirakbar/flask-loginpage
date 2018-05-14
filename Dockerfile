# FROM fourirakbar/mitmproxy-oing:version3
# MAINTAINER Fourir Akbar <fourir.akbar@gmail.com>
# ENV LANG en_US.UTF-8
# WORKDIR /root
# # ARG MY_RUN_COMMAND=
# # ENTRYPOINT [ "mitmdump --mode Transparent --showhost --set client_certs=~/.mitimproxy -w cok -p 49155" ] 

 FROM alpine:3.4

 RUN apk update
 RUN apk add vim
 RUN apk add git