#include "schematiceditor.h"
#include "ui_schematiceditor.h"

SchematicEditor::SchematicEditor(QWidget *parent)
    : QMainWindow(parent)
    , ui_(new Ui::MainWindow)
{
    ui_->setupUi(this);
    ui_->graphicsView->setScene(&scene_);

    scene_.addItem(&resistor_);
}

SchematicEditor::~SchematicEditor()
{
    delete ui_;
}
