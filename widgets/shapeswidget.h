/*
 * Copyright (C) 2017 ~ 2017 Deepin Technology Co., Ltd.
 *
 * Maintainer: Peng Hui<penghui@deepin.com>
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

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

    enum ShapeBlurStatus {
        Drawing,
        Selected,
        Hovered,
        Normal,
    };
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
    void shapePressed(QString shape);
    void saveBtnPressed(int index);
    void requestExit();
    void menuNoFocus();

public slots:
    void updateSelectedShape(const QString &group, const QString &key, int index);
    void setCurrentShape(QString shapeType);
    void updatePenColor();
    void setPenColor(QColor color);
    void clearSelected();
    void setAllTextEditReadOnly();
    void saveActionTriggered();

    void handleDrag(QPointF oldPoint, QPointF newPoint);
    void handleRotate(QPointF pos);
    void handleResize(QPointF pos, int key);

    bool clickedOnShapes(QPointF pos);
    bool clickedOnRect(FourPoints rectPoints, QPointF pos, bool isBlurMosaic = false);
    bool clickedOnEllipse(FourPoints mainPoints, QPointF pos, bool isBlurMosaic = false);
    bool clickedOnArrow(QList<QPointF> points, QPointF pos);
    bool clickedOnLine(FourPoints mainPoints, QList<QPointF> points, QPointF pos);
    bool clickedOnText(FourPoints mainPoints, QPointF pos);
    bool rotateOnPoint(FourPoints mainPoints, QPointF pos);

    bool hoverOnShapes(Toolshape toolShape, QPointF pos);
    bool hoverOnRect(FourPoints rectPoints, QPointF pos, bool isTextBorder = false);
    bool hoverOnEllipse(FourPoints mainPoints, QPointF pos);
    bool hoverOnArrow(QList<QPointF> points, QPointF pos);
    bool hoverOnLine(FourPoints mainPoints, QList<QPointF> points, QPointF pos);
    bool hoverOnText(FourPoints mainPoints, QPointF pos);

    bool hoverOnRotatePoint(FourPoints mainPoints, QPointF pos);
    bool textEditIsReadOnly();

    void undoDrawShapes();
    void deleteCurrentShape();
    QString  getCurrentType();
    void microAdjust(QString direction);
    void setShiftKeyPressed(bool isShift);
    void updateCursorShape();

protected:
    void mousePressEvent(QMouseEvent* e);
    void mouseReleaseEvent(QMouseEvent* e);
    void mouseMoveEvent(QMouseEvent* e);
    void paintEvent(QPaintEvent *);
    void enterEvent(QEvent *e);

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

    int m_shapesIndex;
    int m_selectedIndex;
    int m_currentIndex;
    int m_hoveredIndex;
    int m_selectedOrder;
    bool m_blurEffectExist = false;
    bool m_mosaicEffectExist = false;
    QString m_currentType = "rectangle";
    QColor m_penColor;
    bool m_clearAllTextBorder = false;

    Toolshape m_currentShape;
    Toolshape m_selectedShape;
    Toolshape m_hoveredShape;

    QMap<int, TextEdit*> m_editMap;
    void updateTextRect(TextEdit* edit, QRectF newRect);
    Toolshapes m_shapes;
    MenuController* m_menuController;

    void paintImgPoint(QPainter &painter, QPointF pos, QPixmap img, bool isResize = true);
    void paintRect(QPainter &painter, FourPoints rectFPoints, int index,
                   ShapeBlurStatus  rectStatus = Normal, bool isBlur = false, bool isMosaic = false);
    void paintEllipse(QPainter &painter, FourPoints ellipseFPoints, int index,
                  ShapeBlurStatus  ovalStatus = Normal, bool isBlur = false, bool isMosaic = false);
    void paintArrow(QPainter &painter, QList<QPointF> lineFPoints,
                                  int lineWidth, bool isStraight = false);
    void paintLine(QPainter &painter, QList<QPointF> lineFPoints);
    void paintText(QPainter &painter, FourPoints rectFPoints);
};
#endif // SHAPESWIDGET_H
