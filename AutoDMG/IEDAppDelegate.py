#-*- coding: utf-8 -*-
#
#  InstallESDtoDMGAppDelegate.py
#  InstallESDtoDMG
#
#  Created by Per Olofsson on 2013-09-19.
#  Copyright Per Olofsson, University of Gothenburg 2013. All rights reserved.
#

from Foundation import *
from AppKit import *
from objc import IBAction, IBOutlet

from IEDLog import *


defaults = NSUserDefaults.standardUserDefaults()


class IEDAppDelegate(NSObject):
    
    mainWindowController = IBOutlet()
    
    def init(self):
        self = super(IEDAppDelegate, self).init()
        if self is None:
            return None
        
        return self
    
    def initialize(self):
        defaultsPath = NSBundle.mainBundle().pathForResource_ofType_(u"Defaults", u"plist")
        defaultsDict = NSDictionary.dictionaryWithContentsOfFile_(defaultsPath)
        defaults.registerDefaults_(defaultsDict)
    
    def applicationDidFinishLaunching_(self, sender):
        LogDebug(u"applicationDidFinishLaunching:")
        
        updateProfileInterval = defaults.integerForKey_(u"UpdateProfileInterval")
        LogInfo(u"UpdateProfileInterval = %d", updateProfileInterval)
        if updateProfileInterval != 0:
            lastCheck = defaults.objectForKey_(u"LastUpdateProfileCheck")
            if lastCheck.timeIntervalSinceNow() < (-60 * 60 * 18 * updateProfileInterval):
                self.mainWindowController.updateController.checkForProfileUpdates_(self)
    
    def applicationShouldTerminate_(self, sender):
        LogDebug(u"applicationShouldTerminate:")
        if self.mainWindowController.isBusy():
            alert = NSAlert.alloc().init()
            alert.setAlertStyle_(NSCriticalAlertStyle)
            alert.setMessageText_(u"Application busy")
            alert.setInformativeText_(u"Quitting now could leave the " \
                                      u"system in an unpredictable state.")
            alert.addButtonWithTitle_(u"Quit")
            alert.addButtonWithTitle_(u"Stay")
            button = alert.runModal()
            if button == NSAlertSecondButtonReturn:
                return NSTerminateCancel
        return NSTerminateNow
    
    def applicationWillTerminate_(self, sender):
        LogDebug(u"applicationWillTerminate:")
        self.mainWindowController.cleanup()
    
    @IBAction
    def showHelp_(self, sender):
        NSWorkspace.sharedWorkspace().openURL_(NSURL.URLWithString_(defaults.stringForKey_(u"HelpURL")))