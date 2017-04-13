#include "toolbar.h"
#include "utils/baseutils.h"
#include <QDebug>

namespace {
    const int TOOLBAR_HEIGHT = 28;
    const int TOOLBAR_WIDTH = 284;
    const int BUTTON_SPACING = 3;
}

ToolBar::ToolBar(QWidget *parent)
    : QLabel(parent),
      m_isChecked(false)
{
    setObjectName("ToolBar");
    setStyleSheet(getFileContent(":/resources/qss/toolbar.qss"));
    setFixedSize(TOOLBAR_WIDTH, TOOLBAR_HEIGHT);

    m_hSeperatorLine = new QLabel(this);
    m_hSeperatorLine->setObjectName("HorSeperatorLine");
    m_hSeperatorLine->setFixedHeight(1);

    m_majToolbar = new MajToolBar(this);
    m_subToolbar = new SubToolBar(this);

    QVBoxLayout* vLayout = new QVBoxLayout();
    vLayout->setMargin(0);
    vLayout->setSpacing(0);
    vLayout->addStretch();
    vLayout->addWidget(m_majToolbar);
    vLayout->addWidget(m_hSeperatorLine);
    vLayout->addWidget(m_subToolbar);
    vLayout->addStretch();
    setLayout(vLayout);

    m_hSeperatorLine->hide();
    m_subToolbar->hide();

    connect(m_majToolbar, &MajToolBar::buttonChecked, this, &ToolBar::setExpand);
}

bool ToolBar::isButtonChecked() {
    return m_isChecked;
}

void ToolBar::setExpand(bool expand, QString shapeType) {
    emit buttonChecked(shapeType);
    if (expand) {
        m_isChecked = true;
        setFixedSize(TOOLBAR_WIDTH, TOOLBAR_HEIGHT*2);
        m_hSeperatorLine->show();
        m_subToolbar->show();
    } else {
        m_isChecked = false;
        setFixedSize(TOOLBAR_WIDTH, TOOLBAR_HEIGHT);
        m_hSeperatorLine->hide();
        m_subToolbar->hide();
    }
    update();
}

void ToolBar::showAt(QPoint pos) {
    if (!isVisible())
        show();

    move(pos.x() - TOOLBAR_WIDTH, pos.y());
}

ToolBar::~ToolBar() {}
