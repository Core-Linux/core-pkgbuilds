#include <QProcess>
#include "widget.h"
#include "./ui_widget.h"

Widget::Widget(QWidget *parent)
    : QWidget(parent)
    , ui(new Ui::Widget)
{
    ui->setupUi(this);
    // Tamaño fijo para la ventana
    // setFixedSize(600, 400);
    setWindowFlags(windowFlags() & ~Qt::WindowMaximizeButtonHint);
    setFixedSize(width(), height());

    // Botones más grandes
    ui->pushButton->setFixedSize(150, 50);
    ui->pushButton_2->setFixedSize(150, 50);

    // Fuente más grande
    QFont font = ui->pushButton->font();
    font.setPointSize(14);
    ui->pushButton->setFont(font);
    ui->pushButton_2->setFont(font);

}

Widget::~Widget()
{
    delete ui;
}

void Widget::on_pushButton_2_clicked()
{
    // QProcess::startDetached("calamares", {"-d"});
    QProcess::startDetached("pkexec calamares");
    close();
}

void Widget::on_pushButton_clicked()
{
    close();
}
