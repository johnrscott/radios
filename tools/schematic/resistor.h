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
        qreal bound_width{width_ + 2*lead_length_ + pen_width_};
        qreal bound_height{height_ + pen_width_};
        return QRectF(bound_width/2, -bound_height/2,
                      bound_width, bound_height);
    }

    void paint(QPainter *painter, const QStyleOptionGraphicsItem *option,
               QWidget *widget) override
    {
        painter->drawRect(-width_/2, -height_/2, width_, height_);
        painter->drawLine(-width_/2, 0, -width_/2 - lead_length_, 0);
        painter->drawLine(width_/2, 0, width_/2 + lead_length_, 0);
    }
private:
    qreal pen_width_{1};
    qreal width_{50};
    qreal height_{15};
    qreal lead_length_{20};

};

#endif // RESISTOR_H
