#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QGraphicsScene>

QT_BEGIN_NAMESPACE
namespace Ui { class MainWindow; }
QT_END_NAMESPACE

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    MainWindow(QWidget *parent = nullptr);
    ~MainWindow();

    void setName(const QString &name);
    QString name() const;

    void draw_circle();

private:
    Ui::MainWindow *ui;
    QGraphicsScene *scene_;
};
#endif // MAINWINDOW_H
