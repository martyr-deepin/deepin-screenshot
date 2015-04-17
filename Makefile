PREFIX = /usr

all:
	deepin-generate-mo locale/locale_config.ini
install:
	mkdir -p ${DESTDIR}${PREFIX}/bin
	mkdir -p ${DESTDIR}${PREFIX}/share/locale
	mkdir -p ${DESTDIR}${PREFIX}/share/applications
	mkdir -p ${DESTDIR}${PREFIX}/share/deepin-screenshot
	cp -r image sound src ${DESTDIR}${PREFIX}/share/deepin-screenshot
	cp deepin-screenshot.desktop ${DESTDIR}${PREFIX}/share/applications
	cp -r locale/mo/* ${DESTDIR}${PREFIX}/share/locale/
	ln -s ${PREFIX}/share/deepin-screenshot/src/main.py ${DESTDIR}${PREFIX}/bin/deepin-screenshot
