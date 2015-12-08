PREFIX = /usr

all:
	deepin-generate-mo locale/locale_config.ini

install:
	mkdir -p ${DESTDIR}${PREFIX}/bin
	mkdir -p ${DESTDIR}${PREFIX}/share/locale
	mkdir -p ${DESTDIR}${PREFIX}/share/applications
	mkdir -p ${DESTDIR}${PREFIX}/share/icons/hicolor/scalable/apps
	mkdir -p ${DESTDIR}${PREFIX}/share/deepin-screenshot
	mkdir -p ${DESTDIR}${PREFIX}/share/dman/deepin-screenshot
	cp -r image src ${DESTDIR}${PREFIX}/share/deepin-screenshot
	cp -r doc/* ${DESTDIR}${PREFIX}/share/dman/deepin-screenshot/
	cp deepin-screenshot.desktop ${DESTDIR}${PREFIX}/share/applications
	cp deepin-screenshot.svg ${DESTDIR}${PREFIX}/share/icons/hicolor/scalable/apps
	cp -r locale/mo/* ${DESTDIR}${PREFIX}/share/locale/
	ln -s ${PREFIX}/share/deepin-screenshot/src/main.py ${DESTDIR}${PREFIX}/bin/deepin-screenshot
