#ifndef SUBTOOLBAR_H
#define SUBTOOLBAR_H

#include <QStackedWidget>
#include <QLabel>

class SubToolBar : public QStackedWidget{
    Q_OBJECT
public:
    SubToolBar(QWidget* parent=0);
    ~SubToolBar();

    void initWidget();
    void initRectLabel();
    void initArrowLabel();
    void initLineLabel();
    void initTextLabel();
    void initColorLabel();
    void initSaveLabel();

    void switchContent(QString shapeType);

signals:
    void setCurrentColor(QColor color);
    void setSaveBtn(int saveOption);

private:
    int m_lineWidth;

    QLabel* m_rectLabel;
    QLabel* m_arrowLabel;
    QLabel* m_lineLabel;
    QLabel* m_textLabel;
    QLabel* m_colorLabel;
    QLabel* m_saveLabel;
};
#endif // SUBTOOLBAR_H
