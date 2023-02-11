#include "schematiceditor.h"
#include "ui_schematiceditor.h"

SchematicEditor::SchematicEditor(QWidget *parent)
    : QMainWindow(parent)
    , ui_(new Ui::MainWindow)
{
    ui_->setupUi(this);
    connect(ui_->actionInsert, &QAction::triggered, this, &SchematicEditor::insert_component);
    connect(ui_->actionNew, &QAction::triggered, this, &SchematicEditor::set_resistor_pos);
    ui_->graphicsView->setScene(&scene_);
}

SchematicEditor::~SchematicEditor()
{
    delete ui_;
}

void SchematicEditor::insert_component() {
    scene_.addItem(&resistor_);
}

void SchematicEditor::set_resistor_pos() {
    resistor_.setPos(150,150);
}
