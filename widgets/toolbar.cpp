#include "toolbar.h"
#include "utils.h"

#include <QPushButton>
#include <QApplication>
#include <QDebug>

ToolBar::ToolBar(QWidget *parent)
    : QLabel(parent) {
    initWidgets();

}

ToolBar::~ToolBar() {}

void ToolBar::initWidgets() {
    setObjectName("ToolBar");
    setFixedSize(284, 28);
    setStyleSheet(getFileContent(":/resources/qss/toolbar.qss"));
    qApp->setOverrideCursor(Qt::ArrowCursor);
    QPushButton* ovalBtn = new QPushButton();
    ovalBtn->setObjectName("OvalBtn");
    ovalBtn->setFixedSize(22, 22);
    ovalBtn->setCheckable(true);
    QPushButton* rectBtn = new QPushButton();
    rectBtn->setObjectName("RectBtn");
    rectBtn->setFixedSize(22, 22);
    rectBtn->setCheckable(true);
    QPushButton* arrowBtn = new QPushButton();
    arrowBtn->setObjectName("ArrowBtn");
    arrowBtn->setFixedSize(22, 22);
    arrowBtn->setCheckable(true);
    QPushButton* penBtn = new QPushButton();
    penBtn->setObjectName("PenBtn");
    penBtn->setFixedSize(22, 22);
    penBtn->setCheckable(true);
    QPushButton* textBtn = new QPushButton();
    textBtn->setObjectName("TextBtn");
    textBtn->setFixedSize(22, 22);
    textBtn->setCheckable(true);
    QPushButton* colorBtn = new QPushButton();
    colorBtn->setObjectName("ColorBtn");
    colorBtn->setFixedSize(22, 22);
    colorBtn->setCheckable(true);
    QPushButton* saveBtn = new QPushButton();
    saveBtn->setObjectName("SaveBtn");
    saveBtn->setFixedSize(15, 22);
    saveBtn->setCheckable(true);

    QPushButton* saveListBtn = new QPushButton();
    saveListBtn->setObjectName("ListBtn");
    saveListBtn->setFixedSize(10, 22);
    saveListBtn->setCheckable(true);

    QPushButton* shareBtn = new QPushButton();
    shareBtn->setObjectName("ShareBtn");
    shareBtn->setFixedSize(22, 22);
    shareBtn->setCheckable(true);

    QPushButton* closeBtn = new QPushButton();
    closeBtn->setObjectName("CloseBtn");
    closeBtn->setFixedSize(22, 22);
    closeBtn->setCheckable(true);

    m_layout = new QHBoxLayout();
    m_layout->setMargin(0);
    m_layout->setSpacing(8);
    m_layout->addSpacing(7);
    m_layout->addWidget(ovalBtn);
    m_layout->addWidget(rectBtn);
    m_layout->addWidget(arrowBtn);
    m_layout->addWidget(penBtn);
    m_layout->addWidget(textBtn);
    m_layout->addWidget(colorBtn);
    m_layout->addWidget(saveBtn);
    m_layout->addWidget(saveListBtn);
    m_layout->addWidget(shareBtn);
    m_layout->addWidget(closeBtn);
    m_layout->addStretch();

    setLayout(m_layout);

}

void ToolBar::showToolBar(QPoint pos) {
    if (!this->isVisible())
        this->show();
    this->move(pos.x() - 284, pos.y());
}
