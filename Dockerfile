FROM python:3.6.5-jessie

RUN echo 'deb http://httpredir.debian.org/debian jessie-backports main non-free' >> /etc/apt/sources.list && echo 'deb-src http://httpredir.debian.org/debian jessie-backports main non-free' >> /etc/apt/sources.list

RUN apt-get update

#install vcs to create contact sheets
RUN apt-get install -y wget mplayer ffmpeg bash sed grep coreutils imagemagick mediainfo

RUN wget http://p.outlyer.net/vcs/files/vcs_1.13.2-pon.1_all.deb && dpkg -i vcs_1.13.2-pon.1_all.deb

ADD pbay.conf  /usr/share/vcs/profiles/pbay.conf

RUN mkdir /video && mkdir /output
# finish install vcs

RUN mkdir /app

#install torrentHelper script first and make it available as "torrentHelper" in the container

ADD torrentHelper /app/torrentHelper

RUN pip3 install -r /app/torrentHelper/requirements.txt

RUN echo "#!/bin/sh " > /usr/local/bin/torrentHelper && echo 'python /app/torrentHelper/torrentHelper.py "$@" ' >> /usr/local/bin/torrentHelper && chmod +x /usr/local/bin/torrentHelper

#finish torrentHelper

# add pMetaLoad
ADD pMetaload /app/pMetaLoad

RUN pip3 install -r /app/pMetaLoad/requirements.txt

CMD ["python", "/app/pMetaLoad/main.py" ]