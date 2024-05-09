import xbmcgui

class SkipIntro(xbmcgui.WindowXMLDialog):
    def __init__(self, *args, **kwargs):
        self.dialog_open = False
        self.JumpFunction = None
        xbmcgui.WindowXMLDialog.__init__(self, *args, **kwargs)

    def set_JumpFunction(self, JumpFunction):
        self.JumpFunction = JumpFunction

    def onFocus(self, controlId):
        self.dialog_open = True

    def onAction(self, action):
        if action.getId() == 10:  # ACTION_PREVIOUS_MENU
            self.dialog_open = False
            self.close()
        elif action.getId() == 92:  # ACTION_NAV_BACK
            self.dialog_open = False
            self.close()

    def onClick(self, controlId):
        if controlId == 1:
            self.JumpFunction()
            self.dialog_open = False
            self.close()
