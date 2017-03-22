#ifndef UTILS_H
#define UTILS_H

#include <QCursor>
#include <QFont>
#include <QFontMetrics>

QCursor setCursorShape(QString cursorName);
int stringWidth(const QFont &f, const QString &str);
QString     getFileContent(const QString &file);

#endif // UTILS_H
