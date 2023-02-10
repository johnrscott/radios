#ifndef SCHEMATICEDITOR_H
#define SCHEMATICEDITOR_H

#include <QMainWindow>
#include <QGraphicsScene>
#include "resistor.h"

QT_BEGIN_NAMESPACE
namespace Ui { class MainWindow; }
QT_END_NAMESPACE

class SchematicEditor : public QMainWindow
{
    Q_OBJECT

public:
    SchematicEditor(QWidget *parent = nullptr);
    ~SchematicEditor();

private slots:
    void insert_component();

private:
    Ui::MainWindow *ui_;
    QGraphicsScene scene_;
    Resistor resistor_;

};
#endif // SCHEMATICEDITOR_H
