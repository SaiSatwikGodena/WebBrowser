import sys
import os
import json
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtGui import QIcon
from bookmarks_manager import BookmarksManager


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle('My Cool Browser')
        self.setGeometry(0, 0, 1200, 800)
        self.showMaximized()

        # locate the landing page file
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.landing_path = os.path.join(self.base_dir, 'landing.html')
        self.landing_url = QUrl.fromLocalFile(self.landing_path)

        # bookmarks manager
        self.bookmarks_mgr = BookmarksManager(self.base_dir)

        # central layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        central_widget.setLayout(layout)

        # navbar
        navbar = QToolBar('Navigation')
        navbar.setStyleSheet("""QToolBar {
                                 background: #d9d9d9;
                                 spacing: 6px;
                                 padding: 6px;
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
                             }
                             QLineEdit {
                                 padding: 4px;
                                 border-radius: 5px;
                                 border: 1px solid #ccc;
                             }""")
        self.addToolBar(navbar)

        # back / forward / reload / home buttons
        back_btn = QAction('← Back', self)
        back_btn.triggered.connect(self.browser_back)
        navbar.addAction(back_btn)

        forward_btn = QAction('→ Forward', self)
        forward_btn.triggered.connect(self.browser_forward)
        navbar.addAction(forward_btn)

        reload_btn = QAction('⟳ Reload', self)
        reload_btn.triggered.connect(self.browser_reload)
        navbar.addAction(reload_btn)

        home_btn = QAction('⌂ Home', self)
        home_btn.triggered.connect(self.navigate_home)
        navbar.addAction(home_btn)

        navbar.addSeparator()

        # URL bar
        self.url_bar = QLineEdit()
        self.url_bar.setPlaceholderText('Enter URL or search...')
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        self.url_bar.setMaximumWidth(600)
        navbar.addWidget(self.url_bar)

        # bookmark current page button
        bookmark_btn = QAction('★ Bookmark', self)
        bookmark_btn.triggered.connect(self.bookmark_current_page)
        navbar.addAction(bookmark_btn)

        navbar.addSeparator()

        # new tab button
        new_tab_btn = QAction('+ New Tab', self)
        new_tab_btn.triggered.connect(self.new_tab)
        navbar.addAction(new_tab_btn)

        # bookmarks bar
        bookmarks_bar = QToolBar('Bookmarks')
        bookmarks_bar.setStyleSheet("""QToolBar {
                                       background: #e8e8e8;
                                       spacing: 4px;
                                       padding: 4px;
                                   }
                                   QToolButton {
                                       color: #12324a;
                                       background-color: transparent;
                                       padding: 4px 8px;
                                       border-radius: 4px;
                                       border: none;
                                       font-size: 12px;
                                   }
                                   QToolButton:hover {
                                       background-color: rgba(135, 206, 250, 0.50);
                                   }""")
        self.addToolBar(bookmarks_bar)
        self.bookmarks_bar = bookmarks_bar
        self.refresh_bookmarks_bar()

        # tabs widget
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.tabs.currentChanged.connect(self.on_tab_changed)
        layout.addWidget(self.tabs)

        # create first tab
        self.new_tab()

    def new_tab(self, url=None):
        """Create a new tab and optionally navigate to a URL."""
        browser = QWebEngineView()
        if url:
            browser.setUrl(url)
        else:
            browser.setUrl(self.landing_url)

        # connect signals
        browser.urlChanged.connect(self.on_url_changed)
        browser.loadProgress.connect(lambda p: self.update_tab_title(browser, p))

        tab_index = self.tabs.addTab(browser, 'New Tab')
        self.tabs.setCurrentIndex(tab_index)
        return browser

    def close_tab(self, index):
        """Close a tab at the given index."""
        if self.tabs.count() > 1:
            self.tabs.removeTab(index)
        else:
            # if only one tab, replace it with a blank landing page
            self.tabs.widget(0).setUrl(self.landing_url)

    def on_tab_changed(self, index):
        """Update URL bar when switching tabs."""
        if index >= 0:
            browser = self.tabs.widget(index)
            if browser:
                self.on_url_changed(browser.url())

    def on_url_changed(self, qurl):
        """Update URL bar when page loads."""
        if self.tabs.currentWidget():
            if qurl.isLocalFile():
                self.url_bar.setText(qurl.toLocalFile())
            else:
                self.url_bar.setText(qurl.toString())

    def update_tab_title(self, browser, progress):
        """Update tab title based on page title or progress."""
        for i in range(self.tabs.count()):
            if self.tabs.widget(i) == browser:
                if progress < 100:
                    self.tabs.setTabText(i, f'Loading... {progress}%')
                else:
                    title = browser.page().title()
                    if not title:
                        url = browser.url()
                        title = url.host() if not url.isLocalFile() else 'New Tab'
                    self.tabs.setTabText(i, title[:30])

    def get_current_browser(self):
        """Get the currently active browser widget."""
        return self.tabs.currentWidget()

    def browser_back(self):
        browser = self.get_current_browser()
        if browser:
            browser.back()

    def browser_forward(self):
        browser = self.get_current_browser()
        if browser:
            browser.forward()

    def browser_reload(self):
        browser = self.get_current_browser()
        if browser:
            browser.reload()

    def navigate_home(self):
        browser = self.get_current_browser()
        if browser:
            browser.setUrl(self.landing_url)

    def navigate_to_url(self):
        text = self.url_bar.text().strip()
        if not text:
            return
        url = QUrl.fromUserInput(text)
        browser = self.get_current_browser()
        if browser:
            browser.setUrl(url)

    def bookmark_current_page(self):
        """Add current page to bookmarks."""
        browser = self.get_current_browser()
        if not browser:
            return

        url = browser.url()
        title = browser.page().title() or url.host() or 'Bookmark'

        # prompt user for bookmark title
        text, ok = QInputDialog.getText(
            self, 'Add Bookmark', 'Bookmark title:', text=title
        )
        if ok and text:
            self.bookmarks_mgr.add_bookmark(text, url.toString())
            self.refresh_bookmarks_bar()
            QMessageBox.information(self, 'Bookmarked', f'"{text}" added to bookmarks!')

    def refresh_bookmarks_bar(self):
        """Refresh the bookmarks toolbar."""
        # clear existing buttons
        self.bookmarks_bar.clear()

        # load bookmarks
        bookmarks = self.bookmarks_mgr.get_bookmarks()
        for bm in bookmarks:
            action = QAction(bm['title'][:20], self)
            action.triggered.connect(
                lambda checked, u=bm['url']: self.navigate_bookmark(u)
            )
            self.bookmarks_bar.addAction(action)

        # add manage bookmarks button
        self.bookmarks_bar.addSeparator()
        manage_btn = QAction('⚙ Manage', self)
        manage_btn.triggered.connect(self.manage_bookmarks)
        self.bookmarks_bar.addAction(manage_btn)

    def navigate_bookmark(self, url):
        """Navigate to a bookmarked URL."""
        browser = self.get_current_browser()
        if browser:
            browser.setUrl(QUrl(url))

    def manage_bookmarks(self):
        """Show a dialog to manage bookmarks."""
        bookmarks = self.bookmarks_mgr.get_bookmarks()
        if not bookmarks:
            QMessageBox.information(self, 'Bookmarks', 'No bookmarks yet!')
            return

        dialog = QDialog(self)
        dialog.setWindowTitle('Manage Bookmarks')
        dialog.setGeometry(200, 200, 500, 400)

        layout = QVBoxLayout()

        # bookmarks list
        list_widget = QListWidget()
        for i, bm in enumerate(bookmarks):
            item = QListWidgetItem(f"{bm['title']} ({bm['url'][:30]}...)")
            item.setData(Qt.UserRole, i)
            list_widget.addItem(item)
        layout.addWidget(QLabel('Your Bookmarks:'))
        layout.addWidget(list_widget)

        # buttons
        btn_layout = QHBoxLayout()
        delete_btn = QPushButton('Delete Selected')
        delete_btn.clicked.connect(
            lambda: self.delete_bookmark(list_widget, bookmarks)
        )
        close_btn = QPushButton('Close')
        close_btn.clicked.connect(dialog.accept)
        btn_layout.addWidget(delete_btn)
        btn_layout.addWidget(close_btn)
        layout.addLayout(btn_layout)

        dialog.setLayout(layout)
        dialog.exec_()

    def delete_bookmark(self, list_widget, bookmarks):
        """Delete selected bookmark."""
        current = list_widget.currentItem()
        if not current:
            QMessageBox.warning(self, 'Delete', 'Select a bookmark to delete.')
            return

        idx = current.data(Qt.UserRole)
        del bookmarks[idx]
        self.bookmarks_mgr.save_bookmarks(bookmarks)
        self.refresh_bookmarks_bar()

        list_widget.takeItem(list_widget.row(current))
        QMessageBox.information(self, 'Deleted', 'Bookmark deleted!')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setApplicationName('My Cool Browser')
    window = MainWindow()
    app.exec_()
