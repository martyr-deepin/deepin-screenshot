#!/bin/bash

DESKTOP_SOURCE_FILE=deepin-screenshot.desktop
DESKTOP_TS_DIR=translations/desktop/

/usr/bin/deepin-desktop-ts-convert ts2desktop $DESKTOP_SOURCE_FILE $DESKTOP_TS_DIR $DESKTOP_SOURCE_FILE
