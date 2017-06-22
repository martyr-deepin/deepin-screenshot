#ifndef SCREENSHOT_H
#define SCREENSHOT_H

#include <QMainWindow>

#include "mainwindow.h"
#include "eventcontainer.h"

class Screenshot : public QMainWindow {
    Q_OBJECT
public:
    Screenshot(QWidget* parent = 0);
    ~Screenshot();

public slots:
    void startScreenshot();
    void delayScreenshot(int num);
    void fullscreenScreenshot();
    void topWindowScreenshot();
    void noNotifyScreenshot();
    void savePathScreenshot(const QString &path);

protected:
    bool  eventFilter(QObject* watched, QEvent* event) override;

private:
    void initUI();

    EventContainer* m_eventContainer = nullptr;
    bool m_keyboardGrabbed = false;
    bool m_keyboardReleased = false;

    MainWindow* m_window = nullptr;

};

#endif // SCREENSHOT_H
