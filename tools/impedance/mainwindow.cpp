#include "mainwindow.h"
#include "ui_mainwindow.h"

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    ui->setupUi(this);
    scene_ = new QGraphicsScene(this);
    ui->graphicsView->setScene(scene_);
}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::setName(const QString & name)
{
    ui->lineEdit->setText(name);
}

void MainWindow::draw_circle()
{
    scene_->addEllipse(-100, -100, 300, 60);

}

QString MainWindow::name() const
{
    return ui->lineEdit->text();
}
