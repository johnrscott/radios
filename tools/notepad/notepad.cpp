#include "notepad.h"
#include "ui_notepad.h"
#include <QFileDialog>
#include <QFile>
#include <QMessageBox>
#include <QTextStream>

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


void Notepad::on_actionNew_triggered()
{
    currentFile.clear();
    ui->textEdit->setText(QString());
}

void Notepad::on_actionOpen_triggered()
{
    QString fileName = QFileDialog::getOpenFileName(this, "Open the file");
    if (fileName.isEmpty())
        return;
    QFile file(fileName);
    currentFile = fileName;
    if (!file.open(QIODevice::ReadOnly | QFile::Text)) {
        QMessageBox::warning(this, "Warning", "Cannot open file: " + file.errorString());
        return;
    }
    setWindowTitle(fileName);
    QTextStream in(&file);
    QString text = in.readAll();
    ui->textEdit->setText(text);
    file.close();
}

