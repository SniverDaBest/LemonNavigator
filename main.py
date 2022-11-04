from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtWebEngineWidgets import *
from PyQt6.QtPrintSupport import *
from PyQt6.QtNetwork import *
from tkinter import Tk
from os import system as runCommand
import tkinter as tk
import sys

def showHelp():
    window = Tk()
    window.geometry("255x50")
    window.title("Help")

    txt = tk.Label(window,text="Lemon Navigator v1.0\nTip: Double Click the tab bar to make a new tab!")
    txt.pack(side="left")

    window.mainloop()

def showCL():
    window = Tk()
    window.geometry("500x500")
    window.title("Changelog")

    txt = tk.Label(window, text=
    """v1.0 (The Original)
    ____________________________
    This was the original version! (Well besides the betas...)
    """)
    txt.pack(side="top")

    window.mainloop()

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.tabs = QTabWidget()

        self.tabs.setDocumentMode(True)

        self.tabs.tabBarDoubleClicked.connect(self.tab_open_doubleclick)
        self.tabs.currentChanged.connect(self.current_tab_changed)

        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_current_tab)
        self.setCentralWidget(self.tabs)

        self.status = QStatusBar()
        self.setStatusBar(self.status)

        navtb = QToolBar("Navigation")
        self.addToolBar(navtb)

        back_btn = QAction("<", self)
        back_btn.triggered.connect(lambda: self.tabs.currentWidget().back())
        navtb.addAction(back_btn)

        next_btn = QAction(">", self)
        next_btn.triggered.connect(lambda: self.tabs.currentWidget().forward())
        navtb.addAction(next_btn)

        home_btn = QAction("Home", self)
        home_btn.triggered.connect(self.navigate_home)
        navtb.addAction(home_btn)

        reload_btn = QAction("Refresh", self)
        reload_btn.triggered.connect(lambda: self.tabs.currentWidget().reload())
        navtb.addAction(reload_btn)

        help_btn = QAction("?", self)
        help_btn.triggered.connect(lambda: showHelp())
        navtb.addAction(help_btn)

        navtb.addSeparator()

        self.urlbar = QLineEdit()
        self.urlbar.returnPressed.connect(self.navigate_to_url)

        navtb.addWidget(self.urlbar)

        navtb.addSeparator()

        changelog_btn = QAction("CL", self)
        changelog_btn.setStatusTip("Opens the changelog")
        changelog_btn.triggered.connect(lambda: showCL())
        navtb.addAction(changelog_btn)

        self.add_new_tab(QUrl("https://www.ecosia.org/"), 'Homepage')
        self.show()

        self.setWindowTitle("Lemon Navigator")

    def add_new_tab(self, qurl = None, label ="Blank"):
        if qurl is None:
            qurl = QUrl('https://www.ecosia.org/')
 
        browser = QWebEngineView()
        browser.setUrl(qurl)

        i = self.tabs.addTab(browser, label)
        self.tabs.setCurrentIndex(i)

        browser.urlChanged.connect(lambda qurl, browser = browser:
                                   self.update_urlbar(qurl, browser))
        browser.loadFinished.connect(lambda _, i = i, browser = browser:
                                     self.tabs.setTabText(i, browser.page().title()))

    def tab_open_doubleclick(self, i):
        if i == -1:
            self.add_new_tab()

    def current_tab_changed(self, i):
        qurl = self.tabs.currentWidget().url()

        self.update_urlbar(qurl, self.tabs.currentWidget())

        self.update_title(self.tabs.currentWidget())

    def close_current_tab(self, i):
        if self.tabs.count() < 2:
            return

        self.tabs.removeTab(i)

    def update_title(self, browser):
        if browser != self.tabs.currentWidget():
            return

        title = self.tabs.currentWidget().page().title()
        self.setWindowTitle("% s - Lemon Navigator" % title)

    def navigate_home(self):
        self.tabs.currentWidget().setUrl(QUrl("https://www.ecosia.org/"))

    def navigate_to_url(self):
        q = QUrl(self.urlbar.text())

        if q.scheme() == "":
            q.setScheme("http")

        self.tabs.currentWidget().setUrl(q)

    def update_urlbar(self, q, browser = None):
        if browser != self.tabs.currentWidget():
            return

        self.urlbar.setText(q.toString())
        self.urlbar.setCursorPosition(0)

while __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("Lemon Navigator")
    window = MainWindow()
    sys.exit(app.exec())
