
from app.core.common.registry import Registry
from app.core.common import is_win


class RegistryProperties(object):
    """
    This adds registry components to classes to use at run time.
    """

    @property
    def application(self):
        """
        Adds the praypertimes to the class dynamically.
        Windows needs to access the application in a dynamic manner.
        """
        if is_win():
            return Registry().get('application')
        else:
            if not hasattr(self, '_application') or not self._application:
                self._application = Registry().get('application')
            return self._application

    @property
    def global_frame(self):
        """
        Adds the global_frame to the class dynamically.
        """
        if not hasattr(self, '_global_frame') or not self._global_frame:
            self._global_frame = Registry().get('global_frame')
        return self._global_frame
