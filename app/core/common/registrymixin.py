
from app.core.common import de_hump
from app.core.common.registry import Registry


class RegistryMixin(object):
    """
    This adds registry components to classes to use at run time.
    """
    def __init__(self, parent):
        """
        Register the class and initialization/clean hooks.
        """
        try:
            super(RegistryMixin, self).__init__(parent)
        except TypeError:
            super(RegistryMixin, self).__init__()
        Registry().register_function('__application_init__', self.__application_init__)
        Registry().register_function('__application_post_init__', self.__application_post_init__)
        Registry().register_function('__application_clean__', self.__application_clean__)

    def __application_init__(self):
        """ Override """
        pass

    def __application_post_init__(self):
        """ Override """
        pass

    def __application_clean__(self):
        """ Override """
        pass


class UniqueRegistryMixin(RegistryMixin):
    """
    This adds a UNIQUE registry components to classes to use at run time.
    """
    def __init__(self, parent):
        """
        Register the unique class.
        """
        try:
            super(UniqueRegistryMixin, self).__init__(parent)
        except TypeError:
            super(UniqueRegistryMixin, self).__init__()
        Registry().register(de_hump(self.__class__.__name__), self)
