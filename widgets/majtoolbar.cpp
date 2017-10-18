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

#include "majtoolbar.h"
#include "utils/baseutils.h"
#include "utils/configsettings.h"
#include "bigcolorbutton.h"
#include "toolbutton.h"
#include "savebutton.h"
#include "savetips.h"

#include <QApplication>
#include <QButtonGroup>
#include <QDebug>
#include <QCursor>

namespace {
    const int TOOLBAR_HEIGHT = 28;
    const int TOOLBAR_WIDTH = 276;
    const int BTN_SPACING = 1;
    const int TOOLBUTTON_WIDTH = 22;
    const QSize SAVE_BTN = QSize(30, 26);
    const QSize LIST_BTN = QSize(12, 26);
}

MajToolBar::MajToolBar(QWidget *parent)
    : QLabel(parent),
      m_isChecked(false),
      m_currentShape("")
{
    initWidgets();
}

MajToolBar::~MajToolBar() {}

void MajToolBar::initWidgets()
{
    setStyleSheet(getFileContent(":/resources/qss/majtoolbar.qss"));
    setFixedHeight(TOOLBAR_HEIGHT);
    setFocusPolicy(Qt::StrongFocus);
    setMouseTracking(true);
    setAcceptDrops(true);

    SaveTips* saveTips = new SaveTips();
    QList<ToolButton*> toolBtnList;
    QButtonGroup* buttonGroup = new QButtonGroup(this);
    buttonGroup->setExclusive(true);
    ToolButton* rectBtn = new ToolButton();
    rectBtn->setObjectName("RectBtn");
    toolBtnList.append(rectBtn);
    ToolButton* ovalBtn = new ToolButton();
    ovalBtn->setObjectName("OvalBtn");
    toolBtnList.append(ovalBtn);
    ToolButton* arrowBtn = new ToolButton();
    arrowBtn->setObjectName("ArrowBtn");
    toolBtnList.append(arrowBtn);
    ToolButton* sLineBtn = new ToolButton();
    sLineBtn->setObjectName("StraightLineBtn");
    toolBtnList.append(sLineBtn);
    ToolButton* lineBtn = new ToolButton();
    lineBtn->setObjectName("PenBtn");
    toolBtnList.append(lineBtn);
    ToolButton* textBtn = new ToolButton();
    textBtn->setObjectName("TextBtn");
    toolBtnList.append(textBtn);


    BigColorButton* colorBtn = new BigColorButton();
    colorBtn->setObjectName("ColorBtn");
//    ToolButton* shareBtn = new ToolButton();
//    shareBtn->setObjectName("ShareBtn");
    ToolButton* saveBtn = new ToolButton(this);
    saveBtn->setObjectName("SaveBtn");
    saveBtn->setFixedSize(SAVE_BTN);
    ToolButton* listBtn = new ToolButton(this);
    listBtn->setObjectName("ListBtn");
    listBtn->setFixedSize(LIST_BTN);

    ToolButton* okBtn = new ToolButton(this);
    okBtn->setObjectName("OkBtn");

    ToolButton* closeBtn = new ToolButton();
    closeBtn->setObjectName("CloseBtn");

    connect(this, &MajToolBar::shapePressed, this, [=](QString shape) {
        if (shape == "rectangle") {
            qDebug() << "rect clicked!";
            rectBtn->click();
        } else if (shape == "oval") {
            ovalBtn->click();
            qDebug() << "oval clicked!";
        } else if (shape == "arrow") {
            if (arrowBtn->isVisible())
                arrowBtn->click();
            else
                sLineBtn->click();
        } else if (shape == "line") {
            lineBtn->click();
        } else if (shape == "text") {
            textBtn->click();
        } else if (shape == "color") {
           colorBtn->click();
        } else if (shape == "close") {
            closeBtn->click();
        }
    });

    m_baseLayout = new QHBoxLayout();
    m_baseLayout->setMargin(0);
    m_baseLayout->setSpacing(0);
    m_baseLayout->addSpacing(1);
    m_baseLayout->addWidget(saveTips);
    for (int k = 0; k < toolBtnList.length(); k++) {
        m_baseLayout->addWidget(toolBtnList[k]);
        if (k != 2) {
        m_baseLayout->addSpacing(BTN_SPACING);
        }
        buttonGroup->addButton(toolBtnList[k]);
    }
    m_baseLayout->addWidget(colorBtn);
    m_baseLayout->addSpacing(BTN_SPACING);
    m_baseLayout->addWidget(saveBtn);
    m_baseLayout->addSpacing(1);
    m_baseLayout->addWidget(listBtn);
    m_baseLayout->addWidget(okBtn);
    m_baseLayout->addSpacing(BTN_SPACING);
    m_baseLayout->addWidget(closeBtn);
    m_baseLayout->addStretch();
    setLayout(m_baseLayout);
    if (ConfigSettings::instance()->value("arrow", "is_straight").toBool()) {
        sLineBtn->show();
        arrowBtn->hide();
    } else {
        sLineBtn->hide();
        arrowBtn->show();
    }

    okBtn->hide();

    connect(saveTips, &SaveTips::tipWidthChanged, this,  [=](int value){
        setFixedWidth(TOOLBAR_WIDTH + value);
        m_baseLayout->update();
        setLayout(m_baseLayout);
        this->updateGeometry();
    });
    connect(this, &MajToolBar::showSaveTooltip, this, [=](QString tips){
        saveTips->setSaveText(tips);
        saveTips->startAnimation();
    });
    connect(this, &MajToolBar::hideSaveTooltip, this, [=]{
        saveTips->endAnimation();
    });

    connect(rectBtn, &ToolButton::clicked, this, [=](){
        if (m_currentShape != "rectangle") {
            m_currentShape = "rectangle";
            m_isChecked = true;

            int rectColorIndex = ConfigSettings::instance()->value("rectangle", "color_index").toInt();
            ConfigSettings::instance()->setValue("common", "color_index", rectColorIndex);
        } else {
            m_currentShape = "";
            m_isChecked = false;
        }
        rectBtn->update();
        emit buttonChecked(m_isChecked, "rectangle");
    });
    connect(ovalBtn, &ToolButton::clicked, this, [=](){
        if (m_currentShape != "oval") {
            m_currentShape = "oval";
            m_isChecked = true;
            int ovalColorIndex = ConfigSettings::instance()->value("oval", "color_index").toInt();
            ConfigSettings::instance()->setValue("common", "color_index", ovalColorIndex);
        } else {
            m_currentShape = "";
            m_isChecked = false;
        }

        emit buttonChecked(m_isChecked, "oval");
    });
    connect(arrowBtn, &ToolButton::clicked, this, [=](){
        if (m_currentShape != "arrow") {
            m_currentShape = "arrow";
            m_isChecked = true;
            int rectColorIndex = ConfigSettings::instance()->value("arrow", "color_index").toInt();
            ConfigSettings::instance()->setValue("common", "color_index", rectColorIndex);
        } else {
            m_currentShape = "";
            m_isChecked = false;
        }

        emit buttonChecked(m_isChecked, "arrow");
    });
    connect(sLineBtn, &ToolButton::clicked, this, [=](){
        if (m_currentShape != "arrow") {
            m_currentShape = "arrow";
            m_isChecked = true;
            int rectColorIndex = ConfigSettings::instance()->value("arrow", "color_index").toInt();
            ConfigSettings::instance()->setValue("common", "color_index", rectColorIndex);
        } else {
            m_currentShape = "";
            m_isChecked = false;
        }

        emit buttonChecked(m_isChecked, "arrow");
    });
    connect(ConfigSettings::instance(), &ConfigSettings::straightLineConfigChanged, this, [=](bool isStraightLine){
        if (isStraightLine) {
            arrowBtn->hide();
            sLineBtn->show();
            if (m_currentShape == "arrow") {
                sLineBtn->setChecked(true);
            }
        } else {
            arrowBtn->show();
            sLineBtn->hide();
            if (m_currentShape == "arrow") {
                arrowBtn->setChecked(true);
            }
        }
    });
    connect(lineBtn, &ToolButton::clicked, this, [=](){
        if (m_currentShape != "line") {
            m_currentShape = "line";
            m_isChecked = true;
            int rectColorIndex = ConfigSettings::instance()->value("line", "color_index").toInt();
            ConfigSettings::instance()->setValue("common", "color_index", rectColorIndex);
        } else {
            m_currentShape = "";
            m_isChecked = false;
        }

        emit buttonChecked(m_isChecked, "line");
    });
    connect(textBtn, &ToolButton::clicked, this, [=](){
        if (m_currentShape != "text") {
            m_currentShape = "text";
            m_isChecked = true;
            int rectColorIndex = ConfigSettings::instance()->value("text", "color_index").toInt();
            ConfigSettings::instance()->setValue("common", "color_index", rectColorIndex);
        } else {
            m_currentShape = "";
            m_isChecked = false;
        }

        emit buttonChecked(m_isChecked, "text");
    });
    connect(colorBtn, &BigColorButton::clicked, this, [=]{
        colorBtn->setChecked(true);
        emit buttonChecked(true, "color");
    });

    connect(saveBtn,  &ToolButton::clicked, this, [=](){
        emit saveImage();
    });
    connect(listBtn, &ToolButton::clicked, this, [=] {
        bool expand = listBtn->isChecked();
        if (!m_listBtnChecked) {
            m_listBtnChecked = true;
        }
        if (m_listBtnChecked) {
            listBtn->setChecked(true);
        }
        emit buttonChecked(expand, "saveList");
    });

    connect(this, &MajToolBar::specificedSavePath, this, [=]{
        okBtn->show();
        saveBtn->hide();
        listBtn->hide();
        this->updateGeometry();
    });
    connect(okBtn, &ToolButton::clicked, this, [=]{
        emit this->saveSpecificedPath();
    });
    connect(closeBtn, &ToolButton::clicked, this, &MajToolBar::closed);
}

bool MajToolBar::isButtonChecked() {
    return m_isChecked;
}
