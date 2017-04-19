#include "subtoolbar.h"
#include "toolbutton.h"
#include "colorbutton.h"
#include "utils/baseutils.h"

#include <QLineEdit>
#include <QButtonGroup>
#include <QHBoxLayout>
#include <QDebug>

namespace {
    const int TOOLBAR_HEIGHT = 28;
    const int TOOLBAR_WIDTH = 284;
    const int BUTTON_SPACING = 3;
}

SubToolBar::SubToolBar(QWidget *parent)
    : QStackedWidget(parent),
      m_lineWidth(1)
{
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
    m_rectLabel = new QLabel(this);
    QButtonGroup* rectBtnGroup = new QButtonGroup();
    rectBtnGroup->setExclusive(true);
    //rectangle, oval...
    ToolButton* fineLine = new ToolButton();
    fineLine->setObjectName("FineLine");
    rectBtnGroup->addButton(fineLine);
    ToolButton*  mediumLine = new ToolButton();
    mediumLine->setObjectName("MediumLine");
    mediumLine->setChecked(true);
    rectBtnGroup->addButton(mediumLine);
    ToolButton* thickLine = new ToolButton();
    thickLine->setObjectName("ThickLine");
    rectBtnGroup->addButton(thickLine);
    //seperator line...
    QLabel* vSeperatorLine = new QLabel();
    vSeperatorLine->setFixedSize(1, 16);
    vSeperatorLine->setObjectName("VerticalSeperatorLine");
    //blur, mosaic...
    ToolButton* blurBtn = new ToolButton();
    blurBtn->setObjectName("BlurBtn");
    ToolButton* mosaicBtn = new ToolButton();
    mosaicBtn->setObjectName("MosaicBtn");

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
    m_arrowLabel = new QLabel(this);
    QButtonGroup*  arrowBtnGroup = new QButtonGroup();
    arrowBtnGroup->setExclusive(true);
    //rectangle, oval...
    ToolButton* arrowFineLine = new ToolButton();
    arrowFineLine->setObjectName("ArrowFineLine");
    arrowBtnGroup->addButton(arrowFineLine);
    ToolButton*  arrowMediumLine = new ToolButton();
    arrowMediumLine->setObjectName("ArrowMediumLine");
    arrowMediumLine->setChecked(true);
    arrowBtnGroup->addButton(arrowMediumLine);
    ToolButton* arrowThickLine = new ToolButton();
    arrowThickLine->setObjectName("ArrowThickLine");
    arrowBtnGroup->addButton(arrowThickLine);
    //seperator line...
    QLabel* vSeperatorLine = new QLabel();
    vSeperatorLine->setFixedSize(1, 16);
    vSeperatorLine->setObjectName("VerticalSeperatorLine");
    ToolButton*  lineBtn = new ToolButton();
    lineBtn->setObjectName("LineBtn");
    ToolButton* arrowBtn = new ToolButton();
    arrowBtn->setObjectName("ArrowBtn");

    QHBoxLayout* arrowLayout = new QHBoxLayout();
    arrowLayout->setMargin(0);
    arrowLayout->setSpacing(2);
    arrowLayout->addWidget(arrowFineLine);
    arrowLayout->addWidget(arrowMediumLine);
    arrowLayout->addWidget(arrowThickLine);
    arrowLayout->addSpacing(2);
    arrowLayout->addWidget(vSeperatorLine);
    arrowLayout->addSpacing(2);
    arrowLayout->addWidget(lineBtn);
    arrowLayout->addSpacing(2);
    arrowLayout->addWidget(arrowBtn);
    arrowLayout->addStretch();
    m_arrowLabel->setLayout(arrowLayout);
    addWidget(m_arrowLabel);
}

void SubToolBar::initLineLabel() {
     m_lineLabel = new QLabel(this);
     //rectangle, oval...
    QButtonGroup* lineBtnGroup = new QButtonGroup();
    lineBtnGroup->setExclusive(true);
    ToolButton* fineLine = new ToolButton();
    fineLine->setObjectName("FineLine");
    lineBtnGroup->addButton(fineLine);
    ToolButton*  mediumLine = new ToolButton();
    mediumLine->setObjectName("MediumLine");
    mediumLine->setChecked(true);
    lineBtnGroup->addButton(mediumLine);
    ToolButton* thickLine = new ToolButton();
    thickLine->setObjectName("ThickLine");
    lineBtnGroup->addButton(thickLine);

    QHBoxLayout* lineLayout = new QHBoxLayout();
    lineLayout->setMargin(0);
    lineLayout->setSpacing(2);
    lineLayout->addWidget(fineLine);
    lineLayout->addWidget(mediumLine);
    lineLayout->addWidget(thickLine);
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
    QList<ColorButton*> colorBtnList;
    QButtonGroup* colorBtnGroup = new QButtonGroup(m_colorLabel);
    colorBtnGroup->setExclusive(true);

    ColorButton* firstColor = new ColorButton(QColor("#ffd903"));
    ColorButton* secondColor = new ColorButton(QColor("#ff5e1a"));
    ColorButton* thirdColor  = new ColorButton(QColor("#ff3305"));
    ColorButton* fourthColor = new ColorButton(QColor("#ff1c49"));
    ColorButton* fifthColor = new ColorButton(QColor("#fb00ff"));
    ColorButton* sixthColor  = new ColorButton(QColor("#7700ed"));
    ColorButton* seventhColor = new ColorButton(QColor("#3d08ff"));
    ColorButton* eighthColor = new ColorButton(QColor("#3467ff"));
    ColorButton* ninthColor  = new ColorButton(QColor("#00aaff"));
    ColorButton* tenthColor = new ColorButton(QColor("#08ff77"));
    ColorButton* eleventhColor = new ColorButton(QColor("#03a60e"));
    ColorButton* twelfthColor  = new ColorButton(QColor("#3c7d00"));
    ColorButton* thirteenthColor = new ColorButton(QColor("#ffd903"));
    ColorButton* fourteenthColor = new ColorButton(QColor("#ffffff"));
    ColorButton* fifteenthColor  = new ColorButton(QColor("#666666"));
    ColorButton* sixteenthColor = new ColorButton(QColor("#2b2b2b"));
    ColorButton* eighteenthColor = new ColorButton(QColor("#000000"));

    colorBtnList.append(firstColor);
    colorBtnList.append(secondColor);
    colorBtnList.append(thirdColor);
    colorBtnList.append(fourthColor);
    colorBtnList.append(fifthColor);
    colorBtnList.append(sixthColor);
    colorBtnList.append(seventhColor);
    colorBtnList.append(eighthColor);
    colorBtnList.append(ninthColor);
    colorBtnList.append(tenthColor);
    colorBtnList.append(eleventhColor);
    colorBtnList.append(twelfthColor);
    colorBtnList.append(thirteenthColor);
    colorBtnList.append(fourteenthColor);
    colorBtnList.append(fifteenthColor);
    colorBtnList.append(sixteenthColor);
    colorBtnList.append(eighteenthColor);

    for(int i = 0; i < colorBtnList.length(); i++) {
        colorBtnGroup->addButton(colorBtnList[i]);
    }

    QHBoxLayout* colorLayout = new QHBoxLayout();
    colorLayout->setMargin(0);
    colorLayout->setSpacing(3);
    colorLayout->addStretch();
    for(int i = 0; i < colorBtnList.length(); i++) {
        colorLayout->addWidget(colorBtnList[i]);
        connect(colorBtnList[i], &ColorButton::updatePaintColor,
                this, &SubToolBar::setCurrentColor);
    }
    colorLayout->addStretch();
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
    saveLayout->setSpacing(8);
    saveLayout->addSpacing(4);
    saveLayout->addWidget(saveDesktopBtn);
    saveLayout->addWidget(savePicBtn);
    saveLayout->addWidget(saveSpecificDirBtn);
    saveLayout->addWidget(saveClipboardBtn);
    saveLayout->addWidget(saveAutoClipboardBtn);
    saveLayout->addStretch();
    m_saveLabel->setLayout(saveLayout);
    addWidget(m_saveLabel);
}

void SubToolBar::switchContent(QString shapeType) {
    if (shapeType == "rectangle" || shapeType == "oval") {
        setCurrentWidget(m_rectLabel);
    }   else if (shapeType == "arrow") {
        setCurrentWidget(m_arrowLabel);
    } else if (shapeType == "line") {
        setCurrentWidget(m_lineLabel);
    } else if (shapeType == "text") {
        setCurrentWidget(m_textLabel);
    } else if (shapeType == "color") {
        setCurrentWidget(m_colorLabel);
    } else if (shapeType == "saveList") {
        setCurrentWidget(m_saveLabel);
    }
}

SubToolBar::~SubToolBar() {}

