#ifndef CONSTANTREACTANCECURVE_H
#define CONSTANTREACTANCECURVE_H

#include <QGraphicsItem>

class ConstantReactanceCurve : public QGraphicsItem
{
public:
    ConstantReactanceCurve(qreal reactance);

    QPainterPath boundary_path() const;
    void set_boundary_path(const QPainterPath &boundaryPath);
private:
    qreal reactance_;
    QPainterPath boundary_path_;
};

#endif // CONSTANTREACTANCECURVE_H
