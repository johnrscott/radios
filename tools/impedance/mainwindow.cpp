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

void MainWindow::draw_constant_resistance_circle(qreal resistance)
{
    qreal centre_x{resistance/(resistance+1)};
    qreal centre_y{0};
    qreal radius{1/(resistance + 1)};
    qreal x{centre_x - radius};
    qreal y{centre_y - radius};
    qreal length{2*radius};
    scene_->addEllipse(700*x, 700*y, 700*length, 700*length);
}

QString MainWindow::name() const
{
    return ui->lineEdit->text();
}
