PREFIX = /usr

all:

install:
	mkdir -p ${DESTDIR}${PREFIX}/bin
	mkdir -p ${DESTDIR}${PREFIX}/share/applications
	mkdir -p ${DESTDIR}${PREFIX}/share/deepin-screenshot-v3
	cp -r image sound src theme ${DESTDIR}${PREFIX}/share/deepin-screenshot-v3
	cp deepin-screenshot-v3.desktop ${DESTDIR}${PREFIX}/share/applications
	ln -s ${PREFIX}/share/deepin-screenshot-v3/src/main.py ${DESTDIR}${PREFIX}/bin/deepin-screenshot-v3
