"""
Adding this package to installed apps is not needed
https://stackoverflow.com/questions/47684387/what-is-the-purpose-of-adding-to-installed-apps-in-django
"""

from django.core.files.storage import FileSystemStorage


class OverwriteStorage(FileSystemStorage):
    '''
    Storage that overrides files if already existent
    '''

    def get_available_name(self, name, max_length=None):
        self.delete(name)
        return name
