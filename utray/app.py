from AppKit import NSApplication
from PyObjCTools import AppHelper
from utray import interfaces
from utray.cron import setup_syncing_cronjobs
from utray.syncer import Syncer
from utray.tray import TrayMenu
from utray.utils import app
from utray.utils import create_icon
from utray.watcher import setup_observer



class Application(object):

    def __init__(self, path_to_unison):
        self.path_to_unison = path_to_unison
        self._status = interfaces.STATUS_INACTIVE
        app.set(self)

    def run(self):
        self._syncer = Syncer(self.path_to_unison)
        self._syncer.start()

        app = NSApplication.sharedApplication()
        app.setActivationPolicy_(2)  # Hide from dock
        app.setApplicationIconImage_(create_icon('appicon.png'))

        self.traymenu = TrayMenu.alloc()
        self.traymenu.init()
        app.setDelegate_(self.traymenu)

        setup_observer(self)
        setup_syncing_cronjobs()

        AppHelper.runEventLoop()

    @property
    def status(self):
        self._status

    def set_status(self, status):
        self._status = status
        self.traymenu.status_changed(status)

    def sync(self, foreground=False, now=False):
        self._syncer.sync(foreground=foreground, now=now)

    def quit(self):
        self._syncer.stop()


def run(path_to_unison):
    Application(path_to_unison).run()
