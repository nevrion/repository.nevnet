import xbmc
import xbmcgui
from helper import utils

ACTION_PARENT_DIR = 9
ACTION_PREVIOUS_MENU = 10
ACTION_BACK = 92
CONNECT = 200
CANCEL = 201
ERROR_TOGGLE = 202
ERROR_MSG = 203
ERROR = {'Invalid': 1, 'Empty': 2}


class ServerManual(xbmcgui.WindowXMLDialog):
    def __init__(self, *args):
        self.error = None
        self.connect_button = None
        self.cancel_button = None
        self.error_toggle = None
        self.error_msg = None
        self.host_field = None
        self.port_field = None
        self.connect_to_address = None
        xbmcgui.WindowXMLDialog.__init__(self, *args)

    def onInit(self):
        self.connect_button = self.getControl(CONNECT)
        self.cancel_button = self.getControl(CANCEL)
        self.error_toggle = self.getControl(ERROR_TOGGLE)
        self.error_msg = self.getControl(ERROR_MSG)
        self.host_field = self._add_editcontrol(755, 433, 40, 415)
        self.port_field = self._add_editcontrol(755, 543, 40, 415)
        self.port_field.setText('8096')
        self.setFocus(self.host_field)
        self.host_field.controlUp(self.cancel_button)
        self.host_field.controlDown(self.port_field)
        self.port_field.controlUp(self.host_field)
        self.port_field.controlDown(self.connect_button)
        self.connect_button.controlUp(self.port_field)
        self.cancel_button.controlDown(self.host_field)

    def onClick(self, controlId):
        if controlId == CONNECT:
            # Sign in to emby connect
            self._disable_error()
            server = self.host_field.getText()
            port = self.port_field.getText()

            if not server:
                # Display error
                self._error(ERROR['Empty'], utils.Translate(30617))
                xbmc.log("EMBY.dialogs.servermanual: Server cannot be null", 3) # LOGERROR
            elif self._connect_to_server(server, port):
                self.close()
        # Remind me later
        elif controlId == CANCEL:
            self.close()

    def onAction(self, action):
        if self.error == ERROR['Empty'] and self.host_field.getText() and self.port_field.getText():
            self._disable_error()

        if action in (ACTION_BACK, ACTION_PARENT_DIR, ACTION_PREVIOUS_MENU):
            self.close()

    def _add_editcontrol(self, x, y, height, width):
        control = xbmcgui.ControlEdit(0, 0, 0, 0, label="", font="font13", textColor="FF52b54b", disabledColor="FF888888", focusTexture="-", noFocusTexture="-")
        control.setPosition(x, y)
        control.setHeight(height)
        control.setWidth(width)
        self.addControl(control)
        return control

    def _connect_to_server(self, server, port):
        server_address = f"{server}:{port}"
        self._message(f"{utils.Translate(30610)} {server_address}...")

        if not self.connect_to_address(server_address):  # Unavailable
            self._message(utils.Translate(30609))
            return False

        return True

    def _message(self, message):
        self.error_msg.setLabel(message)
        self.error_toggle.setVisibleCondition('true')

    def _error(self, state, message):
        self.error = state
        self.error_msg.setLabel(message)
        self.error_toggle.setVisibleCondition('true')

    def _disable_error(self):
        self.error = None
        self.error_toggle.setVisibleCondition('false')
