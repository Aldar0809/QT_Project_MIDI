from PyQt5.QtWidgets import QApplication, QMainWindow, QListWidgetItem
from PyQt5.QtGui import QMovie
from datetime import datetime
from PyQt5.QtCore import Qt
from PyQt5 import uic
import sqlite3
import sys
import os
from player import player_m
from recorder import record


fname = 'recorded.wav'
sec = 10
values = []
flag = ''

# Подключение к БД
con = sqlite3.connect("audio.db")

# Создание класса AnotherWindow - он отвечает за настройки


class AnotherWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('secondform.ui', self)

        global fname, sec

        self.setFixedSize(430, 330)
        self.setWindowTitle('Настройки')

        self.pushButton.clicked.connect(self.run)

        self.line_fname.setText(fname)
        self.line_time_rec.setText(str(sec))

    def run(self):
        global fname, sec

        fname = self.line_fname.text()
        sec = self.line_time_rec.text()

        self.close()


# Создание класса HelpWidget - он помогает


class HelpWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('helpform.ui', self)

        self.setFixedSize(410, 360)
        self.setWindowTitle('Помощь')


# Создание наиглавнейшего класса MyWindow


class MyWindow(QMainWindow):
    def __init__(self):
        global values
        super().__init__()
        uic.loadUi('mainform.ui', self)

        self.label.setObjectName('label')

        # Integrate QMovie to the label and initiate the GIF
        self.movie = QMovie("skeleton-dance_min.gif")
        self.label.setMovie(self.movie)
        self.movie.start()

        self.btn_stngs.clicked.connect(self.show_second_window)
        self.help.clicked.connect(self.show_help_window)

        self.btn_dlt.clicked.connect(self.delete_file)
        self.clr_log.clicked.connect(self.clear_logs)

        self.listWidget.itemClicked.connect(self.on_clicked)
        self.listWidget.itemDoubleClicked.connect(self.on_clicked_double)

        values = [f for f in os.listdir('Records') if os.path.isfile(os.path.join('Records', f))]
        for i in values:
            self.listWidget.addItem(QListWidgetItem(i))

        self.setFixedSize(840, 550)
        self.setWindowTitle('Главное меню')

    # Это когда нажимаешь на элемент в listWidget
    def on_clicked(self, item):
        global flag
        flag = item.text()

    def on_clicked_double(self, item):
        print(item.text())
        player_m(f"Records\\{item.text()}")

    # Создание функции для удалении логов

    def clear_logs(self):
        cur = con.cursor()

        cur.execute("DELETE FROM logs")
        con.commit()

        self.logs.clear()

    # Функция удаления файла

    def delete_file(self):
        global fname, values, flag

        if len(flag) > 0:
            fname = flag
            flag = ''

        file_path = f"Records\\{fname}"
        text = f"REMOVED FILE name: '{fname}'"

        cur = con.cursor()

        if os.path.exists(file_path):
            os.remove(file_path)
            cur.execute("INSERT INTO logs (value, filename) VALUES"
                        " (?, ?);", (text, fname)).fetchall()

            con.commit()

            self.logs.append(text)

            self.listWidget.takeItem(values.index(fname))
            values.remove(fname)

        else:
            self.logs.append('NOT EXIST FILE')

    # Показ второго окна

    def show_second_window(self):
        self.w = AnotherWindow()
        self.w.show()

    # Показ вспомогательного окна

    def show_help_window(self):
        self.h = HelpWidget()
        self.h.show()

    # При нажатии F или G активируется эта функция да

    def keyPressEvent(self, event):
        global fname, sec, values

        cur = con.cursor()

        time_now = datetime.today()

        if event.key() == Qt.Key_F:
            record(f"Records\\{fname}", float(sec))

            text = f"time: '{time_now}'; RECORDED name: '{fname}'; "

            cur.execute("INSERT INTO logs (value, filename) VALUES"
                        " (?, ?);", (text, fname)).fetchall()

            con.commit()

            if fname not in values:
                self.listWidget.addItem(QListWidgetItem(fname))
                values.append(fname)

            self.logs.append(text)

        elif event.key() == Qt.Key_G:
            if os.path.isfile(f"Records\\{fname}") is not True:
                self.logs.append('FILE NOT EXIST')
            else:
                player_m(f"Records\\{fname}")

                text = f"time: '{time_now}'; PLAYED name: '{fname}'; "

                cur.execute("INSERT INTO logs (value, filename) VALUES"
                            " (?, ?);", (text, fname)).fetchall()

                con.commit()

                self.logs.append(text)


# Показ программы

if __name__ == '__main__':
    appl = QApplication(sys.argv)
    ex = MyWindow()
    ex.show()
    sys.exit(appl.exec())

con.close()
