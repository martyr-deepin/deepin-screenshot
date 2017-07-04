#ifndef SCREENUTILS_H
#define SCREENUTILS_H

#include <QObject>
#include <QWindow>

class ScreenUtils : public QObject {
    Q_OBJECT
public:
    static ScreenUtils *instance(QPoint pos);

public slots:
    int getScreenNum();
    QRect backgroundRect();
    WId rootWindowId();
    QScreen* primaryScreen();

private:
     static ScreenUtils* m_screenUtils;
     ScreenUtils(QPoint pos, QObject* parent = 0);
     ~ScreenUtils();

    QRect m_backgroundRect;
    int m_screenNum;
    WId m_rootWindowId;
    QScreen* m_primaryScreen;
};

#endif // SCREENUTILS_H
