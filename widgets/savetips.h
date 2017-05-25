#ifndef SAVETIPS_H
#define SAVETIPS_H

#include <QLabel>
#include <QPropertyAnimation>

class SaveTips : public QLabel {
    Q_OBJECT
    Q_PROPERTY(int tipWidth READ tipWidth WRITE setTipWidth NOTIFY tipWidthChanged)

public:
    SaveTips(QWidget* parent = 0);
    ~SaveTips();

signals:
    void tipWidthChanged(int value);

public slots:
    void setSaveText(QString text);
    void startAnimation();
    void endAnimation();

private:
    int m_tipsWidth = 0;
    int tipWidth() const;
    void setTipWidth(int tipsWidth);

    QPropertyAnimation* m_animation;
};
#endif // SAVETIPS_H
