#include "schematiceditor.h"
#include "ui_schematiceditor.h"

SchematicEditor::SchematicEditor(QWidget *parent)
    : QMainWindow(parent)
    , ui_(new Ui::MainWindow)
{
    ui_->setupUi(this);
    connect(ui_->actionInsert, &QAction::triggered, this, &SchematicEditor::insert_component);
    ui_->graphicsView->setScene(&scene_);
}

SchematicEditor::~SchematicEditor()
{
    delete ui_;
}

void SchematicEditor::insert_component() {
    scene_.addItem(&resistor_);
}
