#include "subtoolbar.h"
#include "toolbutton.h"
#include "utils/baseutils.h"

#include <QLineEdit>
#include <QHBoxLayout>
namespace {
    const int TOOLBAR_HEIGHT = 28;
    const int TOOLBAR_WIDTH = 284;
    const int BUTTON_SPACING = 3;
}

SubToolBar::SubToolBar(QWidget *parent)
    : QStackedWidget(parent) {
    initWidget();
}

void SubToolBar::initWidget() {
    setObjectName("SubToolBar");
    setStyleSheet(getFileContent(":/resources/qss/subtoolbar.qss"));
    setFixedSize(TOOLBAR_WIDTH, TOOLBAR_HEIGHT);

    initRectLabel();
    initArrowLabel();
    initLineLabel();
    initTextLabel();
    initColorLabel();
    initSaveLabel();

    setCurrentWidget(0);
}

void SubToolBar::initRectLabel() {
    //rectangle, oval...
    ToolButton* fineLine = new ToolButton();
    fineLine->setObjectName("FineLine");
    ToolButton*  mediumLine = new ToolButton();
    mediumLine->setObjectName("MediumLine");
    ToolButton* thickLine = new ToolButton();
    thickLine->setObjectName("ThickLine");
    //seperator line...
    QLabel* vSeperatorLine = new QLabel();
    vSeperatorLine->setFixedSize(1, 16);
    vSeperatorLine->setObjectName("VerticalSeperatorLine");
    //blur, mosaic...
    ToolButton* blurBtn = new ToolButton();
    blurBtn->setObjectName("BlurBtn");
    ToolButton* mosaicBtn = new ToolButton();
    mosaicBtn->setObjectName("MosaicBtn");
    m_rectLabel = new QLabel(this);
    QHBoxLayout* rectLayout = new QHBoxLayout();
    rectLayout->setMargin(0);
    rectLayout->setSpacing(4);
    rectLayout->addSpacing(4);
    rectLayout->addWidget(fineLine);
    rectLayout->addWidget(mediumLine);
    rectLayout->addWidget(thickLine);
    rectLayout->addSpacing(2);
    rectLayout->addWidget(vSeperatorLine);
    rectLayout->addSpacing(2);
    rectLayout->addWidget(blurBtn);
    rectLayout->addWidget(mosaicBtn);
    rectLayout->addStretch();
    m_rectLabel->setLayout(rectLayout);
    addWidget(m_rectLabel);
}

void SubToolBar::initArrowLabel() {
    //rectangle, oval...
    ToolButton* fineLine = new ToolButton();
    fineLine->setObjectName("FineLine");
    ToolButton*  mediumLine = new ToolButton();
    mediumLine->setObjectName("MediumLine");
    ToolButton* thickLine = new ToolButton();
    thickLine->setObjectName("ThickLine");
    //seperator line...
    QLabel* vSeperatorLine = new QLabel();
    vSeperatorLine->setFixedSize(1, 16);
    vSeperatorLine->setObjectName("VerticalSeperatorLine");
    ToolButton* arrowBtn = new ToolButton();
    arrowBtn->setObjectName("ArrowBtn");
    m_arrowLabel = new QLabel(this);
    QHBoxLayout* arrowLayout = new QHBoxLayout();
    arrowLayout->setMargin(0);
    arrowLayout->setSpacing(2);
    arrowLayout->addWidget(fineLine);
    arrowLayout->addWidget(mediumLine);
    arrowLayout->addWidget(thickLine);
    arrowLayout->addSpacing(2);
    arrowLayout->addWidget(vSeperatorLine);
    arrowLayout->addSpacing(2);
    arrowLayout->addWidget(arrowBtn);
    arrowLayout->addStretch();
    m_arrowLabel->setLayout(arrowLayout);
    addWidget(m_arrowLabel);
}

void SubToolBar::initLineLabel() {
    //rectangle, oval...
    ToolButton* fineLine = new ToolButton();
    fineLine->setObjectName("FineLine");
    ToolButton*  mediumLine = new ToolButton();
    mediumLine->setObjectName("MediumLine");
    ToolButton* thickLine = new ToolButton();
    thickLine->setObjectName("ThickLine");
    //seperator line...
    QLabel* vSeperatorLine = new QLabel();
    vSeperatorLine->setFixedSize(1, 16);
    vSeperatorLine->setObjectName("VerticalSeperatorLine");
    ToolButton*  lineBtn = new ToolButton();
    lineBtn->setObjectName("LineBtn");

    m_lineLabel = new QLabel(this);
    QHBoxLayout* lineLayout = new QHBoxLayout();
    lineLayout->setMargin(0);
    lineLayout->setSpacing(2);
    lineLayout->addWidget(fineLine);
    lineLayout->addWidget(mediumLine);
    lineLayout->addWidget(thickLine);
    lineLayout->addSpacing(2);
    lineLayout->addWidget(vSeperatorLine);
    lineLayout->addSpacing(2);
    lineLayout->addWidget(lineBtn);
    lineLayout->addStretch();
    m_lineLabel->setLayout(lineLayout);
    addWidget(m_lineLabel);
}

void SubToolBar::initTextLabel() {
    //text...
    QLineEdit* lineEdit = new QLineEdit();
    lineEdit->setObjectName("TextBtn");
    m_textLabel = new QLabel(this);
    QHBoxLayout* textLayout = new QHBoxLayout();
    textLayout->setMargin(0);
    textLayout->setSpacing(0);
    textLayout->addWidget(lineEdit);
    textLayout->addStretch();
    m_textLabel->setLayout(textLayout);
    addWidget(m_textLabel);
}

void SubToolBar::initColorLabel() {
    m_colorLabel = new QLabel(this);
    QHBoxLayout* colorLayout = new QHBoxLayout();
    colorLayout->setMargin(0);
    colorLayout->setSpacing(0);
    m_colorLabel->setLayout(colorLayout);
    addWidget(m_colorLabel);
}

void SubToolBar::initSaveLabel() {
    //save to...
    ToolButton* saveDesktopBtn = new ToolButton();
    saveDesktopBtn->setObjectName("SaveToDesktop");
    ToolButton* savePicBtn = new ToolButton();
    savePicBtn->setObjectName("SaveToPictureDir");
    ToolButton* saveSpecificDirBtn = new ToolButton();
    saveSpecificDirBtn->setObjectName("SaveToSpecificDir");
    ToolButton* saveClipboardBtn = new ToolButton();
    saveClipboardBtn->setObjectName("SaveToClipboard");
    ToolButton* saveAutoClipboardBtn = new ToolButton();
    saveAutoClipboardBtn->setObjectName("SaveToAutoClipboard");

     m_saveLabel = new QLabel(this);
    QHBoxLayout* saveLayout = new QHBoxLayout();
    saveLayout->setMargin(0);
    saveLayout->setSpacing(2);
    saveLayout->addWidget(saveDesktopBtn);
    saveLayout->addWidget(savePicBtn);
    saveLayout->addWidget(saveSpecificDirBtn);
    saveLayout->addWidget(saveClipboardBtn);
    saveLayout->addWidget(saveAutoClipboardBtn);
    saveLayout->addStretch();
    m_saveLabel->setLayout(saveLayout);
    addWidget(m_saveLabel);
}

SubToolBar::~SubToolBar() {}

