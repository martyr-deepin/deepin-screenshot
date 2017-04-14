#include "majtoolbar.h"
#include "utils/baseutils.h"
#include "bigcolorbutton.h"
#include "toolbutton.h"

#include <QApplication>
#include <QButtonGroup>
#include <QDebug>
#include <QCursor>

namespace {
    const int TOOLBAR_HEIGHT = 28;
    const int TOOLBAR_WIDTH = 284;
    const int BUTTON_SPACING = 3;
}
MajToolBar::MajToolBar(QWidget *parent)
    : QLabel(parent),
      m_isChecked(false),
      m_currentShape("")
{
    initWidgets();
}

MajToolBar::~MajToolBar() {}

void MajToolBar::initWidgets() {
    setStyleSheet(getFileContent(":/resources/qss/majtoolbar.qss"));
    setFixedSize(TOOLBAR_WIDTH, TOOLBAR_HEIGHT);
    setFocusPolicy(Qt::StrongFocus);
    setMouseTracking(true);
    setAcceptDrops(true);
    installEventFilter(this);

    QButtonGroup* buttonGroup = new QButtonGroup(this);
    buttonGroup->setExclusive(true);
    ToolButton* rectBtn = new ToolButton();
    rectBtn->setObjectName("RectBtn");
    buttonGroup->addButton(rectBtn);
    ToolButton* ovalBtn = new ToolButton();
    ovalBtn->setObjectName("OvalBtn");
    buttonGroup->addButton(ovalBtn);
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

    m_baseLayout = new QHBoxLayout();
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

    setLayout(m_baseLayout);

    connect(rectBtn, &ToolButton::clicked, this, [=](){
        if (m_currentShape != "rectangle") {
            m_currentShape = "rectangle";
            m_isChecked = true;
        } else {
            m_currentShape = "";
            m_isChecked = false;
        }
        rectBtn->setChecked(m_isChecked);
        rectBtn->update();
        emit buttonChecked(m_isChecked, "rectangle");
    });
    connect(ovalBtn, &ToolButton::clicked, this, [=](){
        if (m_currentShape != "oval") {
            m_currentShape = "oval";
            m_isChecked = true;
        } else {
            m_currentShape = "";
            m_isChecked = false;
        }
        ovalBtn->setChecked(m_isChecked);
        emit buttonChecked(m_isChecked, "oval");
    });
    connect(arrowBtn, &ToolButton::clicked, this, [=](){
        if (m_currentShape != "arrow") {
            m_currentShape = "arrow";
            m_isChecked = true;
        } else {
            m_currentShape = "";
            m_isChecked = false;
        }
        arrowBtn->setChecked(m_isChecked);
        emit buttonChecked(m_isChecked, "arrow");
    });
    connect(penBtn, &ToolButton::clicked, this, [=](){
        if (m_currentShape != "pen") {
            m_currentShape = "pen";
            m_isChecked = true;
        } else {
            m_currentShape = "";
            m_isChecked = false;
        }
        penBtn->setChecked(m_isChecked);
        emit buttonChecked(m_isChecked, "pen");
    });
    connect(textBtn, &ToolButton::clicked, this, [=](){
        if (m_currentShape != "text") {
            m_currentShape = "text";
            m_isChecked = true;
        } else {
            m_currentShape = "";
            m_isChecked = false;
        }
        textBtn->setChecked(m_isChecked);
        emit buttonChecked(m_isChecked, "text");
    });
    connect(colorBtn, &ToolButton::clicked, this, [=](){
        if (m_currentShape != "color") {
            m_currentShape = "color";
            m_isChecked = true;
        } else {
            m_currentShape = "";
            m_isChecked = false;
        }
        colorBtn->setChecked(m_isChecked);
        emit buttonChecked(m_isChecked, "color");
    });

    connect(saveBtn, &ToolButton::clicked, this, [=](){
        if (m_currentShape != "save") {
            m_currentShape = "save";
            m_isChecked = true;
        } else {
            m_currentShape = "";
            m_isChecked = false;
        }
        saveBtn->setChecked(m_isChecked);
        emit buttonChecked(m_isChecked, "save");
    });
    connect(saveListBtn, &ToolButton::clicked, this, [=](){
        if (m_currentShape != "saveList") {
            m_currentShape = "saveList";
            m_isChecked = true;
        } else {
            m_currentShape = "";
            m_isChecked = false;
        }
        saveListBtn->setChecked(m_isChecked);
        emit buttonChecked(m_isChecked, "saveList");
    });

    connect(closeBtn, &ToolButton::clicked, this, [=](bool checked){
        Q_UNUSED(checked);
        qDebug() << "screenshot will exit!";
        qApp->quit();
    });
}

bool MajToolBar::isButtonChecked() {
    return m_isChecked;
}

bool MajToolBar::eventFilter(QObject *watched, QEvent *event) {
    Q_UNUSED(watched);

    if (event->type() == QEvent::Enter) {
        setCursor(Qt::ArrowCursor);
        qApp->setOverrideCursor(Qt::ArrowCursor);
    }
    return false;
}

void MajToolBar::mouseMoveEvent(QMouseEvent *ev) {
    Q_UNUSED(ev);
    qApp->setOverrideCursor(Qt::ArrowCursor);
}
