PREFIX = /usr

all:

install:
	mkdir -p ${DESTDIR}${PREFIX}/bin
	mkdir -p ${DESTDIR}${PREFIX}/share/applications
	mkdir -p ${DESTDIR}${PREFIX}/share/deepin-screenshot
	cp -r image sound src ${DESTDIR}${PREFIX}/share/deepin-screenshot
	cp deepin-screenshot.desktop ${DESTDIR}${PREFIX}/share/applications
	ln -s ${PREFIX}/share/deepin-screenshot/src/main.py ${DESTDIR}${PREFIX}/bin/deepin-screenshot
