#include "savebutton.h"

#include "utils/baseutils.h"
#include <QHBoxLayout>

const QSize TOOL_SAVE_BTN = QSize(32, 22);
const QSize SAVE_BTN = QSize(21, 22);
const QSize LIST_BTN = QSize(11, 22);

SaveButton::SaveButton(QWidget *parent)
    : QPushButton(parent) {
    setFixedSize(TOOL_SAVE_BTN);
    setStyleSheet(getFileContent(":/resources/qss/toolsavebutton.qss"));
    m_saveBtn = new ToolButton(this);
    m_saveBtn->setObjectName("SaveBtn");
    m_saveBtn->setFixedSize(SAVE_BTN);
    m_listBtn = new ToolButton(this);
    m_listBtn->setObjectName("ListBtn");
    m_listBtn->setFixedSize(LIST_BTN);

    QHBoxLayout* saveLayout = new QHBoxLayout();
    saveLayout->setMargin(0);
    saveLayout->setSpacing(0);
    saveLayout->addWidget(m_saveBtn);
    saveLayout->addWidget(m_listBtn);

    setLayout(saveLayout);

    connect(m_saveBtn, &ToolButton::clicked, this,
            &SaveButton::saveAction);
    connect(m_listBtn, &ToolButton::clicked, this, [=](){
        bool isChecked = m_listBtn->isChecked();
        emit  expandSaveOption(isChecked);
    });
}

SaveButton::~SaveButton() {
}
