#include "mainwindow.h"

#include <QApplication>

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    MainWindow w;

    w.setName("John Scott");

    for (qreal resistance{0.1}; resistance < 100; resistance *= 1.414) {
        w.draw_constant_resistance_circle(resistance);
    }
    w.show();
    return a.exec();
}
