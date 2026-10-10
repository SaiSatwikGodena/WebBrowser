WebBrowser

A simple, customizable desktop web browser built with Python, PyQt5, and PyQtWebEngine.

WebBrowser is designed to make everyday browsing simple and convenient.
It includes tabbed browsing, bookmark management, a custom landing page, quick links, and dark and light themes.
The clean interface makes it easy to navigate through the options. (Note: It's been nick-named premitive web browser because of it's looks resembling old browsers like Internet Explorer)

Features :

Tabbed Browsing - Each tab maintains its own browsing history and page state.
The attention to details-Tab titles update dynamically as pages load, a progress indicator displays page-loading progress.

Bookmarks
Bookmark any webpage with a custom title.
View, edit, and delete bookmarks through the Manage Bookmarks button.

Custom Landing Page
Live clock and built-in search bar.
Search using Google, DuckDuckGo, or Bing.
Add, edit, and remove quick links to your favorite websites.
Switch between dark and light themes with just a toggle.
Theme preferences and quick links persist locally - so only you have your choice of style.

Navigation
Back and Forward buttons for browsing history.
Reload button to refresh the current page.
Home button to return to the landing page.
URL bar for entering website addresses or search terms.
Keyboard shortcuts for faster navigation.
Installation and Setup

You can skip the manual setup by downloading the prebuilt .EXE from the project's Releases section, if available.

Requirements
Python 3.7+
PyQt5
PyQtWebEngine
Install Dependencies
pip install PyQt5 PyQtWebEngine

Run the Browser
Navigate to the project directory and run:

python WebBrowser.py

Project Structure
WebBrowser/
├── WebBrowser.py          # Main browser application
├── bookmarks_manager.py  # Bookmark management
├── landing.html          # Landing page
├── app.js                # Landing page functionality
├── styles.css             # Landing page styling
├── bookmarks.json        # Bookmark storage (auto-created)
└── README.md              # Project documentation

# Built With
Python
PyQt5
PyQtWebEngine
HTML, CSS, and JavaScript
Planned Features
Download manager
Tab groups and tab pinning
Bookmark folders and categories
Bookmark import and export (HTML/JSON)
Additional keyboard shortcuts, including Ctrl + T and Ctrl + W
Session restoration after restarting the browser
Custom themes
Bookmark search

Have something to say?
Suggestions, bug reports, and contributions are welcome. Feel free to fork the project, experiment with the code, and help improve the browser.

WebBrowser — Simple browsing, customizable your way.
