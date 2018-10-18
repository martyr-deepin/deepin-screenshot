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

#ifndef TEMPFILE_H
#define TEMPFILE_H

#include <QObject>
#include <QWindow>

class TempFile : public QObject {
    Q_OBJECT
public:
    static TempFile *instance();

public slots:
    inline const QPixmap getFullscreenPixmap() const { return m_fullscreenPixmap; }
    inline const QPixmap getMosaicPixmap() const { return m_mosaicPixmap; }
    inline const QPixmap getBlurPixmap() const { return m_blurPixmap; }

    void setFullScreenPixmap(const QPixmap &pixmap);
    void setBlurPixmap(const QPixmap &pixmap);
    void setMosaicPixmap(const QPixmap &pixmap);

private:
     TempFile(QObject* parent = 0);
     ~TempFile();

     QPixmap m_fullscreenPixmap;
     QPixmap m_mosaicPixmap;
     QPixmap m_blurPixmap;
};
#endif // TEMPFILE_H
