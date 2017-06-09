#ifndef BASEUTILS_H
#define BASEUTILS_H

#include <QCursor>
#include <QFont>
#include <QLayout>
#include <QFontMetrics>
#include <QPainter>

enum ResizeDirection {
    Rotate,
    Moving,
    TopLeft,
    TopRight,
    BottomLeft,
    BottomRight,
    Top,
    Bottom,
    Left,
    Right,
    Outting,
};

namespace utils {
const QString TMP_FILE = "/tmp/deepin-screenshot.png";
const QString TMP_FULLSCREEN_FILE = "/tmp/deepin-screenshot-fullscreen.png";
const QString TMP_MOSA_FILE = "/tmp/deepin-screenshot-mosa.png";
const QString TMP_BLUR_FILE = "/tmp/deepin-screenshot-blur.png";
}

QCursor setCursorShape(QString cursorName, int colorIndex = 0);
int stringWidth(const QFont &f, const QString &str);
QString     getFileContent(const QString &file);
QColor       colorIndexOf(int index);
int                colorIndex(QColor color);
bool          isValidFormat(QString suffix);
bool          isCommandExist(QString command);
void  paintSelectedPoint(QPainter &painter, QPoint pos, QPixmap pointImg);
#endif // BASEUTILS_H
