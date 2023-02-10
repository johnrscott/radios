#ifndef RESISTOR_H
#define RESISTOR_H

#include <QGraphicsItem>
#include <QRect>
#include <QPainter>

class Resistor : public QGraphicsItem
{
public:
    Resistor();
    QRectF boundingRect() const override
    {
        qreal penWidth = 1;
        return QRectF(-10 - penWidth / 2, -10 - penWidth / 2,
                      20 + penWidth, 20 + penWidth);
    }

    void paint(QPainter *painter, const QStyleOptionGraphicsItem *option,
               QWidget *widget) override
    {
        painter->drawRoundedRect(-10, -10, 20, 20, 5, 5);
    }
};

#endif // RESISTOR_H
