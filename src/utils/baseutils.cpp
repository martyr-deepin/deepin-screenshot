/*
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

#include "baseutils.h"

#include <QPixmap>
#include <QProcess>
#include <QLayoutItem>
#include <QFile>
#include <QApplication>
#include <QDebug>
#include <QIcon>

const QSize START_SIZE = QSize(15, 15);
const QSize RECT_SIZE = QSize(22, 26);
const QSize ARROW_SIZE = QSize(24, 24);
const QSize TEXT_SIZE = QSize(11, 23);
const QSize COLORPEN_SIZE = QSize(25, 25);

QCursor setCursorShape(QString cursorName, int colorIndex) {
    QCursor customShape = QCursor();
    qreal ration = qApp->devicePixelRatio();

    if (cursorName == "start") {
        QPixmap startPix;
        if (ration <= 1)
        {
            startPix = QIcon(":/image/mouse_style/shape/start_mouse.svg").pixmap(START_SIZE);
            customShape = QCursor(startPix, 8, 8);
        } else
        {
            startPix = QIcon(":/image/mouse_style/shape/start_mouse@2x.svg").pixmap(START_SIZE);
            customShape = QCursor(startPix, int(8*ration), int(8*ration));
        }

    } else if (cursorName == "rotate") {
        QPixmap rotateCursor  = QIcon(":/image/mouse_style/shape/rotate_mouse.svg").pixmap(ARROW_SIZE);
        rotateCursor.setDevicePixelRatio(ration);

        customShape = QCursor(rotateCursor, int(10*ration), int(10*ration));
    } else if (cursorName == "rectangle") {
        QPixmap rectCursor  = QIcon(":/image/mouse_style/shape/rect_mouse.svg").pixmap(RECT_SIZE);
        rectCursor.setDevicePixelRatio(ration);

        customShape = QCursor(rectCursor, 0, int(1*ration));
    } else if (cursorName == "oval") {
        QPixmap ovalCursor  = QIcon(":/image/mouse_style/shape/ellipse_mouse.svg").pixmap(RECT_SIZE);
        ovalCursor.setDevicePixelRatio(ration);

        customShape = QCursor(ovalCursor, 0, int(1*ration));
    } else if (cursorName == "arrow") {
        QPixmap arrowCursor  = QIcon(":/image/mouse_style/shape/arrow_mouse.svg").pixmap(ARROW_SIZE);
        arrowCursor.setDevicePixelRatio(ration);

        customShape = QCursor(arrowCursor, int(5*ration), int(5*ration));
    } else if (cursorName == "text") {
        QPixmap textCursor  = QIcon(":/image/mouse_style/shape/text_mouse.svg").pixmap(TEXT_SIZE);
        textCursor.setDevicePixelRatio(ration);

        customShape = QCursor(textCursor, int(5*ration), int(5*ration));
    } else if  (cursorName == "line") {
        QPixmap colorPic = QIcon(QString(":/image/mouse_style/"
            "color_pen/color%1.svg").arg(colorIndex)).pixmap(COLORPEN_SIZE);
        colorPic.setDevicePixelRatio(ration);

        customShape = QCursor(colorPic,  int(5*ration), int(22*ration));
    } else if (cursorName == "straightLine") {
        QPixmap lineCursor  = QIcon(":/image/mouse_style/shape/line_mouse.svg").pixmap(ARROW_SIZE);
        lineCursor.setDevicePixelRatio(ration);

        customShape = QCursor(lineCursor, int(2*ration), int(9*ration));
    }

    return customShape;
}

int stringWidth(const QFont &f, const QString &str)
{
    QFontMetrics fm(f);
    return fm.boundingRect(str).width();
}

QString getFileContent(const QString &file)
{
    QFile f(file);
    QString fileContent = "";
    if (f.open(QFile::ReadOnly))
    {
        fileContent = QLatin1String(f.readAll());
        f.close();
    }
    return fileContent;
}

QColor colorIndexOf(int index)
{
    switch(index) {
    case 0: { return QColor("#ffd903");}
    case 1: { return QColor("#ff5e1a");}
    case 2: { return QColor("#ff3305");}
    case 3: { return QColor("#ff1c49");}
    case 4: { return QColor("#fb00ff");}
    case 5: { return QColor("#7700ed");}
    case 6: { return QColor("#3d08ff");}
    case 7: { return QColor("#3467ff");}
    case 8: { return QColor("#00aaff");}
    case 9: { return QColor("#08ff77");}
    case 10: { return QColor("#03a60e");}
    case 11: { return QColor("#3c7d00");}
    case 12: { return QColor("#ffffff");}
    case 13: { return QColor("#666666");}
    case 14: { return QColor("#2b2b2b");}
    case 15: { return QColor("#000000");}
    default:  {return QColor("#ffd903");}
    }

    return QColor("#ffd903");
}

int colorIndex(QColor color)
{
    QList<QColor> colorList;
    colorList.append(QColor("#ffd903"));
    colorList.append(QColor("#ff5e1a"));
    colorList.append(QColor("#ff3305"));
    colorList.append(QColor("#ff1c49"));
    colorList.append(QColor("#fb00ff"));
    colorList.append(QColor("#7700ed"));
    colorList.append(QColor("#3d08ff"));
    colorList.append(QColor("#3467ff"));
    colorList.append(QColor("#00aaff"));
    colorList.append(QColor("#08ff77"));
    colorList.append(QColor("#03a60e"));
    colorList.append(QColor("#3c7d00"));
    colorList.append(QColor("#ffffff"));
    colorList.append(QColor("#666666"));
    colorList.append(QColor("#2b2b2b"));
    colorList.append(QColor("#000000"));
    return colorList.indexOf(color);
}

bool          isValidFormat(QString suffix) {
    QStringList validFormat;
    validFormat << "bmp" << "jpg" << "jpeg" << "png" << "pbm" << "pgm" << "xbm" << "xpm";
    if (validFormat.contains(suffix)) {
        return true;
    } else {
        return false;
    }
}

bool          isCommandExist(QString command) {
    QProcess* proc = new QProcess;
    QString cm = QString("which %1\n").arg(command);
    proc->start(cm);
    proc->waitForFinished(1000);

    if (proc->exitCode() == 0) {
        return true;
    } else {
        return false;
    }
}

void   paintSelectedPoint(QPainter &painter, QPointF pos, QPixmap pointImg) {
    painter.drawPixmap(pos, pointImg);
}
