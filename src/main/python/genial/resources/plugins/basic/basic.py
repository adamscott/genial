"""
    Génial - Basic plugin
    ================================================
    A "Génies en herbe" questions manager.

    :copyright: (c) 2015, Adam Scott.
    :license: GPL3, see LICENSE for more details.
"""
import logging
from genial import plugins

# The logger name reflects the plugin name
log = logging.getLogger('Basic')


class BasicPlugin (plugins.IQuestionPlugin):
    global log

    def activate(self):
        log.debug('===Activated===')
        self.is_activated = True

    def deactivate(self):
        log.debug('===Deactivated===')
        self.is_activated = False
