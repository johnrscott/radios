#include "mainwindow.h"

#include <QApplication>

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    MainWindow w;

    w.setName("John Scott");
    w.draw_circle();
    w.show();
    return a.exec();
}
