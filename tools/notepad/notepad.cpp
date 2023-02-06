#include "notepad.h"
#include "ui_notepad.h"
#include <QtDebug>

Notepad::Notepad(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::Notepad)
{
    ui->setupUi(this);
}

Notepad::~Notepad()
{
    delete ui;
}


void Notepad::on_actionnewDocument_triggered()
{
    qDebug() << "New document";
    currentFile.clear();
    ui->textEdit->setText(QString());
}
