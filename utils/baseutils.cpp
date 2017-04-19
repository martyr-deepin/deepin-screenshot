#include "baseutils.h"

#include <QPixmap>
#include <QLayoutItem>
#include <QFile>

QCursor setCursorShape(QString cursorName) {
    QCursor customShape = QCursor();
    if (cursorName == "start") {
        customShape = QCursor(QPixmap(
                      ":/image/mouse_style/shape/start_mouse.png"), 8, 8);
    } else if (cursorName == "rotate") {
        customShape = QCursor(QPixmap(
                      ":/image/mouse_style/shape/rotate_mouse.png"), 5, 5);
    } else if (cursorName == "rectangle") {
        customShape = QCursor(QPixmap(
                      ":/image/mouse_style/shape/rect_mouse.png"), 5, 5);
    } else if (cursorName == "oval") {
        customShape = QCursor(QPixmap(
                      ":/image/mouse_style/shape/ellipse_mouse.png"), 5, 5);
    } else if (cursorName == "arrow") {
        customShape = QCursor(QPixmap(
                      ":/image/mouse_style/shape/arrow_mouse.png"), 5, 5);
    } else if (cursorName == "text") {
        customShape = QCursor(QPixmap(
                      ":/image/mouse_style/shape/text_mouse.png"), 5, 5);
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

void clearLayout(QLayout *layout) {
    QLayoutItem *item;
    while((item = layout->takeAt(0))) {
        if (item->layout()) {
            clearLayout(item->layout());
            delete item->layout();
        }
        if (item->widget()) {
            delete item->widget();
        }
        delete item;
    }
}
