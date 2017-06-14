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

public slots:
    void switchContent(QString shapeType);
    void setSaveOption(int saveOption);
    void setSaveQualityIndex(int saveQuality);
    int    getSaveQualityIndex();
    void updateColor(QColor color);

signals:
    void currentColorChanged(QColor color);
    void shapeChanged();
    void saveAction();
    void showSaveTip(QString tips);
    void hideSaveTip();
    void  saveBtnPressed(int index = 0);
    void defaultColorIndexChanged(int index);

private:
    int m_lineWidth;
    int m_saveQuality;
    QString m_currentType;

    QLabel* m_rectLabel;
    QLabel* m_arrowLabel;
    QLabel* m_lineLabel;
    QLabel* m_textLabel;
    QLabel* m_colorLabel;
    QLabel* m_saveLabel;
};
#endif // SUBTOOLBAR_H
