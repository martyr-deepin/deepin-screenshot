#include "toolbar.h"
#include "utils/baseutils.h"

#include <QPainter>
#include <QDebug>

namespace {
    const int TOOLBAR_HEIGHT = 28;
    const int TOOLBAR_WIDTH = 280;
    const int BUTTON_SPACING = 3;
}

ToolBar::ToolBar(QWidget *parent)
    :DBlurEffectWidget(parent),
      m_expanded(false)
{
    setStyleSheet(getFileContent(":/resources/qss/toolbar.qss"));
    setBlurRectXRadius(3);
    setBlurRectYRadius(3);
    setRadius(30);
    setMaskColor(Qt::white);
    setFixedSize(TOOLBAR_WIDTH, TOOLBAR_HEIGHT);

    m_hSeperatorLine = new QLabel(this);
    m_hSeperatorLine->setObjectName("HorSeperatorLine");
    m_hSeperatorLine->setFixedHeight(1);

    m_bgLabel = new QLabel(this);
    m_bgLabel->setFixedSize(TOOLBAR_WIDTH, TOOLBAR_HEIGHT);
    m_majToolbar = new MajToolBar(this);
    m_subToolbar = new SubToolBar(this);

    QVBoxLayout* vLayout = new QVBoxLayout();
    vLayout->setMargin(0);
    vLayout->setSpacing(0);
    vLayout->addStretch();
    vLayout->addWidget(m_majToolbar, 0, Qt::AlignVCenter);
    vLayout->addWidget(m_hSeperatorLine, 0, Qt::AlignVCenter);
    vLayout->addWidget(m_subToolbar, 0, Qt::AlignVCenter);
    vLayout->addStretch();
    m_bgLabel->setLayout(vLayout);

    m_hSeperatorLine->hide();
    m_subToolbar->hide();

    QHBoxLayout* hLayout = new QHBoxLayout();
    hLayout->setMargin(0);
    hLayout->setSpacing(0);
    hLayout->addStretch();
    hLayout->addWidget(m_bgLabel);
    hLayout->addStretch();
    setLayout(hLayout);

    connect(m_majToolbar, &MajToolBar::buttonChecked, this, &ToolBar::setExpand);
    connect(m_majToolbar, &MajToolBar::saveImage, this, &ToolBar::requestSaveScreenshot);
    connect(this, &ToolBar::buttonChecked, m_subToolbar, &SubToolBar::switchContent);
    connect(m_subToolbar, &SubToolBar::currentColorChanged,
            m_majToolbar, &MajToolBar::mainColorChanged);
    connect(m_subToolbar, &SubToolBar::saveAction, this, &ToolBar::requestSaveScreenshot);
    connect(m_subToolbar, &SubToolBar::currentColorChanged, this, &ToolBar::updateColor);
    connect(m_subToolbar, &SubToolBar::showSaveTip, m_majToolbar, &MajToolBar::showSaveTooltip);
    connect(m_subToolbar, &SubToolBar::hideSaveTip, m_majToolbar, &MajToolBar::hideSaveTooltip);
    connect(this, &ToolBar::shapePressed, m_majToolbar, &MajToolBar::shapePressed);
    connect(this, &ToolBar::saveBtnPressed, m_subToolbar, &SubToolBar::saveBtnPressed);
    connect(m_majToolbar, &MajToolBar::saveSpecificedPath, this, &ToolBar::saveSpecifiedPath);
}

bool ToolBar::isButtonChecked() {
    return m_expanded;
}

void ToolBar::setExpand(bool expand, QString shapeType) {
     emit buttonChecked(shapeType);

    if (expand) {
        m_expanded = true;
        m_bgLabel->setFixedSize(TOOLBAR_WIDTH, TOOLBAR_HEIGHT*2+1);
        setFixedSize(TOOLBAR_WIDTH, TOOLBAR_HEIGHT*2+1);;
        m_hSeperatorLine->show();
        m_subToolbar->show();
        m_bgLabel->update();
    }

    update();
}

int ToolBar::getSaveQualityIndex() {
    return m_subToolbar->getSaveQualityIndex();
}

void ToolBar::specificedSavePath() {
    emit m_majToolbar->specificedSavePath();
}

void ToolBar::paintEvent(QPaintEvent *e) {
    DBlurEffectWidget::paintEvent(e);

    QPainter painter(this);
    painter.setPen(QColor(0, 0, 0, 25));
    painter.setRenderHint(QPainter::Antialiasing);
    QRectF rect(0, 0, this->width() -1, this->height() - 1);

    painter.setBrush(QColor(255, 255, 255, 154));
    painter.drawRoundedRect(rect.translated(0.5, 0.5), 3, 3, Qt::AbsoluteSize);
}

void ToolBar::showAt(QPoint pos) {
    if (!isVisible())
        show();

    move(pos.x(), pos.y());
}

ToolBar::~ToolBar() {}
