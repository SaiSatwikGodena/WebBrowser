WebBrowser 

Browser with Bookmarks
Features

Tabbed Browsing
● Open multiple tabs simultaneously
● Switch between tabs easily with a clean tab bar
● Close individual tabs or replace the last tab with a new landing page
● Each tab maintains independent history and state
Bookmarks

● Bookmark any webpage with a custom title
● View all bookmarks in a dedicated toolbar below the navigation bar
● Click bookmarks to instantly navigate to them
● Manage bookmarks: view, delete, or edit from the Manage Bookmarks dialog
● Bookmarks persist automatically in bookmarks.json

Landing Page
● Custom start/home page with a live clock display, search bar (Google, DuckDuckGo,
Bing), editable/persistent quick links, and a dark/light theme toggle (defaults to dark)

Navigation
● Back / Forward: Navigate through page history
● Reload: Refresh current page
● Home: Return to the landing page
● URL Bar: Type URLs or search terms
● Keyboard shortcut / focuses the search bar

Tab Management
● New Tab button opens a landing page in a new tab
● Close Tab (X button on tabs) closes the tab
● Tab titles update dynamically as pages load
● Progress indicator shows loading percentage

Installation & Setup
(You can skip prerequisits if u download the .EXE from the releases)
Prerequisites
● Python 3.7+
● PyQt5
● PyQtWebEngine
Install Dependencies
pip install PyQt5 PyQtWebEngine
Run the Browser
python WebBrowser.py
File Structure
WebBrowser/
├── WebBrowser.py # Main browser application
├── bookmarks_manager.py # Bookmarks storage and management
├── landing.html # Custom start/home page
├── app.js # Landing page interactive features
├── styles.css # Landing page styling
├── bookmarks.json # Bookmarks database (auto-created)
└── README.md # This file

Usage Guide
Bookmarking a Page
1. Click the ★ Bookmark button in the toolbar
2. Enter a custom title for the bookmark (or accept the default)
3. Click OK
4. The bookmark appears in the bookmarks bar below

Navigating Bookmarks
● Click any bookmark button in the bookmarks bar to navigate instantly
● Use ⚙ Manage to open the Manage Bookmarks dialog

Managing Bookmarks
1. Click the ⚙ Manage button in the bookmarks bar
2. Select a bookmark from the list
3. Click Delete Selected to remove it
4. Click Close to exit

Opening Multiple Tabs
1. Click the + New Tab button or use Ctrl+T (if implemented)
2. A new tab opens with the landing page
3. Navigate in each tab independently

Quick Links on Landing Page
1. Scroll to the "Quick links" section on the landing page
2. Enter a title and URL in the form
3. Click Add to save the link
4. Use Edit or Remove buttons to manage existing links

Theme Toggle
1. On the landing page, click the Dark/Light toggle in the top-right
2. The page theme changes and persists locally
Tips & Tricks
● Press / on any page to focus the search bar (works on landing page)
● Keyboard shortcuts: Alt+Left/Right Arrow for Back/Forward; F5 for Reload
● Dark mode: Landing page defaults to dark theme; customize in app.js
● Customize search engine: Edit the select options in landing.html
● Auto-load bookmarks: Bookmarks load from bookmarks.json on startup

Future Enhancements
● Download manager
● Tab groups
● Bookmark folders / categories
● Import/export bookmarks (HTML, JSON)
● Keyboard shortcuts (Ctrl+T, Ctrl+W, etc.)
● Tab pinning
● Session restore on restart
● Custom themes
● Search in bookmarks
