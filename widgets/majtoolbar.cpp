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
    ToolButton* lineBtn = new ToolButton();
    lineBtn->setObjectName("PenBtn");
    buttonGroup->addButton(lineBtn);
    ToolButton* textBtn = new ToolButton();
    textBtn->setObjectName("TextBtn");
    buttonGroup->addButton(textBtn);
    BigColorButton* colorBtn = new BigColorButton();
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
    m_baseLayout->addSpacing(4);
    m_baseLayout->addWidget(rectBtn);
    m_baseLayout->addSpacing(BUTTON_SPACING);
    m_baseLayout->addWidget(ovalBtn);
    m_baseLayout->addSpacing(BUTTON_SPACING);
    m_baseLayout->addWidget(arrowBtn);
    m_baseLayout->addSpacing(BUTTON_SPACING);
    m_baseLayout->addWidget(lineBtn);
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
    connect(lineBtn, &ToolButton::clicked, this, [=](){
        if (m_currentShape != "line") {
            m_currentShape = "line";
            m_isChecked = true;
        } else {
            m_currentShape = "";
            m_isChecked = false;
        }
        lineBtn->setChecked(m_isChecked);
        emit buttonChecked(m_isChecked, "line");
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
    connect(colorBtn, &BigColorButton::clicked, this, [=](bool clicked){
        colorBtn->setChecked(true);
        emit buttonChecked(true, "color");
    });

    connect(this, &MajToolBar::setCurrentColor, colorBtn, &BigColorButton::setColor);
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
