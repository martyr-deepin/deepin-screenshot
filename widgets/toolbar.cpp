/*
 * Copyright (C) 2017 ~ 2017 Deepin Technology Co., Ltd.
 *
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

#include "toolbar.h"
#include "utils/baseutils.h"

#include <QPainter>
#include <QDebug>
#include <QApplication>
#include <QCursor>
#include <QGraphicsDropShadowEffect>
#include <dgraphicsgloweffect.h>

DWIDGET_USE_NAMESPACE

namespace {
    const int TOOLBAR_HEIGHT = 30;
    const int TOOLBAR_WIDTH = 278;

    const QSize TOOLBAR_WIDGET_SIZE = QSize(276, 28);
    const int BUTTON_SPACING = 3;
    const int BTN_RADIUS = 3;
}

ToolBarWidget::ToolBarWidget(QWidget *parent)
    :DBlurEffectWidget(parent),
      m_expanded(false)
{
    setStyleSheet(getFileContent(":/resources/qss/toolbar.qss"));
    setBlurRectXRadius(3);
    setBlurRectYRadius(3);
    setRadius(30);
    setMaskColor(QColor(255, 255, 255, 204));
    setFixedSize(TOOLBAR_WIDGET_SIZE);

    qDebug() << "~~~~~~" << this->size();
    m_hSeperatorLine = new QLabel(this);
    m_hSeperatorLine->setObjectName("HorSeperatorLine");
    m_hSeperatorLine->setFixedHeight(1);

    m_majToolbar = new MajToolBar(this);
    m_subToolbar = new SubToolBar(this);

    QVBoxLayout* vLayout = new QVBoxLayout();
    vLayout->setMargin(0);
    vLayout->setSpacing(0);
    vLayout->addWidget(m_majToolbar, 0, Qt::AlignVCenter);
    vLayout->addWidget(m_hSeperatorLine, 0, Qt::AlignVCenter);
    vLayout->addWidget(m_subToolbar, 0, Qt::AlignVCenter);
    setLayout(vLayout);

    m_hSeperatorLine->hide();
    m_subToolbar->hide();

    connect(m_majToolbar, &MajToolBar::buttonChecked, this, &ToolBarWidget::setExpand);
    connect(m_majToolbar, &MajToolBar::saveImage, this, &ToolBarWidget::saveImage);
    connect(m_subToolbar, &SubToolBar::saveAction, this, &ToolBarWidget::saveImage);

    connect(m_subToolbar, &SubToolBar::currentColorChanged, this, &ToolBarWidget::colorChanged);
    connect(m_subToolbar, &SubToolBar::currentColorChanged,  m_majToolbar, &MajToolBar::mainColorChanged);

    connect(m_subToolbar, &SubToolBar::showSaveTip, m_majToolbar, &MajToolBar::showSaveTooltip);
    connect(m_subToolbar, &SubToolBar::hideSaveTip, m_majToolbar, &MajToolBar::hideSaveTooltip);

    connect(this, &ToolBarWidget::shapePressed, m_majToolbar, &MajToolBar::shapePressed);
    connect(this, &ToolBarWidget::saveBtnPressed, m_subToolbar, &SubToolBar::saveBtnPressed);
    connect(m_majToolbar, &MajToolBar::saveSpecificedPath, this, &ToolBarWidget::saveSpecifiedPath);
    connect(m_majToolbar, &MajToolBar::closed, this, &ToolBarWidget::closed);
}

void ToolBarWidget::paintEvent(QPaintEvent *e) {
    DBlurEffectWidget::paintEvent(e);

    QPainter painter(this);
    painter.setPen(QColor(255, 255, 255, 76.5));
    painter.setRenderHint(QPainter::Antialiasing);
    painter.drawLine(QPointF(BTN_RADIUS, 0), QPointF(this->width() - 1, 0));
}

bool ToolBarWidget::isButtonChecked() {
    return m_expanded;
}

void ToolBarWidget::specifiedSavePath() {
    m_majToolbar->specificedSavePath();
}

void ToolBarWidget::setExpand(bool expand, QString shapeType) {
    m_subToolbar->switchContent(shapeType);
    emit expandChanged(expand, shapeType);

    if (expand) {
        m_expanded = true;
        setFixedSize(TOOLBAR_WIDGET_SIZE.width(),
                                 TOOLBAR_WIDGET_SIZE.height()*2+1);
        m_hSeperatorLine->show();
        m_subToolbar->show();
    }

    update();
}

ToolBarWidget::~ToolBarWidget() {}


ToolBar::ToolBar(QWidget *parent)
    : QLabel(parent)
{
    setFixedSize(TOOLBAR_WIDTH, TOOLBAR_HEIGHT);
    m_toolbarWidget = new ToolBarWidget(this);
    QVBoxLayout* vLayout = new QVBoxLayout(this);
    vLayout->setContentsMargins(1, 1, 1, 1);
    vLayout->addStretch();
    vLayout->addWidget(m_toolbarWidget);
    vLayout->addStretch();
    setLayout(vLayout);

//    QGraphicsDropShadowEffect* shadowEffect = new QGraphicsDropShadowEffect(this);
//    shadowEffect->setXOffset(0);
//    shadowEffect->setYOffset(6);
//    shadowEffect->setColor(QColor(0, 0, 0, 26));
//    shadowEffect->setBlurRadius(20);
//    setGraphicsEffect(shadowEffect);

    connect(m_toolbarWidget, &ToolBarWidget::expandChanged, this, &ToolBar::setExpand);
    connect(m_toolbarWidget, &ToolBarWidget::saveImage, this, &ToolBar::requestSaveScreenshot);
    connect(m_toolbarWidget, &ToolBarWidget::colorChanged, this, &ToolBar::updateColor);
    connect(this, &ToolBar::shapePressed, m_toolbarWidget, &ToolBarWidget::shapePressed);
    connect(this, &ToolBar::saveBtnPressed, m_toolbarWidget, &ToolBarWidget::saveBtnPressed);
    connect(m_toolbarWidget, &ToolBarWidget::saveSpecifiedPath, this, &ToolBar::saveSpecifiedPath);
    connect(m_toolbarWidget, &ToolBarWidget::closed, this, &ToolBar::closed);
}

void ToolBar::setExpand(bool expand, QString shapeType) {
    emit buttonChecked(shapeType);
    if (expand) {
        m_expanded = true;
        setFixedSize(TOOLBAR_WIDTH,
                              TOOLBAR_WIDGET_SIZE.height()*2+3);
        emit heightChanged();
    }

    update();
}

void ToolBar::paintEvent(QPaintEvent *e) {
    QPainter painter(this);
    painter.setPen(QColor(0, 0, 0, 25));
    painter.setRenderHint(QPainter::Antialiasing);
    QRectF rect(0, 0, this->width() -1, this->height() - 1);
    painter.drawRoundedRect(rect.translated(0.5, 0.5), 3, 3, Qt::AbsoluteSize);

    QLabel::paintEvent(e);
}

void ToolBar::enterEvent(QEvent *e) {
    qApp->setOverrideCursor(Qt::ArrowCursor);
    QLabel::enterEvent(e);
}

void ToolBar::showAt(QPoint pos) {
    if (!isVisible())
        this->show();

    move(pos.x(), pos.y());
}

void ToolBar::specificedSavePath()
{
    m_toolbarWidget->specifiedSavePath();
}

bool ToolBar::isButtonChecked() {
    return m_expanded;
}

ToolBar::~ToolBar()
{
}
