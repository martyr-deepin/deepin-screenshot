#ifndef SAVEBUTTON_H
#define SAVEBUTTON_H

#include "toolbutton.h"

class SaveButton : public QPushButton {
    Q_OBJECT
public:
    SaveButton(QWidget* parent = 0);
    ~SaveButton();

signals:
    void saveAction();
    void expandSaveOption(bool expand);

private:
    ToolButton* m_saveBtn;
    ToolButton* m_listBtn;
};

#endif // SAVEBUTTON_H
