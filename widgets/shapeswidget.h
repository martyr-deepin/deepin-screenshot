#ifndef SHAPESWIDGET_H
#define SHAPESWIDGET_H

#include <QFrame>
#include <QMouseEvent>

#include "utils/shapesutils.h"
#include "utils/baseutils.h"
#include "textedit.h"
#include "controller/menucontroller.h"

class ShapesWidget : public QFrame {
    Q_OBJECT
public:
    ShapesWidget(QWidget* parent = 0);
    ~ShapesWidget();

    enum ClickedKey {
        First,
        Second,
        Third,
        Fourth,
        Fifth,
        Sixth,
        Seventh,
        Eighth,
    };

signals:
    void reloadEffectImg(QString effect);
    void requestScreenshot();

public slots:
    void setCurrentShape(QString shapeType);
    void setPenColor(QColor color);
    void clearSelected();
    void setAllTextEditReadOnly();

    void handleDrag(QPointF oldPoint, QPointF newPoint);
    void handleRotate(QPointF pos);
    void handleResize(QPointF pos, int key);

    bool clickedOnShapes(QPointF pos);
    bool clickedOnRect(FourPoints rectPoints, QPointF pos, bool isBlurMosaic = false);
    bool clickedOnEllipse(FourPoints mainPoints, QPointF pos, bool isBlurMosaic = false);
    bool clickedOnArrow(QList<QPointF> points, QPointF pos);
    bool clickedOnLine(FourPoints mainPoints, QList<QPointF> points, QPointF pos);

    bool rotateOnPoint(FourPoints mainPoints, QPointF pos);

    bool hoverOnShapes(Toolshape toolShape, QPointF pos);
    bool hoverOnRect(FourPoints rectPoints, QPointF pos);
    bool hoverOnEllipse(FourPoints mainPoints, QPointF pos);
    bool hoverOnArrow(QList<QPointF> points, QPointF pos);
    bool hoverOnLine(FourPoints mainPoints, QList<QPointF> points, QPointF pos);
    bool hoverOnRotatePoint(FourPoints mainPoints, QPointF pos);

    void deleteCurrentShape();
    QString  getCurrentType();
    void setTextEditGrabKeyboard();
    void microAdjust(QString direction);

protected:
    void mousePressEvent(QMouseEvent* e);
    void mouseReleaseEvent(QMouseEvent* e);
    void mouseMoveEvent(QMouseEvent* e);
    void paintEvent(QPaintEvent *);
    bool eventFilter(QObject *watched, QEvent *event);

private:
    QPointF m_pos1 = QPointF(0, 0);
    QPointF m_pos2 = QPointF(0, 0);
    QPointF m_pos3, m_pos4;
    QPointF m_pressedPoint;
    QPointF m_movingPoint;

    bool m_isRecording;
    bool m_isMoving;
    bool m_isSelected;
    bool m_isPressed;
    bool m_isHovered;
    bool m_isRotated;
    bool m_isResize;
    bool m_isShiftPressed;
    bool m_editing;

    ResizeDirection m_resizeDirection;
    ClickedKey m_clickedKey;

    int m_selectedIndex;
    bool m_blurEffectExist = false;
    bool m_mosaicEffectExist = false;
    QString m_currentType = "rectangle";
    QColor m_penColor;

    DiagPointsList m_diagPointsList;
    DiagPoints m_currentDiagPoints;
    DiagPoints m_currentHoverDiagPoints;
    DiagPoints m_currentSelectedDiagPoints;

    Toolshape m_currentShape;
    Toolshape m_selectedShape;
    Toolshape m_hoveredShape;

    QMap<int, TextEdit*> m_editMap;
    void updateTextRect(TextEdit* edit, QRectF newRect);
    Toolshapes m_shapes;
    MenuController* m_menuController;

    void paintImgPoint(QPainter &painter, QPointF pos, QPixmap img, bool isResize = true);
    void paintRect(QPainter &painter, FourPoints rectFPoints, int index,
                               bool isBlur = false, bool isMosaic = false);
    void paintEllipse(QPainter &painter, FourPoints ellipseFPoints, int index,
                                  bool isBlur = false, bool isMosaic = false);
    void paintArrow(QPainter &painter, QList<QPointF> lineFPoints,
                                  int lineWidth, bool isStraight = false);
    void paintLine(QPainter &painter, QList<QPointF> lineFPoints);
    void paintText(QPainter &painter, FourPoints rectFPoints);
};
#endif // SHAPESWIDGET_H
