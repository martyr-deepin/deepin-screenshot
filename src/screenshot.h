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

#ifndef SCREENSHOT_H
#define SCREENSHOT_H

#include <QObject>

#include "mainwindow.h"
#include "eventcontainer.h"

class Screenshot : public QObject {
    Q_OBJECT
public:
    Screenshot(QObject* parent = 0);
    ~Screenshot();

    void noNotify();

public slots:
    void startScreenshot();
    void delayScreenshot(double num);
    void fullscreenScreenshot();
    void topWindowScreenshot();
    void savePathScreenshot(const QString &path);

private:
    void initUI();

    EventContainer* m_eventContainer = nullptr;
    MainWindow* m_window = nullptr;
    bool m_noNotify = false;
};

#endif // SCREENSHOT_H
