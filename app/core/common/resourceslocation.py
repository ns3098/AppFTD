

from PyQt5.QtCore import QDir

# Use current dir because application is run from AppFTD.py
# When application is compiled and deployed, the src_folder
# is always considered as the root directory from which the
# executable is run.
src_root_dir = QDir().currentPath()


class ResourcesLocation(object):
    """
    The ResourcesLocation class is a static class which retrieves the absolute directory path
    based on the directory type.
    """
    __AppDir__ = 1
    __ResourcesDir__ = 2
    __LanguageDir__ = 5
    __IconsDir__ = 6
    __ImagesDir__ = 7
    __FontDir__ = 9
    __LogsDir__ = 10

    @staticmethod
    def get_directory(dir_type=__AppDir__):
        """
        :param dir_type: The directory type you want, for instance the data directory.
                         Default *ResourcesLocation.AppDir*

        :return: The appropriate directory according to the directory type.
        """
        if dir_type == ResourcesLocation.__AppDir__:
            return src_root_dir

        elif dir_type == ResourcesLocation.__ResourcesDir__:
            app_path = _get_os_dir_path(dir_type)
            return app_path

        elif dir_type == ResourcesLocation.__LanguageDir__:
            app_path = _get_os_dir_path(dir_type)
            return app_path + 'i18n'

        elif dir_type == ResourcesLocation.__IconsDir__:
            app_path = _get_os_dir_path(dir_type)
            return app_path + 'icons'

        elif dir_type == ResourcesLocation.__ImagesDir__:
            app_path = _get_os_dir_path(dir_type)
            return app_path + 'images'

        elif dir_type == ResourcesLocation.__FontDir__:
            app_path = _get_os_dir_path(dir_type)
            return app_path + 'fonts'

        elif dir_type == ResourcesLocation.__LogsDir__:
            return src_root_dir + '/logs'

        else:
            return _get_os_dir_path(dir_type)

    @property
    def root_dir(self):
        return self.get_directory(ResourcesLocation.__AppDir__)

    @property
    def resources_dir(self):
        return self.get_directory(ResourcesLocation.__ResourcesDir__)

    @property
    def language_dir(self):
        return self.get_directory(ResourcesLocation.__LanguageDir__)

    @property
    def icons_dir(self):
        return self.get_directory(ResourcesLocation.__IconsDir__)

    @property
    def images_dir(self):
        return self.get_directory(ResourcesLocation.__ImagesDir__)

    @property
    def font_dir(self):
        return self.get_directory(ResourcesLocation.__FontDir__)

    @property
    def logs_dir(self):
        return self.get_directory(ResourcesLocation.__LogsDir__)


def _get_os_dir_path(dir_type):
    """
    :param dir_type: The directory type you want, for instance the data directory.
    :return: A absolute path.
    """

    directory = src_root_dir + '/resources/'
    if QDir().exists(directory):
        return directory
