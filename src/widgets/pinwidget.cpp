#include "pinwidget.h"
#include <QMouseEvent>
#include <QMenu>
#include <QKeyEvent>
#include <QPainter>
#include <QDebug>
#include <QFileDialog>
#include <QStandardPaths>
#include <DDesktopServices>
#include <QClipboard>
#include <DApplication>
DWIDGET_USE_NAMESPACE
PinWidget::PinWidget(QPixmap img, QWidget *parent) : QWidget(parent)
{
    m_img = img;
    m_move = false;
    m_zoom = 1;
    setWindowFlags(Qt::FramelessWindowHint);
    initMenu();
}

void PinWidget::initMenu()
{
    m_menu = new QMenu(this);
    m_menu->addAction(tr("Copy Image"), [=](){
        qApp->clipboard()->setPixmap(m_img);
    });
    m_menu->addAction(tr("Save As"), [=](){
        auto defaultPath = tr("%1/untitled.png")
                .arg(QStandardPaths::standardLocations(QStandardPaths::PicturesLocation)[0]);
        auto path = QFileDialog::getSaveFileName(
                    nullptr,
                    tr("Save Image"),
                    defaultPath,
                    tr("Images (*.png *.jpg)")
                    );
        if (!path.isEmpty()) {
            m_img.save(path);
            DDesktopServices::showFileItem(path);
        }
    });
    auto zoomMenu = new QMenu(tr("Zoom"), m_menu);
    QList<QAction*> zoomActionList;
    zoomActionList << zoomMenu->addAction(tr("33.3%"), [=](){m_zoom = 0.333;update();})
                   << zoomMenu->addAction(tr("50%"), [=](){m_zoom = 0.5;update();})
                   << zoomMenu->addAction(tr("100%"), [=](){m_zoom = 1;update();})
                   << zoomMenu->addAction(tr("200%"), [=](){m_zoom = 2;update();})
                      ;
    for(auto action : zoomActionList) {
        action->setCheckable(true);
        connect(action, &QAction::triggered, [=](){
            for(auto it: zoomActionList) {
                it->setChecked(false);
            }
            action->setChecked(true);
        });
    }
    zoomActionList[2]->setChecked(true);
    m_menu->addMenu(zoomMenu);
    m_menu->addAction(tr("Destroy"), [=](){
        this->close();
    });
}
void PinWidget::mousePressEvent(QMouseEvent *event)
{
    if (event->button() == Qt::LeftButton) {
        m_move = true;
        m_startPoint = event->globalPos();
        m_windowPoint = this->frameGeometry().topLeft();
    }
}

void PinWidget::mouseMoveEvent(QMouseEvent *event)
{
    if (event->buttons() & Qt::LeftButton) {
        QPoint relativePos = event->globalPos() - m_startPoint;
        this->move(m_windowPoint + relativePos );
    }
}

void PinWidget::contextMenuEvent(QContextMenuEvent *event)
{
    Q_UNUSED(event)
    m_menu->exec(QCursor::pos());
}

void PinWidget::keyPressEvent(QKeyEvent *event)
{
    if(event->key() == Qt::Key_Escape) {
        this->close();
    }
}

void PinWidget::paintEvent(QPaintEvent *event)
{
    Q_UNUSED(event)
    QPainter painter(this);
    auto w = m_img.width() * m_zoom;
    auto h = m_img.height() * m_zoom;
//    qDebug() << w << h << m_img;
    if (width() != w || height() != h) {
        resize(w, h);
    }
    painter.drawPixmap(0, 0, w, h, m_img);
}


void PinWidget::mouseReleaseEvent(QMouseEvent *event)
{
    if (event->button() == Qt::LeftButton) {
        m_move = false;
    }
}
