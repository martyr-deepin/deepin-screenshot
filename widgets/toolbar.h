#ifndef TOOLBAR_H
#define TOOLBAR_H

#include <QLabel>
#include <QPainter>
#include <DBlurEffectWidget>
#include <QEvent>
#include <QLabel>
#include <QDebug>

#include "majtoolbar.h"
#include "subtoolbar.h"

DWIDGET_USE_NAMESPACE

class ToolBarWidget : public DBlurEffectWidget {
    Q_OBJECT
public:
    ToolBarWidget(QWidget* parent = 0);
    ~ToolBarWidget();

signals:
    void buttonChecked(QString shapeType);
    void expandChanged(bool expand,  QString shapeType);
    void colorChanged(QColor color);
    void saveImage();
    void shapePressed(QString tool);
    void saveBtnPressed(int index = 0);
    void saveSpecifiedPath();
    void closed();

public slots:
    bool isButtonChecked();
    void setExpand(bool expand, QString shapeType);
    void specifiedSavePath();

protected:
    void paintEvent(QPaintEvent *e);

private:
    MajToolBar* m_majToolbar;
    QLabel* m_hSeperatorLine;
    SubToolBar* m_subToolbar;

    bool  m_expanded;
};

class ToolBar : public QLabel {
    Q_OBJECT
public:
    ToolBar(QWidget* parent = 0);
    ~ToolBar();

signals:
    void heightChanged();
    void buttonChecked(QString shape);
    void updateColor(QColor color);
    void requestSaveScreenshot();
    void shapePressed(QString tool);
    void saveBtnPressed(int index = 0);
    void saveSpecifiedPath();
    void closed();

public slots:
    bool isButtonChecked();
    void setExpand(bool expand, QString shapeType);
    void showAt(QPoint pos);
    void specificedSavePath();

protected:
    void paintEvent(QPaintEvent *e);
    void enterEvent(QEvent *e);

private:
    ToolBarWidget* m_toolbarWidget;

    bool m_expanded;
};
#endif // TOOLBAR_H
