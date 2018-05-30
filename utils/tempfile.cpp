/*
 * Copyright (C) 2017 ~ 2018 Deepin Technology Co., Ltd.
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

TempFile* TempFile::instance() {
    static TempFile* tempFile = new TempFile;
    return tempFile;
}

TempFile::TempFile(QObject *parent)
    : QObject(parent)
{
}

TempFile::~TempFile() {
}

void TempFile::setFullScreenPixmap(const QPixmap &pixmap)
{
    m_fullscreenPixmap = pixmap;
}

void TempFile::setBlurPixmap(const QPixmap &pixmap)
{
    m_blurPixmap = pixmap;
}

void TempFile::setMosaicPixmap(const QPixmap &pixmap)
{
    m_mosaicPixmap = pixmap;
}
