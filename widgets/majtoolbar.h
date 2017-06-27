#ifndef MAJTOOLBAR_H
#define MAJTOOLBAR_H

#include <QLabel>
#include <QPushButton>
#include <QHBoxLayout>
#include <QStackedWidget>

class MajToolBar : public QLabel {
    Q_OBJECT
public:
    MajToolBar(QWidget* parent = 0);
    ~MajToolBar();

signals:
    void buttonChecked(bool checked, QString type);
    void mainColorChanged(QColor currentColor);
    void saveImage();
    void showSaveTooltip(QString tooltips);
    void hideSaveTooltip();
    void shapePressed(QString shape);
    void specificedSavePath();
    void saveSpecificedPath();
    void closed();

public slots:
    void initWidgets();
    bool isButtonChecked();

private:
    QHBoxLayout* m_baseLayout;

    bool m_isChecked;
    bool m_listBtnChecked;
    QString m_currentShape;
};

#endif // MAJTOOLBAR_H
