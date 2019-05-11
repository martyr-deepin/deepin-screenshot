#ifndef PINWIDGET_H
#define PINWIDGET_H

#include <QWidget>
class QMenu;
class PinWidget : public QWidget
{
    Q_OBJECT
public:
    explicit PinWidget(QPixmap img, QWidget *parent = nullptr);
signals:

public slots:
protected:
    void mousePressEvent(QMouseEvent *event) override;
    void mouseReleaseEvent(QMouseEvent *event) override;
    void mouseMoveEvent(QMouseEvent *event) override;
    void contextMenuEvent(QContextMenuEvent *event) override;
    void keyPressEvent(QKeyEvent *event) override;
    void paintEvent(QPaintEvent *event) override;
private:
    bool m_move;
    double m_zoom;
    QPoint m_startPoint;
    QPoint m_windowPoint;
    QMenu* m_menu;
    QPixmap m_img;
private:
    void initMenu();
};

#endif // PINWIDGET_H
