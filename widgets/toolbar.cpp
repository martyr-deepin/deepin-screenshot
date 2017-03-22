#include "toolbar.h"
#include "utils.h"

#include <QApplication>
#include <QDebug>

namespace {
    const int TOOLBAR_HEIGHT = 28;
    const int TOOLBAR_WIDTH = 284;
}
ToolBar::ToolBar(QWidget *parent)
    : QLabel(parent) {
    initWidgets();

}

ToolBar::~ToolBar() {}

void ToolBar::initWidgets() {
    setObjectName("ToolBar");
    setFixedSize(TOOLBAR_WIDTH, TOOLBAR_HEIGHT);
    setStyleSheet(getFileContent(":/resources/qss/toolbar.qss"));
    qApp->setOverrideCursor(Qt::ArrowCursor);

    ToolButton* ovalBtn = new ToolButton();
    ovalBtn->setObjectName("OvalBtn");

    ToolButton* rectBtn = new ToolButton();
    rectBtn->setObjectName("RectBtn");

    ToolButton* arrowBtn = new ToolButton();
    arrowBtn->setObjectName("ArrowBtn");

    ToolButton* penBtn = new ToolButton();
    penBtn->setObjectName("PenBtn");

    ToolButton* textBtn = new ToolButton();
    textBtn->setObjectName("TextBtn");

    ToolButton* colorBtn = new ToolButton();
    colorBtn->setObjectName("ColorBtn");

    ToolButton* saveBtn = new ToolButton();
    saveBtn->setObjectName("SaveBtn");
    saveBtn->setFixedSize(15, 22);

    ToolButton* saveListBtn = new ToolButton();
    saveListBtn->setObjectName("ListBtn");
    saveListBtn->setFixedSize(10, 22);

    ToolButton* shareBtn = new ToolButton();
    shareBtn->setObjectName("ShareBtn");

    ToolButton* closeBtn = new ToolButton();
    closeBtn->setObjectName("CloseBtn");

    m_baseLayout = new QHBoxLayout();
    m_baseLayout->setMargin(0);
    m_baseLayout->setSpacing(8);
    m_baseLayout->addSpacing(7);
    m_baseLayout->addWidget(ovalBtn);
    m_baseLayout->addWidget(rectBtn);
    m_baseLayout->addWidget(arrowBtn);
    m_baseLayout->addWidget(penBtn);
    m_baseLayout->addWidget(textBtn);
    m_baseLayout->addWidget(colorBtn);
    m_baseLayout->addWidget(saveBtn);
    m_baseLayout->addWidget(saveListBtn);
    m_baseLayout->addWidget(shareBtn);
    m_baseLayout->addWidget(closeBtn);
    m_baseLayout->addStretch();

    QWidget* expandWidget = new QWidget;
    expandWidget->setFixedSize(TOOLBAR_WIDTH, TOOLBAR_HEIGHT);

    m_expandLayout = new QHBoxLayout();
    m_expandLayout->setMargin(0);
    m_expandLayout->setSpacing(0);
    m_expandLayout->addWidget(expandWidget);

    m_layout = new QVBoxLayout();
    m_layout->setMargin(0);
    m_layout->setSpacing(0);
    m_layout->addStretch();
    m_layout->addSpacing(2);
    m_layout->addLayout(m_baseLayout);
    m_layout->addLayout(m_expandLayout);
    m_layout->addStretch();
    setLayout(m_layout);

    connect(ovalBtn, &ToolButton::clicked, this, [=](bool checked){
        setExpandMode(checked, "Oval");
    });
    connect(rectBtn, &ToolButton::clicked, this, [=](bool checked){
        setExpandMode(checked, "Rect");
    });
    connect(arrowBtn, &ToolButton::clicked, this, [=](bool checked){
        setExpandMode(checked, "Arrow");
    });
    connect(penBtn, &ToolButton::clicked, this, [=](bool checked){
        setExpandMode(checked, "Pen");
    });
    connect(textBtn, &ToolButton::clicked, this, [=](bool checked){
        setExpandMode(checked, "Text");
    });
    connect(colorBtn, &ToolButton::clicked, this, [=](bool checked){
        setExpandMode(checked, "Color");
    });
    connect(saveBtn, &ToolButton::clicked, this, [=](bool checked){
        setExpandMode(checked, "Save");
    });
    connect(saveListBtn, &ToolButton::clicked, this, [=](bool checked){
        setExpandMode(checked, "SaveList");
    });

    connect(closeBtn, &ToolButton::clicked, this, [=](bool checked){
        setExpandMode(checked, "Close");
    });
}

void ToolBar::showToolBar(QPoint pos) {
    if (!this->isVisible())
        this->show();
    this->move(pos.x() - TOOLBAR_WIDTH, pos.y());
}

void ToolBar::setExpandMode(bool expand, QString type) {
    if (expand) {
        this->setFixedHeight(28*2);
    } else {
        this->setFixedHeight(28);
    }
    Q_UNUSED(type);
}
