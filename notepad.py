from PyQt5.QtGui import QIcon, QFontDatabase, QFont
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPlainTextEdit, QStatusBar, QToolBar,
                             QMenu, QAction, QMessageBox, QFileDialog)
from PyQt5.QtCore import QSize
from PyQt5.QtPrintSupport import QPrintDialog

import os
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.editor = QPlainTextEdit()
        self.setCentralWidget(self.editor)

        font = QFontDatabase.systemFont(QFontDatabase.FixedFont)
        font.setPointSize(12)
        self.editor.setFont(font)

        self.path = None

        status = QStatusBar()
        self.setStatusBar(status)
        
        toolBar = QToolBar()
        toolBar.setIconSize(QSize(14, 14))
        self.addToolBar(toolBar)

        menu_bar = self.menuBar()
        dosya_menu = menu_bar.addMenu("Dosya")
        ekle_menu = menu_bar.addMenu("Ekle")

        self.create_action("Dosya Aç", dosya_menu, self.dosya_ac_def, "Ctrl+O",
                           "Farklı Bir Text Dosyasını, My Notepad App Dosyanıza Aktarmanızı Sağlar", toolBar)
        self.create_action("Kaydet", dosya_menu, self.kaydet_def, "Ctrl+S",
                           "Dosyanızı Varsayılan Dosyanın Üzerine Kaydetmenizi Sağlar", toolBar)
        self.create_action("Farklı Kaydet", dosya_menu, self.farkli_kaydet_def, None,
                           "Dosyanızı İstediğiniz Dizine Kaydetmenizi Sağlar", toolBar)
        self.create_action("Yazdır", dosya_menu, self.yazdir_def, "Ctrl+P",
                           "Dosyanızı Yazdırmanızı Sağlar", None)

        self.create_action("Geri Al", ekle_menu, self.editor.undo, "Ctrl+Z",
                           "Dosya Üzerinde Yaptığınız Son İşlemi Geri Almanızı Sağlar", toolBar)
        self.create_action("İleri Al", ekle_menu, self.editor.redo, "Ctrl+Y",
                           "Dosya Üzerinde Geri Aldığınız Son İşlemi Tekrar Yapmanızı Sağlar", toolBar)
        self.create_action("Kes", ekle_menu, self.editor.cut, "Ctrl+X",
                           "Dosya Üzerindeki Seçilen Kısımları Kesmenizi Sağlar", toolBar)
        self.create_action("Kopyala", ekle_menu, self.editor.copy, "Ctrl+C",
                           "Dosya Üzerindeki Seçilen Kısımları Kopyalamanızı Sağlar", toolBar)
        self.create_action("Yapıştır", ekle_menu, self.editor.paste, "Ctrl+V",
                           "Kopyalanan ya da Kesilen Öğeyi Dosya Üzerine Yapıştırır", toolBar)
        self.create_action("Hepsini Seç", ekle_menu, self.editor.selectAll, "Ctrl+A",
                           "Dosya Üzerindeki Tüm Verilerin Seçilmesini Sağlar", toolBar)

        self.basligi_guncelle()
        self.setGeometry(100, 100, 500, 500)
        self.show()
        
    def create_action(self, text, menu, slot, shortcut=None, status_tip=None, tool_bar=None):
        action = QAction(QIcon(os.path.join("img", text.format("utf-8").lower().replace(" ", "_") + ".png")), text, self)
        if shortcut:
            action.setShortcut(shortcut)
        if status_tip:
            action.setStatusTip(status_tip)
        action.triggered.connect(slot)
        menu.addAction(action)
        if tool_bar:
            tool_bar.addAction(action)

    def hata_mesaj(self, mesaj):
        hata = QMessageBox()
        hata.setText(mesaj)
        hata.setIcon(QMessageBox.Critical)
        hata.show()
        
    def basligi_guncelle(self):
        self.setWindowTitle("{} - My Notepad App".format(os.path.basename(self.path) if self.path else "Untitled"))

    def dosya_ac_def(self):
        path, _ = QFileDialog.getOpenFileName(self, "Dosya Aç", "", "Text Dosyaları (*.txt)")
        if path:
            try:
                with open(path, "r") as file:
                    text = file.read()
                    self.editor.setPlainText(text)
                    self.path = path
                    self.basligi_guncelle()
            except Exception as e:
                self.hata_mesaj(str(e))

    def kaydet_def(self):
        if self.path is None:
            self.farkli_kaydet_def()
            return
        text = self.editor.toPlainText()
        try:
            with open(self.path, "w") as file:
                file.write(text)
        except Exception as e:
            self.hata_mesaj(str(e))

    def farkli_kaydet_def(self):
        path, _ = QFileDialog.getSaveFileName(self, "Farklı Kaydet", "", "Text Dosyası (*.txt)")
        if path:
            text = self.editor.toPlainText()
            try:
                with open(path, "w") as file:
                    file.write(text)
                    self.path = path
                    self.basligi_guncelle()
            except Exception as e:
                self.hata_mesaj(str(e))

    def yazdir_def(self):
        mesaj = QPrintDialog()
        if mesaj.exec_():
            self.editor.print_(mesaj.printer())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setApplicationName("My Notepad App")

    window = MainWindow()
    app.exec_()
