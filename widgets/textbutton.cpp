#include "textbutton.h"

#include "utils/baseutils.h"
#include "utils/configsettings.h"

TextButton::TextButton(int num, QWidget *parent)
    : QPushButton(parent) {
    setStyleSheet(getFileContent(":/resources/qss/textbutton.qss"));
    m_fontsize = num;
    setText(QString("%1").arg(m_fontsize));

     setFixedSize(20, 22);
    setCheckable(true);

    connect(this, &TextButton::clicked, this, [=]{
        if (this->isChecked()) {
            ConfigSettings::instance()->setValue("text", "fontsize", m_fontsize);
        }
    });
}

TextButton::~TextButton() {}