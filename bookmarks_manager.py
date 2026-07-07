import json
import os


class BookmarksManager:
    """Manages bookmarks storage and retrieval."""

    def __init__(self, base_dir=None):
        self.base_dir = base_dir or self._get_default_data_dir()
        os.makedirs(self.base_dir, exist_ok=True)
        self.bookmarks_file = os.path.join(self.base_dir, 'bookmarks.json')
        self.bookmarks = self.load_bookmarks()

    @staticmethod
    def _get_default_data_dir():
        if os.name == 'nt':
            base_dir = os.environ.get('APPDATA') or os.path.expanduser('~/AppData/Roaming')
        else:
            base_dir = os.path.expanduser('~/.config')

        app_dir = os.path.join(base_dir, 'MyCoolBrowser')
        os.makedirs(app_dir, exist_ok=True)
        return app_dir

    def load_bookmarks(self):
        """Load bookmarks from file."""
        if os.path.exists(self.bookmarks_file):
            try:
                with open(self.bookmarks_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return []
        return []

    def save_bookmarks(self, bookmarks=None):
        """Save bookmarks to file."""
        if bookmarks is None:
            bookmarks = self.bookmarks
        try:
            with open(self.bookmarks_file, 'w') as f:
                json.dump(bookmarks, f, indent=2)
            self.bookmarks = bookmarks
        except IOError as e:
            print(f"Error saving bookmarks: {e}")

    def add_bookmark(self, title, url):
        """Add a new bookmark."""
        bookmark = {'title': title, 'url': url}
        # avoid duplicates
        if not any(b['url'] == url for b in self.bookmarks):
            self.bookmarks.append(bookmark)
            self.save_bookmarks()

    def get_bookmarks(self):
        """Get all bookmarks."""
        return self.bookmarks

    def remove_bookmark(self, url):
        """Remove a bookmark by URL."""
        self.bookmarks = [b for b in self.bookmarks if b['url'] != url]
        self.save_bookmarks()
