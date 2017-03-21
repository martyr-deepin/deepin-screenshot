#ifndef TOPTIPS_H
#define TOPTIPS_H

#include <QLabel>

class TopTips : public QLabel {
    Q_OBJECT
public:
    TopTips(QWidget* parent = 0);
    ~TopTips();

public slots:
    void setContent(QString widthXHeight);
    void updateTips(QPoint pos, QString text);
};
#endif // TOPTIPS_H
