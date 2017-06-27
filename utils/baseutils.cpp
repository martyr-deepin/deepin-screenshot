#include "baseutils.h"

#include <QPixmap>
#include <QProcess>
#include <QLayoutItem>
#include <QFile>
#include <QDebug>

QCursor setCursorShape(QString cursorName, int colorIndex) {
    QCursor customShape = QCursor();
    if (cursorName == "start") {
        customShape = QCursor(QPixmap(
                      ":/image/mouse_style/shape/start_mouse.png"), 8, 8);
    } else if (cursorName == "rotate") {
        customShape = QCursor(QPixmap(
                      ":/image/mouse_style/shape/rotate_mouse.png"), 5, 5);
    } else if (cursorName == "rectangle") {
        customShape = QCursor(QPixmap(
                      ":/image/mouse_style/shape/rect_mouse.png"), 0, 4);
    } else if (cursorName == "oval") {
        customShape = QCursor(QPixmap(
                      ":/image/mouse_style/shape/ellipse_mouse.png"), 0, 4);
    } else if (cursorName == "arrow") {
        customShape = QCursor(QPixmap(
                      ":/image/mouse_style/shape/arrow_mouse.png"), 5, 5);
    } else if (cursorName == "text") {
        customShape = QCursor(QPixmap(
                      ":/image/mouse_style/shape/text_mouse.png"), 5, 5);
    } else if  (cursorName == "line") {
        customShape = QCursor(QPixmap(QString(
                   ":/image/mouse_style/color_pen/color%1.png").arg(colorIndex)), 0, 25);
    } else if (cursorName == "straightLine") {
        customShape = QCursor(QPixmap(QString(
                    ":/image/mouse_style/shape/line_mouse.png")), 2, 9);
    }

    return customShape;
}

int stringWidth(const QFont &f, const QString &str)
{
    QFontMetrics fm(f);
    return fm.boundingRect(str).width();
}

QString getFileContent(const QString &file) {
    QFile f(file);
    QString fileContent = "";
    if (f.open(QFile::ReadOnly))
    {
        fileContent = QLatin1String(f.readAll());
        f.close();
    }
    return fileContent;
}

QColor colorIndexOf(int index) {
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

int colorIndex(QColor color) {
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

void   paintSelectedPoint(QPainter &painter, QPoint pos, QPixmap pointImg) {
    painter.drawPixmap(pos, pointImg);
}
