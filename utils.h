#ifndef UTILS_H
#define UTILS_H

#include <QCursor>
#include <QFont>
#include <QFontMetrics>

QCursor setCursorShape(QString cursorName);
int stringWidth(const QFont &f, const QString &str);



#endif // UTILS_H
