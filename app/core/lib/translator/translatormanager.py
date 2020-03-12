
from PyQt5 import QtWidgets
from PyQt5.QtCore import QTranslator

from app.core.common.logapi import log


class LanguageManager(object):
    """
    Helper for Language selection.
    """
    __instance__ = None

    def __new__(cls, language='en_US'):
        """
        Re-implement method __new__ to have a singleton.
        """
        if not cls.__instance__:
            cls.__instance__ = object.__new__(cls)
        return cls.__instance__

    def __init__(self, language='en_US'):
        languages = ['en_US', 'fr_FR', 'ar_AR']
        self.current_language = language

        self.translators = {}

        for _language in languages:
            self.translator = QTranslator()
            if self.translator.load(':/i18n/{}.qm'.format(_language)):
                log.debug('Translation {} has been correclty initialized'.format(_language))
            if _language == self.current_language:
                QtWidgets.QApplication.instance().installTranslator(self.translator)
                log.info('Translation {} has been correclty loaded'.format(_language))

            self.translators[_language] = self.translator

    def set_translator(self, language):
        """
        Remove old translation and apply the new language.
        Need to update EACH text to have dynamic translation (instead of reboot application).

        :param language: language to apply.
        :return:
        """
        translator = self.translators[self.current_language]
        QtWidgets.QApplication.instance().removeTranslator(translator)

        translator = self.translators[language]
        QtWidgets.QApplication.instance().installTranslator(translator)

        self.current_language = language
