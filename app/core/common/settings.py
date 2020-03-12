

from PyQt5.QtCore import QSettings

from app.core.common.logapi import log
from app.core.common.registry import Registry



class Settings(QSettings):
    """
    Class to wrap QSettings.
    """

    default_config = {

        'general_settings/wizard_runned': 0,
        'general_settings/close': 0,
        'general_settings/splashscreen': 1,
        'general_settings/language': 'en_US',
    }

    current_config = {}

    file_path = 'settings.ini'


    def __init__(self):
        super(Settings, self).__init__(self.file_path, QSettings.IniFormat)
        QSettings().setFallbacksEnabled(False)  # File only, no fallback to registry.

        Registry().register_function("restore_default_settings", self.set_up_default_values)

    @staticmethod
    def set_filename(ini_file):
        """
        Sets the complete path to an Ini file to be used by Settings objects.
        Does not affect existing Settings objects.

        :param ini_file: the name of .ini file
        :return:
        """
        Settings.file_path = ini_file

    def set_up_default_values(self):
        """
        This static method is called on start up.
        It is used to perform any operation on the default_config dict.

        :return:
        """
        log.debug("setting default settings values:")
        for key, value in self.default_config.items():
            self.setValue(key, value)
        self.sync()

    @property
    def current_settings(self):
        """
        Get the current configuration.

        :return:
        """
        self.current_config.update(self._get_current_configuration())
        return self.current_config

    def _get_current_configuration(self):
        """
        Generate the current configuration.

        :return:
        """
        setting_keys = self.allKeys()
        current_configuration = {}
        for key in setting_keys:
            current_configuration[key] = self.value(key)
        return current_configuration

    def extend_current_settings(self):
        """
        Extend the current configuration with default configuration in case it is incomplete.

        :return:
        """
        self.default_config.update(self.current_settings)
        for key, value in self.default_config.items():
            self.setValue(key, value)
        self.sync()

    def update_current_settings(self, settings_dict):
        """
        Update the current configuration with dictionnary parameter.

        :param settings_dict:
        :return:
        """
        assert isinstance(settings_dict, dict)

        for key, value in settings_dict.items():
            self.setValue(key, value)
        self.sync()

    def get_default_value(self, key):
        """
        Get the default value of the given key.

        :param key: the key we want its default value.
        :return: the default value of the key given in parameter.
        """
        if self.group():
            key = self.group() + '/' + key
        return Settings.default_config[key]

    def value(self, key, **kwargs):
        """
        Returns the value for the given ``key``. The returned ``value`` is of the same
        type as the default value in the *Settings.default_config* dict.

        :param key: The key to return the value from.
        :return:
        """
        # if group() is not empty the group has not been specified together with the key.
        if self.group():
            default_value = Settings.default_config[self.group() + '/' + key]
        else:
            default_value = Settings.default_config[key]
        setting = super(Settings, self).value(key, default_value, **kwargs)
        return self._convert_value(setting, default_value)

    @staticmethod
    def _convert_value(setting, default_value):
        """
        This converts the given ``setting`` to the type of the given ``default_value``.

        :param setting: The setting to convert. This could be ``true`` for example.Settings()
        :param default_value: Indication the type the setting should be converted to. For example ``True``
        (type is boolean), meaning that we convert the string ``true`` to a python boolean.

        **Note**, this method only converts a few types and might need to be extended if a certain type is missing!
        """
        # Handle 'None' type (empty value) properly.
        if setting is None:
            # An empty string saved to the settings results in a None type being returned.
            # Convert it to empty unicode string.
            if isinstance(default_value, str):
                return ''
            # An empty list saved to the settings results in a None type being returned.
            else:
                return []
        # Convert the setting to the correct type.
        if isinstance(default_value, bool):
            if isinstance(setting, bool):
                return setting
            # Sometimes setting is string instead of a boolean.
            return setting == 'true'
        if isinstance(default_value, int):
            return int(setting)
        if isinstance(default_value, float):
            return float(setting)
        return setting
