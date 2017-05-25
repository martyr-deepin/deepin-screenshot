#ifndef FONTSIZEWIDGET_H
#define FONTSIZEWIDGET_H

#include <QLabel>
#include <QWidget>
#include <QLineEdit>
#include <QPushButton>

class Seperator : public QLabel {
    Q_OBJECT
public:
    Seperator(QWidget* parent);
    ~Seperator();
};

class FontSizeWidget : public QLabel {
    Q_OBJECT
public:
    FontSizeWidget(QWidget* parent = 0);
    ~FontSizeWidget();

    void initWidget();
    void adjustFontSize(bool add);
    void setFontSize(int fontSize);

signals:
    void fontSizeChanged(int fontSize);

private:
    QLineEdit* m_fontSizeEdit;
    QPushButton* m_addSizeBtn;
    QPushButton* m_reduceSizeBtn;
    int m_fontSize;
};
#endif // FONTSIZEWIDGET_H
