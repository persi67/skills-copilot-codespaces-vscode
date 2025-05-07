# نرم‌افزار "ساده" - نسخه تست Python با PyQt5
# فرم ورود + فرم امتیازدهی + ذخیره در SQLite

import sys
import sqlite3
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QMessageBox, QComboBox, QSpinBox, QTextEdit, QDateEdit
)
from PyQt5.QtCore import QDate

# اتصال به پایگاه داده
conn = sqlite3.connect("score_data.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS scores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    team TEXT,
    name TEXT,
    criteria1 INTEGER,
    criteria2 INTEGER,
    criteria3 INTEGER,
    criteria4 INTEGER,
    criteria5 INTEGER,
    notes TEXT
)
""")
conn.commit()

# فرم ورود
class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ورود مدیر")
        layout = QVBoxLayout()

        self.label = QLabel("رمز ورود:")
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)
        self.button = QPushButton("ورود")
        self.button.clicked.connect(self.check_password)

        layout.addWidget(self.label)
        layout.addWidget(self.password)
        layout.addWidget(self.button)
        self.setLayout(layout)

    def check_password(self):
        if self.password.text() == "admin123":
            self.main_window = ScoreWindow()
            self.main_window.show()
            self.close()
        else:
            QMessageBox.warning(self, "خطا", "رمز عبور اشتباه است.")

# فرم اصلی امتیازدهی
class ScoreWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("فرم امتیازدهی")
        self.resize(400, 300)
        layout = QVBoxLayout()

        self.date = QDateEdit()
        self.date.setDate(QDate.currentDate())

        self.team = QComboBox()
        self.team.addItems(["انبار", "تولید"])

        self.name = QComboBox()
        self.name.addItems(["هادی اسماعیلی", "پورعلی", "آذر پرا", "مصری",
                            "یوسف جمهیری", "آقای بازیار", "سالمی", "حیدری", "صمد", "عبدالله"])

        self.criteria1 = QSpinBox(); self.criteria1.setRange(0, 10)
        self.criteria2 = QSpinBox(); self.criteria2.setRange(0, 10)
        self.criteria3 = QSpinBox(); self.criteria3.setRange(0, 10)
        self.criteria4 = QSpinBox(); self.criteria4.setRange(0, 10)
        self.criteria5 = QSpinBox(); self.criteria5.setRange(0, 10)

        self.notes = QTextEdit()

        self.save_button = QPushButton("ذخیره")
        self.save_button.clicked.connect(self.save_data)

        layout.addWidget(QLabel("تاریخ:")); layout.addWidget(self.date)
        layout.addWidget(QLabel("تیم:")); layout.addWidget(self.team)
        layout.addWidget(QLabel("نام:")); layout.addWidget(self.name)
        layout.addWidget(QLabel("معیار 1:")); layout.addWidget(self.criteria1)
        layout.addWidget(QLabel("معیار 2:")); layout.addWidget(self.criteria2)
        layout.addWidget(QLabel("معیار 3:")); layout.addWidget(self.criteria3)
        layout.addWidget(QLabel("معیار 4:")); layout.addWidget(self.criteria4)
        layout.addWidget(QLabel("معیار 5:")); layout.addWidget(self.criteria5)
        layout.addWidget(QLabel("یادداشت:")); layout.addWidget(self.notes)
        layout.addWidget(self.save_button)

        self.setLayout(layout)

    def save_data(self):
        cursor.execute("""
        INSERT INTO scores (date, team, name, criteria1, criteria2, criteria3, criteria4, criteria5, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                self.date.date().toString("yyyy-MM-dd"),
                self.team.currentText(),
                self.name.currentText(),
                self.criteria1.value(),
                self.criteria2.value(),
                self.criteria3.value(),
                self.criteria4.value(),
                self.criteria5.value(),
                self.notes.toPlainText()
            ))
        conn.commit()
        QMessageBox.information(self, "موفق", "اطلاعات ذخیره شد.")
        self.criteria1.setValue(0)
        self.criteria2.setValue(0)
        self.criteria3.setValue(0)
        self.criteria4.setValue(0)
        self.criteria5.setValue(0)
        self.notes.clear()

# اجرای برنامه
app = QApplication(sys.argv)
window = LoginWindow()
window.show()
sys.exit(app.exec_())
