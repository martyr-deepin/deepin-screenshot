#include "baseutils.h"
#include <QPixmap>
#include <QFile>

QCursor setCursorShape(QString cursorName) {
    QCursor customShape = QCursor();
    if (cursorName == "start") {
        customShape = QCursor(QPixmap(
                      ":/image/mouse_style/shape/start_mouse.png"), 8, 8);
    } else if (cursorName == "rotate") {
        customShape = QCursor(QPixmap(
                      ":/image/mouse_style/shape/rotate.png"), 5, 5);
    } else if (cursorName == "rect") {
        customShape = QCursor(QPixmap(
                      ":/image/mouse_style/shape/rect_mouse.png"), 5, 5);
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
