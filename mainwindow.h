#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QWidget>
#include <QPaintEvent>
#include <QObject>
#include <QDebug>
#include <QDir>
#include <QStandardPaths>
#include <QScreen>
#include <QMenu>
#include <QDateTime>

#include "widgets/toptips.h"
#include "widgets/toolbar.h"
#include "widgets/zoomIndicator.h"
#include "widgets/shapeswidget.h"
#include "utils/baseutils.h"
#include "utils/configsettings.h"
#include "controller/menucontroller.h"

#include "dbusinterface/dbuscontrolcenter.h"
#include "dbusinterface/dbusnotify.h"
#include "dbusinterface/dbussoundeffect.h"
#include "dbusinterface/dbuszone.h"

#include "windowmanager.h"
#include "eventmonitor.h"


class MainWindow : public QLabel
{
    Q_OBJECT

public:
    MainWindow(QWidget *parent = 0);
    ~MainWindow();

    enum ShotMouseStatus {
        Normal,
        Wait,
        Shoting,
    };

    void initUI();
    void initShapeWidget(QString type);
    void initDBusInterface();
    void initShortcut();

signals:
    void deleteShapes();

public slots:
    void startScreenshot();
    void showPressFeedback(int x, int y);
    void showDragFeedback(int x, int y);
    void showReleaseFeedback(int x, int y);
    void responseEsc();
    void shotFullScreen();
    void shotCurrentImg();
    void shotImgWidthEffect();
    void saveScreenshot();
    void reloadImage(QString effect);

protected:
    void paintEvent(QPaintEvent *event) Q_DECL_OVERRIDE;
    bool eventFilter(QObject *watched, QEvent *event) Q_DECL_OVERRIDE;
    int  getDirection(QEvent *event);
    void updateCursor(QEvent *event);
    void resizeDirection(ResizeDirection direction, QMouseEvent* e);

private:
    WindowManager* m_windowManager;
    WindowRect m_rootWindowRect;

    QList<WindowRect> m_windowRects;
    QRect m_backgroundRect;
//    QList<QString> m_windowNames;

    int m_screenNum;
    int m_recordX;
    int m_recordY;
    int m_recordWidth;
    int m_recordHeight;

    int m_mouseStatus;
    int m_dragAction;

    int m_dragRecordHeight;
    int m_dragRecordWidth;
    int m_dragRecordX;
    int m_dragRecordY;
    int m_dragStartX;
    int m_dragStartY;

    bool m_needDrawSelectedPoint;
    bool m_drawNothing = false;
    bool m_isFirstDrag;
    bool m_isFirstMove;
    bool m_isFirstPressButton;
    bool m_isFirstReleaseButton;
    bool m_isPressButton;
    bool m_isReleaseButton;
    bool m_isShiftPressed = false;

    QString m_selectAreaName;
    QPixmap m_resizeBigPix;
    QPixmap m_resizeSmallPix;

    TopTips* m_sizeTips;
    ToolBar* m_toolBar;
    ZoomIndicator* m_zoomIndicator;
    ShapesWidget* m_shapesWidget;
    ConfigSettings* m_configSettings;

    bool m_isShapesWidgetExist = false;
    int m_saveIndex;

    MenuController* m_menuController;
    DBusControlCenter* m_controlCenterDBInterface;
    DBusNotify* m_notifyDBInterface;
    DBusSoundEffect* m_soundEffectInterface;
    DBusZone* m_hotZoneInterface;

//    EventMonitor m_eventMonitor;
};

#endif // MAINWINDOW_H
