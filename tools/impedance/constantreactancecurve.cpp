#include "constantreactancecurve.h"

ConstantReactanceCurve::ConstantReactanceCurve(qreal reactance)
    : reactance_{reactance}
{ }


QPainterPath ConstantReactanceCurve::boundary_path() const{
    return boundary_path_;
}

void ConstantReactanceCurve::set_boundary_path(const QPainterPath &boundaryPath){
    boundary_path_ = boundaryPath;
    update();
}
