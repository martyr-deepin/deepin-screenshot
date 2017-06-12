#ifndef TOOLBUTTON_H
#define TOOLBUTTON_H

#include <QPushButton>

class ToolButton : public QPushButton {
    Q_OBJECT
public:
    ToolButton(QWidget* parent = 0) {
        Q_UNUSED(parent);
        setFixedSize(32, 26);
        setCheckable(true);
        m_tips = "";
    }
    ~ToolButton(){}

public slots:
    void setTips(QString tips) {
        m_tips = tips;
    }

    QString getTips() {
        return m_tips;
    }

signals:
    void onEnter();
    void onExist();

protected:
    void enterEvent(QEvent* e) {
        emit onEnter();
        QPushButton::enterEvent(e);
    }

    void leaveEvent(QEvent* e) {
        emit onExist();
        QPushButton::leaveEvent(e);
    }

private:
    QString m_tips;

};
#endif // TOOLBUTTON_H
