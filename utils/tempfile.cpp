/*
 * Copyright (C) 2017 ~ 2017 Deepin Technology Co., Ltd.
 *
 * Maintainer: Peng Hui<penghui@deepin.com>
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

#include "tempfile.h"

#include <QTemporaryFile>
#include <QDebug>

TempFile* TempFile::m_tempFile = nullptr;
TempFile* TempFile::instance() {
    if (!m_tempFile) {
        m_tempFile = new TempFile();
    }

    return m_tempFile;
}

TempFile::TempFile(QObject *parent)
    : QObject(parent) {
    QTemporaryFile tmpFile;
    if (tmpFile.open()) {
        m_tmpFile = tmpFile.fileName();
    }

    QTemporaryFile fullscreenFile;
    if (fullscreenFile.open()) {
        m_fullscreenFile = fullscreenFile.fileName();
    }

    QTemporaryFile mosaicFile;
    if (mosaicFile.open()) {
        m_mosaicFile = mosaicFile.fileName();
    }

    QTemporaryFile blurFile;
    if (blurFile.open()) {
        m_blurFile = blurFile.fileName();
    }
    qDebug() << "ssss" << m_fullscreenFile;
}

TempFile::~TempFile() {}

QString TempFile::getTmpFileName() {
    if (!m_tmpFile.isEmpty()) {
        return QString("%1.png").arg(m_tmpFile);
    } else {
        return "/tmp/deepin-screenshot.png";
    }
}

QString TempFile::getFullscreenFileName() {
    if (!m_fullscreenFile.isEmpty()) {
        return QString("%1.png").arg(m_fullscreenFile);
    } else {
        return "/tmp/deepin-screenshot-fullscreen.png";
    }
}

QString TempFile::getMosaicFileName() {
    if (!m_mosaicFile.isEmpty()) {
        return QString("%1.png").arg(m_mosaicFile);
    } else {
        return "/tmp/deepin-screenshot-mosa.png";
    }
}

QString TempFile::getBlurFileName() {
    if (!m_blurFile.isEmpty()) {
        return QString("%1.png").arg(m_blurFile);
    } else {
        return "/tmp/deepin-screenshot-blur.png";
    }
}
