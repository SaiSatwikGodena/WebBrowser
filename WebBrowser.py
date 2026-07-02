import sys
import os
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        # locate the landing page file in the same folder as this script
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.landing_path = os.path.join(base_dir, 'landing.html')
        # ensure absolute path
        landing_url = QUrl.fromLocalFile(self.landing_path)

        self.browser = QWebEngineView()
        # load landing page at startup
        self.browser.setUrl(landing_url)
        self.setCentralWidget(self.browser)
        self.showMaximized()

        # navbar
        navbar = QToolBar()
        navbar.setStyleSheet("""QToolBar {
                                 background: #d9d9d9;
                                 spacing: 6px;
                             }
                             QToolButton {
                                 color: #12324a;
                                 background-color: rgba(135, 206, 250, 0.45);
                                 padding: 6px 10px;
                                 border-radius: 5px;
                                 border: none;
                                 font-weight: 500;
                             }
                             QToolButton:hover {
                                 background-color: rgba(135, 206, 250, 0.70);
                             }
                             QToolButton:pressed {
                                 background-color: rgba(100, 180, 240, 0.85);
                             }""")
        self.addToolBar(navbar)

        back_btn = QAction('Back', self)
        back_btn.triggered.connect(self.browser.back)
        navbar.addAction(back_btn)

        forward_btn = QAction('Forward', self)
        forward_btn.triggered.connect(self.browser.forward)
        navbar.addAction(forward_btn)

        reload_btn = QAction('Reload', self)
        reload_btn.triggered.connect(self.browser.reload)
        navbar.addAction(reload_btn)

        home_btn = QAction('Home', self)
        home_btn.triggered.connect(self.navigate_home)
        navbar.addAction(home_btn)

        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        navbar.addWidget(self.url_bar)

        # update url bar when the page changes
        self.browser.urlChanged.connect(self.update_url)

    def navigate_home(self):
        # navigate to the local landing page
        self.browser.setUrl(QUrl.fromLocalFile(self.landing_path))

    def navigate_to_url(self):
        text = self.url_bar.text().strip()
        if not text:
            return
        # fromUserInput handles adding http(s) etc. automatically
        url = QUrl.fromUserInput(text)
        self.browser.setUrl(url)

    def update_url(self, qurl):
        # show a friendly string in the address bar
        if qurl.isLocalFile():
            # show local filepath rather than file:// URI
            self.url_bar.setText(qurl.toLocalFile())
        else:
            self.url_bar.setText(qurl.toString())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    QApplication.setApplicationName('My Cool Browser')
    window = MainWindow()
    app.exec_()