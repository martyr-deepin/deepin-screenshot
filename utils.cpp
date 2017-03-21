#include "utils.h"

#include <QPixmap>

QCursor setCursorShape(QString cursorName) {
    QCursor customShape = QCursor();
    if (cursorName == "start") {
        customShape = QCursor(QPixmap(":/image/mouse_style/shape/start_mouse.png"), 8, 8);
        return customShape;
    }
}

int stringWidth(const QFont &f, const QString &str)
{
    QFontMetrics fm(f);
    return fm.boundingRect(str).width();
}
