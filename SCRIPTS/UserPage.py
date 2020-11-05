import wx
import wx.lib.platebtn as plateButtons
from cryptography.fernet import Fernet
import ast

import os
two_up = os.path.dirname(os.path.dirname(__file__))

class settingsButton(wx.Panel):
    def __init__(self, parent, size):
        super(settingsButton, self).__init__(parent, size=size)

        self.SetMinSize(size)
        self.initUI()

        #self.Center()
        self.Layout()
        #self.Show(True)

    def initUI(self):

        LayoutSettingsButton = wx.BoxSizer(wx.HORIZONTAL)

        LayoutSettingsDesc = wx.BoxSizer(wx.VERTICAL)

        self.icon = wx.StaticBitmap(self, -1, wx.NullBitmap, size=(self.GetMinSize()[1], self.GetMinSize()[1]))
        self.icon.SetBackgroundColour(wx.Colour(50, 50, 50))
        self.heading = wx.StaticText(self, -1, "Heading")
        self.heading.SetFont(wx.Font(14, 70, 90, 90, False, wx.EmptyString))
        self.heading.SetForegroundColour(wx.Colour(200, 200, 200))
        self.description = wx.StaticText(self, -1, "Description of the heading")
        self.description.SetFont(wx.Font(11, 70, 90, 90, False, wx.EmptyString))
        self.description.SetForegroundColour(wx.Colour(200, 200, 200))

        LayoutSettingsDesc.Add(self.heading, proportion=0, flag=wx.EXPAND | wx.ALL, border=0)
        LayoutSettingsDesc.Add(self.description, proportion=1, flag=wx.EXPAND | wx.ALL, border=5)

        LayoutSettingsButton.Add(self.icon, proportion=0, flag=wx.EXPAND | wx.ALL, border=0)
        LayoutSettingsButton.Add(LayoutSettingsDesc, proportion=0, flag=wx.EXPAND | wx.ALL, border=10)

        self.SetSizer(LayoutSettingsButton)


class User(wx.Panel):

    def __init__(self, parent):
        #super(User, self).__init__(parent, title="Yantrakar User", size=(1100, 750))
        super(User, self).__init__(parent, size=(1100, 750))

        self.SetMinSize((1100, 750))

        self.settingsBtnSize = (300, 150)

        self.encryptionKey = b'gkmrxai04WhOcWj3EGl-2Io58Q8biOWOytdQbPhNYGU='

        self.changeAdminPassBitmap = wx.Bitmap(two_up + "/ui_elements/admin.png")
        self.changeViewerPassBitmap = wx.Bitmap(two_up + "/ui_elements/Guest.png")
        self.updateKeyBitmap = wx.Bitmap(two_up + "/ui_elements/Key.png")
        self.updateAppBitmap = wx.Bitmap(two_up + "/ui_elements/Update.png")
        self.factoryResetBitmap = wx.Bitmap(two_up + "/ui_elements/Factory.png")
        self.deleteAllDataBitmap = wx.Bitmap(two_up + "/ui_elements/Delete.png")
        self.autoTimerBitmap = wx.Bitmap(two_up + "/ui_elements/Timer.png")
        self.pricingBitmap = wx.Bitmap(two_up + "/ui_elements/Pricing.png")

        self.changeAdminPassBitmap = self.scaleImages(self.changeAdminPassBitmap,
                                                      (self.settingsBtnSize[1], self.settingsBtnSize[1]))
        self.changeViewerPassBitmap = self.scaleImages(self.changeViewerPassBitmap,
                                                       (self.settingsBtnSize[1], self.settingsBtnSize[1]))
        self.updateKeyBitmap = self.scaleImages(self.updateKeyBitmap,
                                                (self.settingsBtnSize[1], self.settingsBtnSize[1]))
        self.updateAppBitmap = self.scaleImages(self.updateAppBitmap,
                                                (self.settingsBtnSize[1], self.settingsBtnSize[1]))
        self.factoryResetBitmap = self.scaleImages(self.factoryResetBitmap,
                                                   (self.settingsBtnSize[1], self.settingsBtnSize[1]))
        self.deleteAllDataBitmap = self.scaleImages(self.deleteAllDataBitmap,
                                                    (self.settingsBtnSize[1], self.settingsBtnSize[1]))
        self.autoTimerBitmap = self.scaleImages(self.autoTimerBitmap,
                                                (self.settingsBtnSize[1], self.settingsBtnSize[1]))
        self.pricingBitmap = self.scaleImages(self.pricingBitmap,
                                              (self.settingsBtnSize[1], self.settingsBtnSize[1]))

        self.autoTimerRows = 0
        self.autoTimerRowList = []

        self.initUI()


    def initUI(self):
        self.fontNormal = wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        self.fontBold = wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        self.darkOrange = wx.Colour(255, 191, 0)
        self.lightOrange = wx.Colour(248, 217, 122)
        self.darkGrey = wx.Colour(50, 50, 50)
        self.Grey = wx.Colour(70, 70, 70)
        self.lightGrey = wx.Colour(100, 100, 100)
        self.faintWhite = wx.Colour(200, 200, 200)
        self.white = wx.Colour(255, 255, 255)
        self.slightlyLightGrey = wx.Colour(80, 80, 80)

        self.SetFont(self.fontNormal)
        self.SetBackgroundColour(self.Grey)

        LayoutMain = wx.BoxSizer(wx.HORIZONTAL)

        self.userPanel = wx.Panel(self, pos=wx.DefaultPosition, size=wx.DefaultSize)

        # LayoutMain.Add(self.navPanel, proportion=0, flag=wx.EXPAND | wx.ALL, border=0)
        LayoutMain.Add(self.userPanel, proportion=1, flag=wx.EXPAND | wx.ALL, border=0)

        LayoutUserPanel = wx.BoxSizer(wx.VERTICAL)

        self.userPanelHeadPanel = wx.Panel(self.userPanel, -1)
        self.userPanelHeadPanel.SetBackgroundColour(self.darkGrey)

        LayoutHeadPanel = wx.BoxSizer(wx.VERTICAL)

        self.userPanelHeading = wx.StaticText(self.userPanelHeadPanel, -1, "User Settings")
        self.userPanelHeading.SetForegroundColour(self.white)
        self.userPanelHeading.SetFont(self.fontBold)

        LayoutHeadPanel.Add(self.userPanelHeading, proportion=1, flag=wx.ALIGN_CENTER | wx.ALL, border=15)
        self.userPanelHeadPanel.SetSizer(LayoutHeadPanel)
        LayoutHeadPanel.Fit(self.userPanelHeadPanel)

        self.userPanelContents = wx.Panel(self.userPanel, -1)

        LayoutUserPanelContents = wx.BoxSizer(wx.HORIZONTAL)

        self.settingsPanel = wx.ScrolledWindow(self.userPanelContents, pos=wx.DefaultPosition, size=wx.DefaultSize,
                                                style=wx.VSCROLL)
        self.settingsPanel.SetScrollRate(5, 5)
        #self.settingsPanel.SetBackgroundColour(self.white)

        LayoutSettingsPanel = wx.BoxSizer(wx.VERTICAL)

        self.settingsMenuPanel = wx.Panel(self.settingsPanel, -1)
        # self.settingsMenuPanel.SetBackgroundColour(self.white)

        LayoutSettingsMenu = wx.BoxSizer(wx.HORIZONTAL)

        ##ADD MENU OPTION TO self.settingsMenu
        self.settingsMenu = wx.Panel(self.settingsMenuPanel, -1)
        # self.settingsMenu.SetMinSize((300, 300))
        # self.settingsMenu.SetBackgroundColour(wx.Colour(0, 0, 0))

        self.LayoutSettingsMenuOptions = wx.GridBagSizer(10, 10)


        self.changeAdminPassButton = settingsButton(self.settingsMenu, self.settingsBtnSize)
        self.changeAdminPassButton.heading.SetLabel("Change Admin Password")
        self.changeAdminPassButton.heading.Wrap(self.settingsBtnSize[0] - self.settingsBtnSize[1] - 20)
        #self.changeAdminPassButton.Bind(wx.EVT_LEFT_UP, lambda evt: self.changePassClicked(evt, type="Admin"))
        self.changeAdminPassButton.icon.Bind(wx.EVT_LEFT_UP, lambda evt: self.changePassClicked(evt, type="Admin"))
        self.changeAdminPassButton.heading.Bind(wx.EVT_LEFT_UP, lambda evt: self.changePassClicked(evt, type="Admin"))
        self.changeAdminPassButton.description.Bind(wx.EVT_LEFT_UP, lambda evt: self.changePassClicked(evt, type="Admin"))
        self.changeAdminPassButton.icon.SetBitmap(self.changeAdminPassBitmap)
        self.changeAdminPassButton.description.SetLabel("Admin account has access to all panels")
        self.changeAdminPassButton.description.Wrap(self.settingsBtnSize[0] - self.settingsBtnSize[1] - 20)


        self.changeViewerPassButton = settingsButton(self.settingsMenu, self.settingsBtnSize)
        self.changeViewerPassButton.heading.SetLabel("Change Viewer Password")
        self.changeViewerPassButton.heading.Wrap(self.settingsBtnSize[0] - self.settingsBtnSize[1] - 20)
        #self.changeViewerPassButton.Bind(wx.EVT_LEFT_UP, lambda evt: self.changePassClicked(evt, type="Viewer"))
        self.changeViewerPassButton.icon.Bind(wx.EVT_LEFT_UP, lambda evt: self.changePassClicked(evt, type="Viewer"))
        self.changeViewerPassButton.heading.Bind(wx.EVT_LEFT_UP, lambda evt: self.changePassClicked(evt, type="Viewer"))
        self.changeViewerPassButton.description.Bind(wx.EVT_LEFT_UP,
                                                    lambda evt: self.changePassClicked(evt, type="Viewer"))
        self.changeViewerPassButton.icon.SetBitmap(self.changeViewerPassBitmap)
        self.changeViewerPassButton.description.SetLabel("Viewer has access to the only the Dashboard Panel")
        self.changeViewerPassButton.description.Wrap(self.settingsBtnSize[0] - self.settingsBtnSize[1] - 20)

        self.updateActivationKeyButton = settingsButton(self.settingsMenu, self.settingsBtnSize)
        self.updateActivationKeyButton.heading.SetLabel("Update Activation Key")
        self.updateActivationKeyButton.heading.Wrap(self.settingsBtnSize[0] - self.settingsBtnSize[1] - 20)
        self.updateActivationKeyButton.icon.Bind(wx.EVT_LEFT_UP, lambda evt: self.changeKeyClicked(evt))
        self.updateActivationKeyButton.heading.Bind(wx.EVT_LEFT_UP, lambda evt: self.changeKeyClicked(evt))
        self.updateActivationKeyButton.description.Bind(wx.EVT_LEFT_UP,
                                                     lambda evt: self.changeKeyClicked(evt))
        self.updateActivationKeyButton.icon.SetBitmap(self.updateKeyBitmap)
        self.updateActivationKeyButton.description.SetLabel("Updating activation key ensures data safety")
        self.updateActivationKeyButton.description.Wrap(self.settingsBtnSize[0] - self.settingsBtnSize[1] - 20)

        self.updateAppButton = settingsButton(self.settingsMenu, self.settingsBtnSize)
        self.updateAppButton.heading.SetLabel("Update Application")
        self.updateAppButton.heading.Wrap(self.settingsBtnSize[0] - self.settingsBtnSize[1] - 20)
        self.updateAppButton.icon.SetBitmap(self.updateAppBitmap)
        self.updateAppButton.description.SetLabel("Install software updates for better experience")
        self.updateAppButton.description.Wrap(self.settingsBtnSize[0] - self.settingsBtnSize[1] - 20)

        self.factoryResetButton = settingsButton(self.settingsMenu, self.settingsBtnSize)
        self.factoryResetButton.heading.SetLabel("Factory Reset")
        self.factoryResetButton.heading.Wrap(self.settingsBtnSize[0] - self.settingsBtnSize[1] - 20)
        self.factoryResetButton.icon.SetBitmap(self.factoryResetBitmap)
        self.factoryResetButton.description.SetLabel("Deletes all configuration settings captured images")
        self.factoryResetButton.description.Wrap(self.settingsBtnSize[0] - self.settingsBtnSize[1] - 20)

        self.deleteAllDataButton = settingsButton(self.settingsMenu, self.settingsBtnSize)
        self.deleteAllDataButton.heading.SetLabel("Delete Data")
        self.deleteAllDataButton.heading.Wrap(self.settingsBtnSize[0] - self.settingsBtnSize[1] - 20)
        self.deleteAllDataButton.icon.SetBitmap(self.deleteAllDataBitmap)
        self.deleteAllDataButton.description.SetLabel("Deletes the captured images")
        self.deleteAllDataButton.description.Wrap(self.settingsBtnSize[0] - self.settingsBtnSize[1] - 20)

        self.autoTimerButton = settingsButton(self.settingsMenu, self.settingsBtnSize)
        self.autoTimerButton.heading.SetLabel("Auto-Timer")
        self.autoTimerButton.heading.Wrap(self.settingsBtnSize[0] - self.settingsBtnSize[1] - 20)
        self.autoTimerButton.icon.SetBitmap(self.autoTimerBitmap)
        self.autoTimerButton.description.SetLabel("Set intervals to make the application run and stop automatically")
        self.autoTimerButton.description.Wrap(self.settingsBtnSize[0] - self.settingsBtnSize[1] - 20)
        self.autoTimerButton.icon.Bind(wx.EVT_LEFT_UP, lambda evt: self.autoTimerButtonClicked(evt))
        self.autoTimerButton.heading.Bind(wx.EVT_LEFT_UP, lambda evt: self.autoTimerButtonClicked(evt))
        self.autoTimerButton.description.Bind(wx.EVT_LEFT_UP,
                                                    lambda evt: self.autoTimerButtonClicked(evt))

        self.pricingButton = settingsButton(self.settingsMenu, self.settingsBtnSize)
        self.pricingButton.heading.SetLabel("Pricing")
        self.pricingButton.heading.Wrap(self.settingsBtnSize[0] - self.settingsBtnSize[1] - 20)
        self.pricingButton.icon.SetBitmap(self.pricingBitmap)
        self.pricingButton.description.SetLabel("Check the estimated cost for your system")
        self.pricingButton.description.Wrap(self.settingsBtnSize[0] - self.settingsBtnSize[1] - 20)

        self.LayoutSettingsMenuOptions.Add(self.changeAdminPassButton, wx.GBPosition(0, 0), wx.GBSpan(1, 1),
                                           wx.EXPAND | wx.ALL, 10)
        self.LayoutSettingsMenuOptions.Add(self.changeViewerPassButton, wx.GBPosition(0, 1), wx.GBSpan(1, 1),
                                           wx.EXPAND | wx.ALL, 10)
        self.LayoutSettingsMenuOptions.Add(self.updateActivationKeyButton, wx.GBPosition(1, 0), wx.GBSpan(1, 1),
                                           wx.EXPAND | wx.ALL, 10)
        self.LayoutSettingsMenuOptions.Add(self.updateAppButton, wx.GBPosition(1, 1), wx.GBSpan(1, 1),
                                           wx.EXPAND | wx.ALL, 10)
        self.LayoutSettingsMenuOptions.Add(self.factoryResetButton, wx.GBPosition(2, 0), wx.GBSpan(1, 1),
                                           wx.EXPAND | wx.ALL, 10)
        self.LayoutSettingsMenuOptions.Add(self.deleteAllDataButton, wx.GBPosition(2, 1), wx.GBSpan(1, 1),
                                           wx.EXPAND | wx.ALL, 10)
        self.LayoutSettingsMenuOptions.Add(self.autoTimerButton, wx.GBPosition(3, 0), wx.GBSpan(1, 1),
                                           wx.EXPAND | wx.ALL, 10)
        self.LayoutSettingsMenuOptions.Add(self.pricingButton, wx.GBPosition(3, 1), wx.GBSpan(1, 1), wx.EXPAND | wx.ALL,
                                           10)

        self.settingsMenu.SetSizer(self.LayoutSettingsMenuOptions)
        self.LayoutSettingsMenuOptions.Fit(self.settingsMenu)

        # LayoutSettingsMenu.Add((0, 0), proportion=1, flag=wx.EXPAND | wx.ALL, border=0)
        LayoutSettingsMenu.Add(self.settingsMenu, proportion=0, flag=wx.CENTER | wx.ALL, border=20)
        LayoutSettingsMenu.Add((0, 0), proportion=1, flag=wx.EXPAND | wx.ALL, border=0)

        self.settingsMenuPanel.SetSizer(LayoutSettingsMenu)
        LayoutSettingsMenu.Fit(self.settingsMenuPanel)

        #################HIDDEN PANELS START HERE

        ##### 1) PASSWORD CHANGE PANEL
        self.passChangePanel = wx.Panel(self.settingsPanel, -1)
        self.passChangePanel.SetBackgroundColour(self.darkGrey)

        LayoutpassChangePanel = wx.BoxSizer(wx.VERTICAL)

        self.passChangeFields = wx.Panel(self.passChangePanel, -1)
        self.passChangeFields.SetBackgroundColour(self.Grey)

        LayoutpassChangeFields = wx.GridBagSizer(10, 10)

        self.passChangeHeading = wx.StaticText(self.passChangeFields, -1, "HEADING")
        self.passChangeHeading.SetForegroundColour(self.faintWhite)
        self.passChangeHeading.SetFont(self.fontBold)
        currentPasswordLabel = wx.StaticText(self.passChangeFields, -1, "Current Password")
        currentPasswordLabel.SetForegroundColour(self.faintWhite)
        newPasswordLabel = wx.StaticText(self.passChangeFields, -1, "New Password")
        newPasswordLabel.SetForegroundColour(self.faintWhite)
        self.currentPasswordEntry = wx.TextCtrl(self.passChangeFields, -1, style=wx.TE_PASSWORD)
        self.newPasswordEntry = wx.TextCtrl(self.passChangeFields, -1, style=wx.TE_PASSWORD)
        self.confirmPassChangebutton = wx.Button(self.passChangeFields, -1, "Confirm", style=wx.NO_BORDER)
        self.confirmPassChangebutton.SetForegroundColour(self.white)
        self.confirmPassChangebutton.SetBackgroundColour(self.darkGrey)
        self.confirmPassChangebutton.Bind(wx.EVT_ENTER_WINDOW, lambda evt: self.changeColor(evt, self.slightlyLightGrey))
        self.confirmPassChangebutton.Bind(wx.EVT_LEAVE_WINDOW, lambda evt: self.changeColor(evt, self.darkGrey))
        self.confirmPassChangebutton.Bind(wx.EVT_LEFT_DOWN, lambda evt: self.changeColor(evt, self.lightGrey))
        self.confirmPassChangebutton.Bind(wx.EVT_LEFT_UP, lambda evt: self.changeColor(self.confirmPassChangebuttonClicked(evt),
                                                                                    self.slightlyLightGrey))

        self.cancelPassChangebutton = wx.Button(self.passChangeFields, -1, "Cancel", style=wx.NO_BORDER)
        self.cancelPassChangebutton.SetForegroundColour(self.white)
        self.cancelPassChangebutton.SetBackgroundColour(self.darkGrey)
        self.cancelPassChangebutton.Bind(wx.EVT_ENTER_WINDOW,
                                          lambda evt: self.changeColor(evt, self.slightlyLightGrey))
        self.cancelPassChangebutton.Bind(wx.EVT_LEAVE_WINDOW, lambda evt: self.changeColor(evt, self.darkGrey))
        self.cancelPassChangebutton.Bind(wx.EVT_LEFT_DOWN, lambda evt: self.changeColor(evt, self.lightGrey))
        self.cancelPassChangebutton.Bind(wx.EVT_LEFT_UP, lambda evt: self.changeColor(self.hideAllForms(evt),
                                                                                       self.slightlyLightGrey))

        LayoutpassChangeFields.SetEmptyCellSize((10, 10))

        LayoutpassChangeFields.Add(self.passChangeHeading, wx.GBPosition(0, 0), wx.GBSpan(1, 11), wx.ALIGN_CENTER | wx.ALL, 10)
        LayoutpassChangeFields.Add(currentPasswordLabel, wx.GBPosition(2, 1), wx.GBSpan(1, 3), wx.EXPAND | wx.ALL)
        LayoutpassChangeFields.Add(self.currentPasswordEntry, wx.GBPosition(2, 5), wx.GBSpan(1, 4), wx.EXPAND | wx.ALL)
        LayoutpassChangeFields.Add(newPasswordLabel, wx.GBPosition(3, 1), wx.GBSpan(1, 3), wx.EXPAND | wx.ALL)
        LayoutpassChangeFields.Add(self.newPasswordEntry, wx.GBPosition(3, 5), wx.GBSpan(1, 4), wx.EXPAND | wx.ALL)
        LayoutpassChangeFields.Add(self.confirmPassChangebutton, wx.GBPosition(5, 2), wx.GBSpan(1, 2), wx.EXPAND | wx.ALL, 10)
        LayoutpassChangeFields.Add(self.cancelPassChangebutton, wx.GBPosition(5, 5), wx.GBSpan(1, 2), wx.EXPAND | wx.ALL, 10)

        self.passChangeFields.SetSizer(LayoutpassChangeFields)
        LayoutpassChangeFields.Fit(self.passChangeFields)

        LayoutpassChangePanel.Add((0, 0), proportion=1, flag=wx.EXPAND | wx.ALL, border=0)
        LayoutpassChangePanel.Add(self.passChangeFields, proportion=0, flag=wx.CENTER | wx.ALL, border=0)
        LayoutpassChangePanel.Add((0, 0), proportion=1, flag=wx.EXPAND | wx.ALL, border=0)

        self.passChangePanel.SetSizer(LayoutpassChangePanel)
        LayoutpassChangePanel.Fit(self.passChangePanel)

        ##### 2) ACTIVATION KEY CHANGE PANEL

        self.activationKeyChangePanel = wx.Panel(self.settingsPanel, -1)
        self.activationKeyChangePanel.SetBackgroundColour(self.darkGrey)

        LayoutactivationKeyChangePanel = wx.BoxSizer(wx.VERTICAL)

        self.activationKeyChangeFields = wx.Panel(self.activationKeyChangePanel, -1)
        self.activationKeyChangeFields.SetBackgroundColour(self.Grey)

        LayoutactivationKeyChangeFields = wx.GridBagSizer(10, 10)

        self.activationKeyChangeHeading = wx.StaticText(self.activationKeyChangeFields, -1, "Activation Key")
        self.activationKeyChangeHeading.SetForegroundColour(self.faintWhite)
        self.activationKeyChangeHeading.SetFont(self.fontBold)
        newKeyLabel = wx.StaticText(self.activationKeyChangeFields, -1, "New Activation Key")
        newKeyLabel.SetForegroundColour(self.faintWhite)
        self.newKeyEntry = wx.TextCtrl(self.activationKeyChangeFields, -1)
        self.confirmActivationKeyChangebutton = wx.Button(self.activationKeyChangeFields, -1, "Confirm", style=wx.NO_BORDER)
        self.confirmActivationKeyChangebutton.SetForegroundColour(self.white)
        self.confirmActivationKeyChangebutton.SetBackgroundColour(self.darkGrey)
        self.confirmActivationKeyChangebutton.Bind(wx.EVT_ENTER_WINDOW,
                                          lambda evt: self.changeColor(evt, self.slightlyLightGrey))
        self.confirmActivationKeyChangebutton.Bind(wx.EVT_LEAVE_WINDOW, lambda evt: self.changeColor(evt, self.darkGrey))
        self.confirmActivationKeyChangebutton.Bind(wx.EVT_LEFT_DOWN, lambda evt: self.changeColor(evt, self.lightGrey))
        self.confirmActivationKeyChangebutton.Bind(wx.EVT_LEFT_UP, lambda evt: self.changeColor(self.confirmKeyChangebuttonClicked(evt),
                                                                                       self.slightlyLightGrey))

        self.cancelKeyChangebutton = wx.Button(self.activationKeyChangeFields, -1, "Cancel", style=wx.NO_BORDER)
        self.cancelKeyChangebutton.SetForegroundColour(self.white)
        self.cancelKeyChangebutton.SetBackgroundColour(self.darkGrey)
        self.cancelKeyChangebutton.Bind(wx.EVT_ENTER_WINDOW,
                                         lambda evt: self.changeColor(evt, self.slightlyLightGrey))
        self.cancelKeyChangebutton.Bind(wx.EVT_LEAVE_WINDOW, lambda evt: self.changeColor(evt, self.darkGrey))
        self.cancelKeyChangebutton.Bind(wx.EVT_LEFT_DOWN, lambda evt: self.changeColor(evt, self.lightGrey))
        self.cancelKeyChangebutton.Bind(wx.EVT_LEFT_UP,
                                         lambda evt: self.changeColor(self.hideAllForms(evt),
                                                                      self.slightlyLightGrey))

        LayoutactivationKeyChangeFields.SetEmptyCellSize((10, 10))

        LayoutactivationKeyChangeFields.Add(self.activationKeyChangeHeading, wx.GBPosition(0, 0), wx.GBSpan(1, 11),
                                   wx.ALIGN_CENTER | wx.ALL, 10)
        LayoutactivationKeyChangeFields.Add(newKeyLabel, wx.GBPosition(2, 1), wx.GBSpan(1, 3), wx.EXPAND | wx.ALL)
        LayoutactivationKeyChangeFields.Add(self.newKeyEntry, wx.GBPosition(2, 5), wx.GBSpan(1, 4), wx.EXPAND | wx.ALL)
        LayoutactivationKeyChangeFields.Add(self.confirmActivationKeyChangebutton, wx.GBPosition(5, 2), wx.GBSpan(1, 2),
                                   wx.EXPAND | wx.ALL, 10)
        LayoutactivationKeyChangeFields.Add(self.cancelKeyChangebutton, wx.GBPosition(5, 5), wx.GBSpan(1, 2),
                                   wx.EXPAND | wx.ALL, 10)

        self.activationKeyChangeFields.SetSizer(LayoutactivationKeyChangeFields)
        LayoutactivationKeyChangeFields.Fit(self.activationKeyChangeFields)

        LayoutactivationKeyChangePanel.Add((0, 0), proportion=1, flag=wx.EXPAND | wx.ALL, border=0)
        LayoutactivationKeyChangePanel.Add(self.activationKeyChangeFields, proportion=0, flag=wx.CENTER | wx.ALL, border=0)
        LayoutactivationKeyChangePanel.Add((0, 0), proportion=1, flag=wx.EXPAND | wx.ALL, border=0)

        self.activationKeyChangePanel.SetSizer(LayoutactivationKeyChangePanel)
        LayoutactivationKeyChangePanel.Fit(self.activationKeyChangePanel)

        ##### 3) Auto Timer CHANGE PANEL

        self.autoTimerPanel = wx.Panel(self.settingsPanel, -1)
        #self.autoTimerPanel.SetScrollRate(5, 5)
        self.autoTimerPanel.SetBackgroundColour(self.darkGrey)

        LayoutautoTimerPanel = wx.BoxSizer(wx.VERTICAL)

        self.autoTimerFields = wx.Panel(self.autoTimerPanel, -1)
        self.autoTimerFields.SetBackgroundColour(self.Grey)

        LayoutAutoTimerFields = wx.GridBagSizer(10, 10)

        self.autoTimerHeading = wx.StaticText(self.autoTimerFields, -1, "Auto Timer Settings")
        self.autoTimerHeading.SetForegroundColour(self.faintWhite)
        self.autoTimerHeading.SetFont(self.fontBold)

        self.addIntervalButton = wx.Button(self.autoTimerFields, -1, "Add Interval", style=wx.NO_BORDER)
        self.addIntervalButton.SetForegroundColour(self.white)
        self.addIntervalButton.SetBackgroundColour(self.darkGrey)
        self.addIntervalButton.Bind(wx.EVT_ENTER_WINDOW,
                                        lambda evt: self.changeColor(evt, self.slightlyLightGrey))
        self.addIntervalButton.Bind(wx.EVT_LEAVE_WINDOW, lambda evt: self.changeColor(evt, self.darkGrey))
        self.addIntervalButton.Bind(wx.EVT_LEFT_DOWN, lambda evt: self.changeColor(evt, self.lightGrey))
        self.addIntervalButton.Bind(wx.EVT_LEFT_UP,
                                        lambda evt: self.changeColor(self.autoTimerAddIntervalClicked(evt),
                                                                     self.slightlyLightGrey))

        self.autoTimerHelpButton = wx.Button(self.autoTimerFields, -1, "Help ?", style=wx.NO_BORDER)
        self.autoTimerHelpButton.SetForegroundColour(self.white)
        self.autoTimerHelpButton.SetBackgroundColour(self.darkGrey)
        self.autoTimerHelpButton.Bind(wx.EVT_ENTER_WINDOW,
                                    lambda evt: self.changeColor(evt, self.slightlyLightGrey))
        self.autoTimerHelpButton.Bind(wx.EVT_LEAVE_WINDOW, lambda evt: self.changeColor(evt, self.darkGrey))
        self.autoTimerHelpButton.Bind(wx.EVT_LEFT_DOWN, lambda evt: self.changeColor(evt, self.lightGrey))
        self.autoTimerHelpButton.Bind(wx.EVT_LEFT_UP,
                                    lambda evt: self.changeColor(evt,
                                                                 self.slightlyLightGrey))

        self.confirmAutoTimerbutton = wx.Button(self.autoTimerFields, -1, "Confirm",
                                                          style=wx.NO_BORDER)
        self.confirmAutoTimerbutton.SetForegroundColour(self.white)
        self.confirmAutoTimerbutton.SetBackgroundColour(self.darkGrey)
        self.confirmAutoTimerbutton.Bind(wx.EVT_ENTER_WINDOW,
                                                   lambda evt: self.changeColor(evt, self.slightlyLightGrey))
        self.confirmAutoTimerbutton.Bind(wx.EVT_LEAVE_WINDOW,
                                                   lambda evt: self.changeColor(evt, self.darkGrey))
        self.confirmAutoTimerbutton.Bind(wx.EVT_LEFT_DOWN, lambda evt: self.changeColor(evt, self.lightGrey))
        self.confirmAutoTimerbutton.Bind(wx.EVT_LEFT_UP, lambda evt: self.changeColor(evt,
                                                                                                self.slightlyLightGrey))

        self.cancelAutoTimerebutton = wx.Button(self.autoTimerFields, -1, "Cancel", style=wx.NO_BORDER)
        self.cancelAutoTimerebutton.SetForegroundColour(self.white)
        self.cancelAutoTimerebutton.SetBackgroundColour(self.darkGrey)
        self.cancelAutoTimerebutton.Bind(wx.EVT_ENTER_WINDOW,
                                        lambda evt: self.changeColor(evt, self.slightlyLightGrey))
        self.cancelAutoTimerebutton.Bind(wx.EVT_LEAVE_WINDOW, lambda evt: self.changeColor(evt, self.darkGrey))
        self.cancelAutoTimerebutton.Bind(wx.EVT_LEFT_DOWN, lambda evt: self.changeColor(evt, self.lightGrey))
        self.cancelAutoTimerebutton.Bind(wx.EVT_LEFT_UP,
                                        lambda evt: self.changeColor(self.hideAllForms(evt),
                                                                     self.slightlyLightGrey))

        self.autoTimerIntervalPanel = wx.Panel(self.autoTimerFields, -1)
        #self.autoTimerIntervalPanel.SetMinSize((-1, 100))

        LayoutAutoTimerInterval = wx.BoxSizer(wx.VERTICAL)

        self.intervalHeadLabel = wx.StaticText(self.autoTimerIntervalPanel, -1, "Interval", size=(80, -1), style=wx.ALIGN_CENTER)
        self.intervalHeadLabel.SetForegroundColour(self.faintWhite)
        self.intervalHeadLabel.SetFont(self.fontBold)
        self.startAllHeadLabel = wx.StaticText(self.autoTimerIntervalPanel, -1, "Start All", size=(80, -1), style=wx.ALIGN_CENTER)
        self.startAllHeadLabel.SetForegroundColour(self.faintWhite)
        self.startAllHeadLabel.SetFont(self.fontBold)
        self.stopAllHeadLabel = wx.StaticText(self.autoTimerIntervalPanel, -1, "Stop All", size=(80, -1), style=wx.ALIGN_CENTER)
        self.stopAllHeadLabel.SetForegroundColour(self.faintWhite)
        self.stopAllHeadLabel.SetFont(self.fontBold)
        self.weekHeadLabel = wx.StaticText(self.autoTimerIntervalPanel, -1, "Week", size=(270, -1), style=wx.ALIGN_CENTER)
        self.weekHeadLabel.SetForegroundColour(self.faintWhite)
        self.weekHeadLabel.SetFont(self.fontBold)

        self.LayoutAutoTimerIntervalList = wx.GridBagSizer(10, 0)
        self.LayoutAutoTimerIntervalList.SetEmptyCellSize((10, 10))

        self.LayoutAutoTimerIntervalList.Add(self.intervalHeadLabel, wx.GBPosition(0, 0), wx.GBSpan(1, 2), wx.EXPAND | wx.ALL)
        self.LayoutAutoTimerIntervalList.Add(self.startAllHeadLabel, wx.GBPosition(0, 6), wx.GBSpan(1, 2), wx.EXPAND | wx.ALL)
        self.LayoutAutoTimerIntervalList.Add(self.stopAllHeadLabel, wx.GBPosition(0, 9), wx.GBSpan(1, 2), wx.EXPAND | wx.ALL)
        self.LayoutAutoTimerIntervalList.Add(self.weekHeadLabel, wx.GBPosition(0, 15), wx.GBSpan(1, 13), wx.EXPAND | wx.ALL)

        LayoutAutoTimerInterval.Add(self.LayoutAutoTimerIntervalList, proportion=0, flag=wx.EXPAND | wx.ALL)

        self.autoTimerIntervalPanel.SetSizer(LayoutAutoTimerInterval)
        LayoutAutoTimerInterval.Fit(self.autoTimerIntervalPanel)

        LayoutAutoTimerFields.SetEmptyCellSize((10, 10))

        LayoutAutoTimerFields.Add(self.autoTimerHeading, wx.GBPosition(0, 0), wx.GBSpan(1, 11),
                                            wx.ALIGN_CENTER | wx.ALL, 10)
        LayoutAutoTimerFields.Add(self.addIntervalButton, wx.GBPosition(1, 0), wx.GBSpan(1, 2),
                                  wx.ALIGN_CENTER | wx.ALL, 10)
        LayoutAutoTimerFields.Add(self.autoTimerHelpButton, wx.GBPosition(1, 10), wx.GBSpan(1, 1),
                                  wx.ALIGN_CENTER | wx.ALL, 10)
        LayoutAutoTimerFields.Add(self.autoTimerIntervalPanel, wx.GBPosition(2, 0), wx.GBSpan(1, 11),
                                  wx.ALIGN_CENTER | wx.ALL, 10)
        LayoutAutoTimerFields.Add(self.confirmAutoTimerbutton, wx.GBPosition(3, 4), wx.GBSpan(1, 2),
                                  wx.ALIGN_CENTER | wx.ALL, 10)
        LayoutAutoTimerFields.Add(self.cancelAutoTimerebutton, wx.GBPosition(3, 6), wx.GBSpan(1, 2),
                                  wx.ALIGN_CENTER | wx.ALL, 10)

        self.autoTimerFields.SetSizer(LayoutAutoTimerFields)
        LayoutAutoTimerFields.Fit(self.autoTimerFields)

        LayoutautoTimerPanel.Add((0, 0), proportion=1, flag=wx.EXPAND | wx.ALL, border=0)
        LayoutautoTimerPanel.Add(self.autoTimerFields, proportion=0, flag=wx.CENTER | wx.ALL,
                                           border=20)
        LayoutautoTimerPanel.Add((0, 0), proportion=1, flag=wx.EXPAND | wx.ALL, border=0)

        self.autoTimerPanel.SetSizer(LayoutautoTimerPanel)
        LayoutautoTimerPanel.Fit(self.autoTimerPanel)

        LayoutSettingsPanel.Add(self.settingsMenuPanel, proportion=2, flag=wx.EXPAND | wx.ALL, border=0)
        LayoutSettingsPanel.Add(self.passChangePanel, proportion=1, flag=wx.EXPAND | wx.ALL, border=0)
        LayoutSettingsPanel.Add(self.activationKeyChangePanel, proportion=1, flag=wx.EXPAND | wx.ALL, border=0)
        LayoutSettingsPanel.Add(self.autoTimerPanel, proportion=1, flag=wx.EXPAND | wx.ALL, border=0)

        self.passChangePanel.Hide()
        self.activationKeyChangePanel.Hide()
        self.autoTimerPanel.Hide()

        self.settingsPanel.SetSizer(LayoutSettingsPanel)
        LayoutSettingsPanel.Fit(self.settingsPanel)

        self.notificationPanel = wx.ScrolledWindow(self.userPanelContents, pos=wx.DefaultPosition, size=wx.DefaultSize,
                                                style=wx.VSCROLL)
        self.notificationPanel.SetBackgroundColour(self.darkGrey)
        self.notificationPanel.SetMinSize((350, -1))

        LayoutUserPanelContents.Add(self.settingsPanel, proportion=1, flag=wx.EXPAND | wx.ALL, border=0)
        LayoutUserPanelContents.Add(self.notificationPanel, proportion=0, flag=wx.EXPAND | wx.ALL, border=0)

        self.userPanelContents.SetSizer(LayoutUserPanelContents)
        LayoutUserPanelContents.Fit(self.userPanelContents)

        self.settingsPanel.Layout()

        LayoutUserPanel.Add(self.userPanelHeadPanel, proportion=0, flag=wx.EXPAND | wx.ALL, border=0)
        LayoutUserPanel.Add(self.userPanelContents, proportion=1, flag=wx.EXPAND | wx.ALL, border=0)

        self.userPanel.SetSizer(LayoutUserPanel)
        LayoutUserPanel.Fit(self.userPanel)

        self.SetSizer(LayoutMain)
        LayoutMain.Fit(self)

        self.Bind(wx.EVT_SIZE, self.userPageSizeChanged)

        self.Center()
        self.Show(True)
        self.Layout()

    def autoTimerAddIntervalClicked(self, event):
        self.autoTimerRows = self.autoTimerRows + 1
        self.addAutoTimerIntervalRow(self.autoTimerRows)
        return event

    def addAutoTimerIntervalRow(self, rowNo):
        intervalCheckbox = wx.CheckBox(self.autoTimerIntervalPanel, -1, "Interval " + str(rowNo), name="timerCheckbox-" + str(rowNo))
        intervalCheckbox.SetForegroundColour(self.faintWhite)
        startAllHourEntry = wx.ComboBox(self.autoTimerIntervalPanel, -1, size=(40, -1), name="timerStartAllHour-" + str(rowNo))
        startAllHourEntry.SetEditable(False)
        startAllMinsEntry = wx.ComboBox(self.autoTimerIntervalPanel, -1, size=(40, -1), name="timerStartAllMin-" + str(rowNo))
        startAllMinsEntry.SetEditable(False)
        stopAllHourEntry = wx.ComboBox(self.autoTimerIntervalPanel, -1, size=(40, -1), name="timerStopAllHour-" + str(rowNo))
        stopAllHourEntry.SetEditable(False)
        stopAllMinsEntry = wx.ComboBox(self.autoTimerIntervalPanel, -1, size=(40, -1), name="timerStopAllMin-" + str(rowNo))
        stopAllMinsEntry.SetEditable(False)
        monWeekButton = wx.ToggleButton(self.autoTimerIntervalPanel, -1, "M", size=(30, -1), name="timerWeekMon-" + str(rowNo), style=wx.NO_BORDER)
        monWeekButton.SetForegroundColour(self.white)
        monWeekButton.SetBackgroundColour(self.Grey)
        monWeekButton.Bind(wx.EVT_ENTER_WINDOW,
                                         lambda evt: self.changeColor(evt, self.darkGrey))
        monWeekButton.Bind(wx.EVT_LEAVE_WINDOW, lambda evt: self.changeColor(evt, self.weekToggleColor(evt)))
        monWeekButton.Bind(wx.EVT_LEFT_DOWN, lambda evt: self.changeColor(evt, self.lightGrey))
        monWeekButton.Bind(wx.EVT_LEFT_UP,
                                         lambda evt: self.changeColor(self.timerWeekButtonClicked(evt),
                                                                      self.weekToggleColor(evt)))
        #monWeekButton.Bind(wx.EVT_TOGGLEBUTTON, lambda evt: self.changeColor(evt, self.weekToggleColor(evt)))
        tueWeekButton = wx.ToggleButton(self.autoTimerIntervalPanel, -1, "T", size=(30, -1), name="timerWeekTue-" + str(rowNo), style=wx.NO_BORDER)
        tueWeekButton.SetForegroundColour(self.white)
        tueWeekButton.SetBackgroundColour(self.Grey)
        tueWeekButton.Bind(wx.EVT_ENTER_WINDOW,
                           lambda evt: self.changeColor(evt, self.darkGrey))
        tueWeekButton.Bind(wx.EVT_LEAVE_WINDOW, lambda evt: self.changeColor(evt, self.weekToggleColor(evt)))
        tueWeekButton.Bind(wx.EVT_LEFT_DOWN, lambda evt: self.changeColor(evt, self.lightGrey))
        tueWeekButton.Bind(wx.EVT_LEFT_UP,
                           lambda evt: self.changeColor(self.timerWeekButtonClicked(evt),
                                                        self.weekToggleColor(evt)))
        #tueWeekButton.Bind(wx.EVT_TOGGLEBUTTON, lambda evt: self.changeColor(evt, self.weekToggleColor(evt)))
        wedWeekButton = wx.ToggleButton(self.autoTimerIntervalPanel, -1, "W", size=(30, -1), name="timerWeekWed-" + str(rowNo), style=wx.NO_BORDER)
        wedWeekButton.SetForegroundColour(self.white)
        wedWeekButton.SetBackgroundColour(self.Grey)
        wedWeekButton.Bind(wx.EVT_ENTER_WINDOW,
                           lambda evt: self.changeColor(evt, self.darkGrey))
        wedWeekButton.Bind(wx.EVT_LEAVE_WINDOW, lambda evt: self.changeColor(evt, self.weekToggleColor(evt)))
        wedWeekButton.Bind(wx.EVT_LEFT_DOWN, lambda evt: self.changeColor(evt, self.lightGrey))
        wedWeekButton.Bind(wx.EVT_LEFT_UP,
                           lambda evt: self.changeColor(self.timerWeekButtonClicked(evt),
                                                        self.weekToggleColor(evt)))
        #wedWeekButton.Bind(wx.EVT_TOGGLEBUTTON, lambda evt: self.changeColor(evt, self.weekToggleColor(evt)))
        thuWeekButton = wx.ToggleButton(self.autoTimerIntervalPanel, -1, "T", size=(30, -1), name="timerWeekThu-" + str(rowNo), style=wx.NO_BORDER)
        thuWeekButton.SetForegroundColour(self.white)
        thuWeekButton.SetBackgroundColour(self.Grey)
        thuWeekButton.Bind(wx.EVT_ENTER_WINDOW,
                           lambda evt: self.changeColor(evt, self.darkGrey))
        thuWeekButton.Bind(wx.EVT_LEAVE_WINDOW, lambda evt: self.changeColor(evt, self.weekToggleColor(evt)))
        thuWeekButton.Bind(wx.EVT_LEFT_DOWN, lambda evt: self.changeColor(evt, self.lightGrey))
        thuWeekButton.Bind(wx.EVT_LEFT_UP,
                           lambda evt: self.changeColor(self.timerWeekButtonClicked(evt),
                                                        self.weekToggleColor(evt)))
        #thuWeekButton.Bind(wx.EVT_TOGGLEBUTTON, lambda evt: self.changeColor(evt, self.weekToggleColor(evt)))
        friWeekButton = wx.ToggleButton(self.autoTimerIntervalPanel, -1, "F", size=(30, -1), name="timerWeekFri-" + str(rowNo), style=wx.NO_BORDER)
        friWeekButton.SetForegroundColour(self.white)
        friWeekButton.SetBackgroundColour(self.Grey)
        friWeekButton.Bind(wx.EVT_ENTER_WINDOW,
                           lambda evt: self.changeColor(evt, self.darkGrey))
        friWeekButton.Bind(wx.EVT_LEAVE_WINDOW, lambda evt: self.changeColor(evt, self.weekToggleColor(evt)))
        friWeekButton.Bind(wx.EVT_LEFT_DOWN, lambda evt: self.changeColor(evt, self.lightGrey))
        friWeekButton.Bind(wx.EVT_LEFT_UP,
                           lambda evt: self.changeColor(self.timerWeekButtonClicked(evt),
                                                        self.weekToggleColor(evt)))
        #friWeekButton.Bind(wx.EVT_TOGGLEBUTTON, lambda evt: self.changeColor(evt, self.weekToggleColor(evt)))
        satWeekButton = wx.ToggleButton(self.autoTimerIntervalPanel, -1, "S", size=(30, -1), name="timerWeekSat-" + str(rowNo), style=wx.NO_BORDER)
        satWeekButton.SetForegroundColour(self.white)
        satWeekButton.SetBackgroundColour(self.Grey)
        satWeekButton.Bind(wx.EVT_ENTER_WINDOW,
                           lambda evt: self.changeColor(evt, self.darkGrey))
        satWeekButton.Bind(wx.EVT_LEAVE_WINDOW, lambda evt: self.changeColor(evt, self.weekToggleColor(evt)))
        satWeekButton.Bind(wx.EVT_LEFT_DOWN, lambda evt: self.changeColor(evt, self.lightGrey))
        satWeekButton.Bind(wx.EVT_LEFT_UP,
                           lambda evt: self.changeColor(self.timerWeekButtonClicked(evt),
                                                        self.weekToggleColor(evt)))
        #satWeekButton.Bind(wx.EVT_TOGGLEBUTTON, lambda evt: self.changeColor(evt, self.weekToggleColor(evt)))
        sunWeekButton = wx.ToggleButton(self.autoTimerIntervalPanel, -1, "S", size=(30, -1), name="timerWeekSun-" + str(rowNo), style=wx.NO_BORDER)
        sunWeekButton.SetForegroundColour(self.white)
        sunWeekButton.SetBackgroundColour(self.Grey)
        sunWeekButton.Bind(wx.EVT_ENTER_WINDOW,
                           lambda evt: self.changeColor(evt, self.darkGrey))
        sunWeekButton.Bind(wx.EVT_LEAVE_WINDOW, lambda evt: self.changeColor(evt, self.weekToggleColor(evt)))
        sunWeekButton.Bind(wx.EVT_LEFT_DOWN, lambda evt: self.changeColor(evt, self.lightGrey))
        sunWeekButton.Bind(wx.EVT_LEFT_UP,
                           lambda evt: self.changeColor(self.timerWeekButtonClicked(evt),
                                                        self.weekToggleColor(evt)))
        #sunWeekButton.Bind(wx.EVT_TOGGLEBUTTON, lambda  evt: self.changeColor(evt, self.weekToggleColor(evt)))

        for i in range(0, 60):
            if(i < 24):
                startAllHourEntry.Append(str(i))
                stopAllHourEntry.Append(str(i))
            startAllMinsEntry.Append(str(i))
            stopAllMinsEntry.Append(str(i))

        self.LayoutAutoTimerIntervalList.Add(intervalCheckbox, wx.GBPosition(rowNo, 0), wx.GBSpan(1, 2), wx.EXPAND | wx.ALL)
        self.LayoutAutoTimerIntervalList.Add(startAllHourEntry, wx.GBPosition(rowNo, 6), wx.GBSpan(1, 1),
                                             wx.EXPAND | wx.ALL)
        self.LayoutAutoTimerIntervalList.Add(startAllMinsEntry, wx.GBPosition(rowNo, 7), wx.GBSpan(1, 1),
                                             wx.EXPAND | wx.ALL)
        self.LayoutAutoTimerIntervalList.Add(stopAllHourEntry, wx.GBPosition(rowNo, 9), wx.GBSpan(1, 1),
                                             wx.EXPAND | wx.ALL)
        self.LayoutAutoTimerIntervalList.Add(stopAllMinsEntry, wx.GBPosition(rowNo, 10), wx.GBSpan(1, 1),
                                             wx.EXPAND | wx.ALL)
        self.LayoutAutoTimerIntervalList.Add(monWeekButton, wx.GBPosition(rowNo, 15), wx.GBSpan(1, 1),
                                             wx.EXPAND | wx.ALL)
        self.LayoutAutoTimerIntervalList.Add(tueWeekButton, wx.GBPosition(rowNo, 17), wx.GBSpan(1, 1),
                                             wx.EXPAND | wx.ALL)
        self.LayoutAutoTimerIntervalList.Add(wedWeekButton, wx.GBPosition(rowNo, 19), wx.GBSpan(1, 1),
                                             wx.EXPAND | wx.ALL)
        self.LayoutAutoTimerIntervalList.Add(thuWeekButton, wx.GBPosition(rowNo, 21), wx.GBSpan(1, 1),
                                             wx.EXPAND | wx.ALL)
        self.LayoutAutoTimerIntervalList.Add(friWeekButton, wx.GBPosition(rowNo, 23), wx.GBSpan(1, 1),
                                             wx.EXPAND | wx.ALL)
        self.LayoutAutoTimerIntervalList.Add(satWeekButton, wx.GBPosition(rowNo, 25), wx.GBSpan(1, 1),
                                             wx.EXPAND | wx.ALL)
        self.LayoutAutoTimerIntervalList.Add(sunWeekButton, wx.GBPosition(rowNo, 27), wx.GBSpan(1, 1),
                                             wx.EXPAND | wx.ALL)

        tmpList = []
        tmpList.append(intervalCheckbox)
        tmpList.append(startAllHourEntry)
        tmpList.append(startAllMinsEntry)
        tmpList.append(stopAllHourEntry)
        tmpList.append(stopAllMinsEntry)
        tmpList.append(monWeekButton)
        tmpList.append(tueWeekButton)
        tmpList.append(wedWeekButton)
        tmpList.append(thuWeekButton)
        tmpList.append(friWeekButton)
        tmpList.append(satWeekButton)
        tmpList.append(sunWeekButton)

        self.autoTimerRowList.append(tmpList)

        self.Layout()

    def scaleImages(self, imageBitmap, imageSize):
        image = wx.Bitmap.ConvertToImage(imageBitmap)
        image = image.Scale(imageSize[0], imageSize[1], wx.IMAGE_QUALITY_HIGH)
        return wx.Bitmap(image)

    # def cancelKeyChangebuttonClicked(self, event):
    #     self.activationKeyChangePanel.Hide()
    #     self.Layout()
    #     return event
    #
    # def cancelPassChangebuttonClicked(self, event):
    #     self.passChangePanel.Hide()
    #     self.Layout()
    #     return event

    def hideAllForms(self, event):
        self.passChangePanel.Hide()
        self.activationKeyChangePanel.Hide()
        self.autoTimerPanel.Hide()
        self.newKeyEntry.SetValue("")
        self.currentPasswordEntry.SetValue("")
        self.newPasswordEntry.SetValue("")
        self.Layout()
        return event

    def changeKeyClicked(self, event):
        self.hideAllForms(None)
        self.activationKeyChangePanel.Show(True)
        self.Layout()
        self.settingsPanel.Scroll((0, 100))

    def changePassClicked(self, event, type):
        self.hideAllForms(None)
        self.passChangePanel.SetName(type)
        if(type == "Admin"):
            self.passChangeHeading.SetLabel(type + " Password")
            self.passChangePanel.Show(True)
        else:
            self.passChangeHeading.SetLabel(type + " Password")
            self.passChangePanel.Show(True)
        self.Layout()
        self.settingsPanel.Scroll((0, 100))

    def autoTimerButtonClicked(self, event):
        self.hideAllForms(None)
        self.autoTimerPanel.Show(True)
        self.Layout()
        self.settingsPanel.Scroll((0, 100))

    def changeSettingsMenuLayout(self):

        if(self.GetSize()[0] > 1340):
            self.LayoutSettingsMenuOptions.Clear(False)

            self.LayoutSettingsMenuOptions.Add(self.changeAdminPassButton, wx.GBPosition(0, 0), wx.GBSpan(1, 1),
                                          wx.EXPAND | wx.ALL, 10)
            self.LayoutSettingsMenuOptions.Add(self.changeViewerPassButton, wx.GBPosition(0, 1), wx.GBSpan(1, 1),
                                          wx.EXPAND | wx.ALL, 10)
            self.LayoutSettingsMenuOptions.Add(self.updateActivationKeyButton, wx.GBPosition(0, 2), wx.GBSpan(1, 1),
                                          wx.EXPAND | wx.ALL, 10)
            self.LayoutSettingsMenuOptions.Add(self.updateAppButton, wx.GBPosition(1, 0), wx.GBSpan(1, 1), wx.EXPAND | wx.ALL,
                                          10)
            self.LayoutSettingsMenuOptions.Add(self.factoryResetButton, wx.GBPosition(1, 1), wx.GBSpan(1, 1), wx.EXPAND | wx.ALL,
                                          10)
            self.LayoutSettingsMenuOptions.Add(self.deleteAllDataButton, wx.GBPosition(1, 2), wx.GBSpan(1, 1),
                                          wx.EXPAND | wx.ALL, 10)
            self.LayoutSettingsMenuOptions.Add(self.autoTimerButton, wx.GBPosition(2, 0), wx.GBSpan(1, 1), wx.EXPAND | wx.ALL,
                                          10)
            self.LayoutSettingsMenuOptions.Add(self.pricingButton, wx.GBPosition(2, 1), wx.GBSpan(1, 1), wx.EXPAND | wx.ALL, 10)
        else:
            self.LayoutSettingsMenuOptions.Clear(False)
            self.LayoutSettingsMenuOptions.Add(self.changeAdminPassButton, wx.GBPosition(0, 0), wx.GBSpan(1, 1),
                                               wx.EXPAND | wx.ALL, 10)
            self.LayoutSettingsMenuOptions.Add(self.changeViewerPassButton, wx.GBPosition(0, 1), wx.GBSpan(1, 1),
                                               wx.EXPAND | wx.ALL, 10)
            self.LayoutSettingsMenuOptions.Add(self.updateActivationKeyButton, wx.GBPosition(1, 0), wx.GBSpan(1, 1),
                                               wx.EXPAND | wx.ALL, 10)
            self.LayoutSettingsMenuOptions.Add(self.updateAppButton, wx.GBPosition(1, 1), wx.GBSpan(1, 1),
                                               wx.EXPAND | wx.ALL, 10)
            self.LayoutSettingsMenuOptions.Add(self.factoryResetButton, wx.GBPosition(2, 0), wx.GBSpan(1, 1),
                                               wx.EXPAND | wx.ALL, 10)
            self.LayoutSettingsMenuOptions.Add(self.deleteAllDataButton, wx.GBPosition(2, 1), wx.GBSpan(1, 1),
                                               wx.EXPAND | wx.ALL, 10)
            self.LayoutSettingsMenuOptions.Add(self.autoTimerButton, wx.GBPosition(3, 0), wx.GBSpan(1, 1),
                                               wx.EXPAND | wx.ALL, 10)
            self.LayoutSettingsMenuOptions.Add(self.pricingButton, wx.GBPosition(3, 1), wx.GBSpan(1, 1),
                                               wx.EXPAND | wx.ALL, 10)
        self.Layout()
        self.settingsPanel.Layout()

    def userPageSizeChanged(self, event):
        self.Layout()
        wx.CallAfter(self.changeSettingsMenuLayout)

    def timerWeekButtonClicked(self, event):
        if(event.GetEventObject().GetValue()):
            event.GetEventObject().SetValue(False)
        else:
            event.GetEventObject().SetValue(True)

    def weekToggleColor(self, event):
        if(event.GetEventObject().GetValue()):
            return self.darkGrey
        else:
            return self.Grey

    def changeColor(self, event, newcolor):
        event.GetEventObject().SetBackgroundColour(newcolor)
        
    def changeAdminPass(self, oldPass,newPass):
        with open(two_up + '/DATA/userSetting.txt','r') as file:
            data=file.read()
        cipher=Fernet(self.encryptionKey)
        userSetting=ast.literal_eval((cipher.decrypt(data.encode('utf-8'))).decode('utf-8'))
        if(userSetting["adminPass"]==oldPass):
            userSetting["adminPass"]=newPass
            encrypted=cipher.encrypt(str(userSetting).encode('utf-8'))
            with open(two_up + '/DATA/userSetting.txt','w') as file:
                file.write(encrypted.decode('utf-8'))
            return 1
        else:
            return 0
    
    def changeViewerPass(self, oldPass,newPass):
        with open(two_up + '/DATA/userSetting.txt','r') as file:
            data=file.read()
        cipher=Fernet(self.encryptionKey)
        userSetting=ast.literal_eval((cipher.decrypt(data.encode('utf-8'))).decode('utf-8'))
        if(userSetting["viewerPass"]==oldPass):
            userSetting["viewerPass"]=newPass
            encrypted=cipher.encrypt(str(userSetting).encode('utf-8'))
            with open(two_up + '/DATA/userSetting.txt','w') as file:
                file.write(encrypted.decode('utf-8'))
            return 1
        else:
            return 0
    
    def changeActivationKey(self, key):
        with open(two_up + '/DATA/userSetting.txt','r') as file:
            data=file.read()
        cipher=Fernet(self.encryptionKey)
        userSetting=ast.literal_eval((cipher.decrypt(data.encode('utf-8'))).decode('utf-8'))
        userSetting["activationKey"]=key
        encrypted=cipher.encrypt(str(userSetting).encode('utf-8'))
        with open(two_up + '/DATA/userSetting.txt','w') as file:
            file.write(encrypted.decode('utf-8'))

    def confirmPassChangebuttonClicked(self, event):
        type = self.passChangePanel.GetName()
        oldPass = self.currentPasswordEntry.GetValue()
        newPass = self.newPasswordEntry.GetValue()
        if(type == "Admin"):
            if(newPass == ""):
                msgBox = wx.MessageBox("Admin password changed failed!", "Admin Password", parent=self)
            else:
                if(self.changeAdminPass(oldPass, newPass)):
                    msgBox = wx.MessageBox("Admin password changed successfully", "Admin Password", parent=self)
                    self.hideAllForms(None)
                else:
                    msgBox = wx.MessageBox("Admin password change failed. Current Admin password is incorrect!", "Admin Password", parent=self)
        elif(type == "Viewer"):
            if (newPass == ""):
                msgBox = wx.MessageBox("Viewer password changed failed!", "Viewer Password", parent=self)
            else:
                if (self.changeViewerPass(oldPass, newPass)):
                    msgBox = wx.MessageBox("Viewer password changed successfully", "Viewer Password", parent=self)
                    self.hideAllForms(None)
                else:
                    msgBox = wx.MessageBox("Viewer password change failed. Current Viewer password is incorrect!",
                                           "Viewer Password", parent=self)

        return event

    def confirmKeyChangebuttonClicked(self, event):
        newKey = self.newKeyEntry.GetValue()
        if(not (newKey == "")):
            self.changeActivationKey(newKey)
            msgBox = wx.MessageBox("Activation Key changed successfully", "Activation Key", parent=self)
        else:
            msgBox = wx.MessageBox("Activation Key change failed!", "Activation Key", parent=self)
        return event

#app = wx.App()
#window = User(None)
#app.MainLoop()