#include "toolbar.h"
#include "utils/baseutils.h"
#include "bigcolorbutton.h"

#include <QApplication>
#include <QButtonGroup>
#include <QDebug>
#include <QCursor>

namespace {
    const int TOOLBAR_HEIGHT = 28;
    const int TOOLBAR_WIDTH = 284;
    const int BUTTON_SPACING = 3;
}
ToolBar::ToolBar(QWidget *parent)
    : QLabel(parent),
      m_isChecked(false)
{
    initWidgets();

}

ToolBar::~ToolBar() {}

void ToolBar::initWidgets() {
    setObjectName("ToolBar");
    setStyleSheet(getFileContent(":/resources/qss/toolbar.qss"));
    setFocusPolicy(Qt::StrongFocus);
    setMouseTracking(true);
    setAcceptDrops(true);
    installEventFilter(this);

    this->setFixedSize(TOOLBAR_WIDTH, TOOLBAR_HEIGHT);
    m_topLabel = new QLabel(this);
    m_topLabel->setFixedSize(TOOLBAR_WIDTH, TOOLBAR_HEIGHT - 6);
    m_bottomLabel = new QLabel(this);
    m_bottomLabel->setFixedSize(TOOLBAR_WIDTH, TOOLBAR_HEIGHT - 6);

    QButtonGroup* buttonGroup = new QButtonGroup(this);
    buttonGroup->setExclusive(true);
    ToolButton* ovalBtn = new ToolButton();
    ovalBtn->setObjectName("OvalBtn");
    buttonGroup->addButton(ovalBtn);
    ToolButton* rectBtn = new ToolButton();
    rectBtn->setObjectName("RectBtn");
    buttonGroup->addButton(rectBtn);
    ToolButton* arrowBtn = new ToolButton();
    arrowBtn->setObjectName("ArrowBtn");
    buttonGroup->addButton(arrowBtn);
    ToolButton* penBtn = new ToolButton();
    penBtn->setObjectName("PenBtn");
    buttonGroup->addButton(penBtn);
    ToolButton* textBtn = new ToolButton();
    textBtn->setObjectName("TextBtn");
    buttonGroup->addButton(textBtn);
    BigColorButton* colorBtn = new BigColorButton();
    colorBtn->setObjectName("ColorBtn");
    buttonGroup->addButton(colorBtn);
    ToolButton* saveBtn = new ToolButton();
    saveBtn->setObjectName("SaveBtn");
    saveBtn->setFixedSize(15, 22);
    buttonGroup->addButton(saveBtn);
    ToolButton* saveListBtn = new ToolButton();
    saveListBtn->setObjectName("ListBtn");
    saveListBtn->setFixedSize(10, 22);
    buttonGroup->addButton(saveListBtn);
    ToolButton* shareBtn = new ToolButton();
    shareBtn->setObjectName("ShareBtn");
    buttonGroup->addButton(shareBtn);
    ToolButton* closeBtn = new ToolButton();
    closeBtn->setObjectName("CloseBtn");
    buttonGroup->addButton(closeBtn);

    m_baseLayout = new QHBoxLayout(m_topLabel);
    m_baseLayout->setMargin(0);
    m_baseLayout->addSpacing(4);    
    m_baseLayout->addWidget(rectBtn);
    m_baseLayout->addSpacing(BUTTON_SPACING);
    m_baseLayout->addWidget(ovalBtn);
    m_baseLayout->addSpacing(BUTTON_SPACING);
    m_baseLayout->addWidget(arrowBtn);
    m_baseLayout->addSpacing(BUTTON_SPACING);
    m_baseLayout->addWidget(penBtn);
    m_baseLayout->addSpacing(BUTTON_SPACING);
    m_baseLayout->addWidget(textBtn);
    m_baseLayout->addSpacing(BUTTON_SPACING);
    m_baseLayout->addWidget(colorBtn);
    m_baseLayout->addSpacing(BUTTON_SPACING);
    m_baseLayout->addWidget(saveBtn);
    m_baseLayout->addSpacing(0);
    m_baseLayout->addWidget(saveListBtn);
    m_baseLayout->addSpacing(BUTTON_SPACING);
    m_baseLayout->addWidget(shareBtn);
    m_baseLayout->addSpacing(BUTTON_SPACING);
    m_baseLayout->addWidget(closeBtn);
    m_baseLayout->addSpacing(4);
    m_baseLayout->addStretch();
    m_expandLayout = new QHBoxLayout(m_bottomLabel);
    m_expandLayout->setMargin(0);
    m_expandLayout->setSpacing(0);

    m_separator = new QLabel(this);
    m_separator->setFixedHeight(1);
    m_separator->setObjectName("SeparatorLine");
    m_separator->hide();

    m_layout = new QVBoxLayout(this);
    m_layout->setMargin(0);
    m_layout->setSpacing(0);
    m_layout->addSpacing(2);
    m_layout->addWidget(m_topLabel);
    m_layout->addSpacing(3);
    m_layout->addWidget(m_separator);
    m_layout->addSpacing(3);
    m_layout->addWidget(m_bottomLabel);
    m_layout->addSpacing(3);
    m_layout->addStretch();

    connect(rectBtn, &ToolButton::clicked, this, [=](bool checked){
        setExpandMode(checked, "Rect");
    });
    connect(ovalBtn, &ToolButton::clicked, this, [=](bool checked){
        setExpandMode(checked, "Oval");
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
        Q_UNUSED(checked);
        qDebug() << "screenshot will exit!";
        qApp->quit();
    });
}

void ToolBar::showToolBar(QPoint pos) {
    if (!this->isVisible())
        this->show();
    this->move(pos.x() - TOOLBAR_WIDTH, pos.y());
}

void ToolBar::setExpandMode(bool expand, QString type) {
    if (expand) {
        m_isChecked = true;
        emit buttonChecked(type);
        setFixedHeight(28*2+1);
        m_separator->show();
    } else {
        m_separator->hide();
        setFixedHeight(28);
    }
}

bool ToolBar::isButtonChecked() {
    return m_isChecked;
}

bool ToolBar::eventFilter(QObject *watched, QEvent *event) {
    Q_UNUSED(watched);

    if (event->type() == QEvent::Enter) {
        setCursor(Qt::ArrowCursor);
        qApp->setOverrideCursor(Qt::ArrowCursor);
    }
    return false;
}

void ToolBar::mouseMoveEvent(QMouseEvent *ev) {
    Q_UNUSED(ev);
    qApp->setOverrideCursor(Qt::ArrowCursor);
}
