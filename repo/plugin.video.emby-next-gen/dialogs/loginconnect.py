import xbmc
import xbmcgui
from helper import utils

ACTION_PARENT_DIR = 9
ACTION_PREVIOUS_MENU = 10
ACTION_BACK = 92
SIGN_IN = 200
CANCEL = 201
ERROR_TOGGLE = 202
ERROR_MSG = 203
ERROR = {'Invalid': 1, 'Empty': 2}


class LoginConnect(xbmcgui.WindowXMLDialog):
    def __init__(self, *args, **kwargs):
        self.error = None
        self.user_field = None
        self.password_field = None
        self.signin_button = None
        self.remind_button = None
        self.error_toggle = None
        self.error_msg = None
        self.EmbyServer = None
        xbmcgui.WindowXMLDialog.__init__(self, *args, **kwargs)

    def onInit(self):
        self.user_field = self._add_editcontrol(755, 338, 40, 415, False)
        self.setFocus(self.user_field)
        self.password_field = self._add_editcontrol(755, 448, 40, 415, True)
        self.signin_button = self.getControl(SIGN_IN)
        self.remind_button = self.getControl(CANCEL)
        self.error_toggle = self.getControl(ERROR_TOGGLE)
        self.error_msg = self.getControl(ERROR_MSG)
        self.user_field.controlUp(self.remind_button)
        self.user_field.controlDown(self.password_field)
        self.password_field.controlUp(self.user_field)
        self.password_field.controlDown(self.signin_button)
        self.signin_button.controlUp(self.password_field)
        self.remind_button.controlDown(self.user_field)

    def onClick(self, controlId):
        if controlId == SIGN_IN:
            # Sign in to emby connect
            self._disable_error()
            user = self.user_field.getText()
            password = self.password_field.getText()

            if not user or not password:
                # Display error
                self._error(ERROR['Empty'], utils.Translate(30608))
                xbmc.log("EMBY.dialogs.loginconnect: Username or password cannot be null", 3) # LOGERROR
            elif self._login(user, password):
                self.close()
        elif controlId == CANCEL:
            # Remind me later
            self.close()

    def onAction(self, action):
        if self.error == ERROR['Empty'] and self.user_field.getText() and self.password_field.getText():
            self._disable_error()

        if action in (ACTION_BACK, ACTION_PARENT_DIR, ACTION_PREVIOUS_MENU):
            self.close()

    def _add_editcontrol(self, x, y, height, width, password):
        control = xbmcgui.ControlEdit(0, 0, 0, 0, label="", font="font13", textColor="FF52b54b", disabledColor="FF888888", focusTexture="-", noFocusTexture="-")
        control.setPosition(x, y)
        control.setHeight(height)
        control.setWidth(width)
        self.addControl(control)

        if password:
            control.setType(xbmcgui.INPUT_TYPE_PASSWORD, "Please enter password")

        return control

    def _login(self, username, password):
        result = self.EmbyServer.login_to_connect(username, password)

        if not result:
            self._error(ERROR['Invalid'], utils.Translate(33009))
            return False

        utils.Dialog.notification(heading=utils.addon_name, message=f"{utils.Translate(33000)} {result['User']['Name']}", icon=result['User'].get('ImageUrl') or utils.icon, time=2000, sound=False)
        return True

    def _error(self, state, message):
        self.error = state
        self.error_msg.setLabel(message)
        self.error_toggle.setVisibleCondition('true')

    def _disable_error(self):
        self.error = None
        self.error_toggle.setVisibleCondition('false')
