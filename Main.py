import wx
import Dashboard
import Calibration
import Configuration

class MainFrame(wx.Frame):

    def __init__(self):
        super(MainFrame, self).__init__(None, title="Yantrakar", size=(1100, 750))
        self.SetMinSize((1100, 750))

        self.current_page = 1

        self.initUI()

    def initUI(self):
        self.fontNormal = wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        self.fontBold = wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        self.darkOrange = wx.Colour(255, 191, 0)
        self.lightOrange = wx.Colour(248, 217, 122)
        self.darkGrey = wx.Colour(50, 50, 50)
        self.Grey = wx.Colour(70, 70, 70)
        self.lightGrey = wx.Colour(100, 100, 100)
        self.slightlyLightGrey = wx.Colour(80, 80, 80)
        self.faintWhite = wx.Colour(200, 200, 200)
        self.white = wx.Colour(255, 255, 255)

        self.DashboardIcon = wx.Bitmap("ui_elements/Dashboard.png")
        self.ConfigIcon = wx.Bitmap("ui_elements/Config.png")
        self.CalibrationIcon = wx.Bitmap("ui_elements/Calibration.png")
        self.HelpIcon = wx.Bitmap("ui_elements/Help.png")
        self.UserIcon = wx.Bitmap("ui_elements/User.png")

        NavIconSize = wx.Size(20, 20)

        self.DashboardIcon = self.scaleIcons(self.DashboardIcon, NavIconSize)
        self.ConfigIcon = self.scaleIcons(self.ConfigIcon, NavIconSize)
        self.CalibrationIcon = self.scaleIcons(self.CalibrationIcon, NavIconSize)
        self.HelpIcon = self.scaleIcons(self.HelpIcon, NavIconSize)
        self.UserIcon = self.scaleIcons(self.UserIcon, NavIconSize)

        self.DashboardIcon.SetSize(NavIconSize)
        self.ConfigIcon.SetSize(NavIconSize)
        self.CalibrationIcon.SetSize(NavIconSize)
        self.HelpIcon.SetSize(NavIconSize)
        self.UserIcon.SetSize(NavIconSize)

        self.SetFont(self.fontNormal)
        self.SetBackgroundColour(self.Grey)

        LayoutMain = wx.BoxSizer(wx.HORIZONTAL)

        self.navPanel = wx.Panel(self, pos=wx.DefaultPosition)
        self.navPanel.SetBackgroundColour(self.darkGrey)

        LayoutnavPanel = wx.BoxSizer(wx.VERTICAL)

        LayoutnavPanelUpper = wx.GridBagSizer(0, 0)
        LayoutnavPanelUpper.SetFlexibleDirection(wx.BOTH)
        LayoutnavPanelUpper.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        # Add Dashboard button on Navbar
        self.dashboardNavButton = wx.Button(self.navPanel, -1, u"  Dashboard", wx.DefaultPosition, wx.DefaultSize,
                                            wx.BORDER_NONE | wx.BU_LEFT)
        self.dashboardNavButton.SetForegroundColour(self.white)
        #self.dashboardNavButton.SetBackgroundColour(self.Grey)
        self.dashboardNavButton.SetBackgroundColour(self.darkGrey)
        self.dashboardNavButton.SetBitmap(self.DashboardIcon)

        self.dashboardNavButton.Bind(wx.EVT_ENTER_WINDOW, lambda evt: self.changeColor(evt, self.Grey, 0))
        self.dashboardNavButton.Bind(wx.EVT_LEAVE_WINDOW, lambda evt: self.changeColor(evt, self.darkGrey, 1))
        self.dashboardNavButton.Bind(wx.EVT_LEFT_DOWN, lambda evt: self.changeColor(evt, self.slightlyLightGrey, 0))
        self.dashboardNavButton.Bind(wx.EVT_LEFT_UP,
                                     lambda evt: self.changeColor(self.changePage(evt, 1), self.Grey, 1))
        # self.dashboardNavButton.SetFont(self.fontBold)
        self.dashboardNavButton.SetMinSize(wx.Size(200, 50))
        # self.dashboardNavButton.SetPressColor(self.darkGrey)

        # Add Config button on Navbar
        self.cameraConfigNavButton = wx.Button(self.navPanel, -1, u"  Camera Config", wx.DefaultPosition,
                                               wx.DefaultSize, wx.BORDER_NONE | wx.BU_LEFT)
        self.cameraConfigNavButton.SetForegroundColour(self.white)
        self.cameraConfigNavButton.SetBackgroundColour(self.darkGrey)
        self.cameraConfigNavButton.SetBitmap(self.ConfigIcon)
        self.cameraConfigNavButton.Bind(wx.EVT_ENTER_WINDOW, lambda evt: self.changeColor(evt, self.Grey, 0))
        self.cameraConfigNavButton.Bind(wx.EVT_LEAVE_WINDOW, lambda evt: self.changeColor(evt, self.darkGrey, 1))
        self.cameraConfigNavButton.Bind(wx.EVT_LEFT_DOWN, lambda evt: self.changeColor(evt, self.slightlyLightGrey, 0))
        self.cameraConfigNavButton.Bind(wx.EVT_LEFT_UP,
                                        lambda evt: self.changeColor(self.changePage(evt, 2), self.Grey, 1))
        # self.cameraConfigNavButton.SetFont(self.fontBold)
        self.cameraConfigNavButton.SetMinSize(wx.Size(200, 50))
        # self.cameraConfigNavButton.SetPressColor(self.darkGrey)

        # Add Calibration button on Navbar
        self.calibrationNavButton = wx.Button(self.navPanel, -1, u"  Calibration", wx.DefaultPosition, wx.DefaultSize,
                                              wx.BORDER_NONE | wx.BU_LEFT)
        self.calibrationNavButton.SetForegroundColour(self.white)
        self.calibrationNavButton.SetBackgroundColour(self.darkGrey)
        self.calibrationNavButton.SetBitmap(self.CalibrationIcon)
        self.calibrationNavButton.Bind(wx.EVT_ENTER_WINDOW, lambda evt: self.changeColor(evt, self.Grey, 0))
        self.calibrationNavButton.Bind(wx.EVT_LEAVE_WINDOW, lambda evt: self.changeColor(evt, self.darkGrey, 1))
        self.calibrationNavButton.Bind(wx.EVT_LEFT_DOWN, lambda evt: self.changeColor(evt, self.slightlyLightGrey, 0))
        self.calibrationNavButton.Bind(wx.EVT_LEFT_UP,
                                       lambda evt: self.changeColor(self.changePage(evt, 3), self.Grey, 1))
        # self.calibrationNavButton.SetFont(self.fontBold)
        self.calibrationNavButton.SetMinSize(wx.Size(200, 50))
        # self.calibrationNavButton.SetPressColor(self.darkGrey)

        # Add Help button on Navbar
        self.helpNavButton = wx.Button(self.navPanel, -1, u"  Help", wx.DefaultPosition, wx.DefaultSize,
                                       wx.BORDER_NONE | wx.BU_LEFT)
        self.helpNavButton.SetForegroundColour(self.white)
        self.helpNavButton.SetBackgroundColour(self.darkGrey)
        self.helpNavButton.SetBitmap(self.HelpIcon)
        self.helpNavButton.Bind(wx.EVT_ENTER_WINDOW, lambda evt: self.changeColor(evt, self.Grey, 0))
        self.helpNavButton.Bind(wx.EVT_LEAVE_WINDOW, lambda evt: self.changeColor(evt, self.darkGrey, 1))
        self.helpNavButton.Bind(wx.EVT_LEFT_DOWN, lambda evt: self.changeColor(evt, self.slightlyLightGrey, 0))
        self.helpNavButton.Bind(wx.EVT_LEFT_UP, lambda evt: self.changeColor(evt, self.Grey, 1))
        # self.helpNavButton.SetFont(self.fontBold)
        self.helpNavButton.SetMinSize(wx.Size(200, 50))
        # self.helpNavButton.SetPressColor(self.darkGrey)

        # add all nav bar buttons
        LayoutnavPanelUpper.Add(self.dashboardNavButton, wx.GBPosition(0, 0), wx.GBSpan(1, 1), wx.ALL, 10)
        LayoutnavPanelUpper.Add(self.cameraConfigNavButton, wx.GBPosition(1, 0), wx.GBSpan(1, 1), wx.ALL, 10)
        LayoutnavPanelUpper.Add(self.calibrationNavButton, wx.GBPosition(2, 0), wx.GBSpan(1, 1), wx.ALL, 10)
        LayoutnavPanelUpper.Add(self.helpNavButton, wx.GBPosition(3, 0), wx.GBSpan(1, 1), wx.ALL, 10)

        # Make lower nav panel
        LayoutnavPanelLower = wx.GridBagSizer(0, 0)
        LayoutnavPanelLower.SetFlexibleDirection(wx.BOTH)
        LayoutnavPanelLower.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        # Add User button on Navbar
        self.userNavButton = wx.Button(self.navPanel, -1, u"  User", wx.DefaultPosition, wx.DefaultSize,
                                       wx.BORDER_NONE | wx.BU_LEFT)
        self.userNavButton.SetForegroundColour(self.white)
        self.userNavButton.SetBackgroundColour(self.darkGrey)
        self.userNavButton.SetBitmap(self.UserIcon)
        self.userNavButton.Bind(wx.EVT_ENTER_WINDOW, lambda evt: self.changeColor(evt, self.Grey, 0))
        self.userNavButton.Bind(wx.EVT_LEAVE_WINDOW, lambda evt: self.changeColor(evt, self.darkGrey, 1))
        self.userNavButton.Bind(wx.EVT_LEFT_DOWN, lambda evt: self.changeColor(evt, self.slightlyLightGrey, 0))
        self.userNavButton.Bind(wx.EVT_LEFT_UP, lambda evt: self.changeColor(evt, self.Grey, 1))
        # self.userNavButton.SetFont(self.fontBold)
        self.userNavButton.SetMinSize(wx.Size(200, 50))
        # self.userNavButton.SetPressColor(self.darkGrey)

        # add user button
        LayoutnavPanelLower.Add(self.userNavButton, wx.GBPosition(0, 0), wx.GBSpan(1, 1), wx.ALL, 10)

        # add upper and lower nav panel
        LayoutnavPanel.Add(LayoutnavPanelUpper, 1, wx.EXPAND, 0)
        LayoutnavPanel.Add(LayoutnavPanelLower, 0, wx.EXPAND, 0)

        self.navPanel.SetSizer(LayoutnavPanel)
        self.navPanel.Layout()
        LayoutnavPanel.Fit(self.navPanel)

        self.mainContainer = wx.Panel(self, pos=wx.DefaultPosition, size=wx.DefaultSize)
        #self.mainContainer.SetScrollRate(5, 5)

        LayoutMain.Add(self.navPanel, proportion=0, flag=wx.EXPAND | wx.ALL, border=0)
        LayoutMain.Add(self.mainContainer, proportion=1, flag=wx.EXPAND | wx.ALL, border=0)

        self.SetSizer(LayoutMain)
        self.Layout()

        self.dashboardPage = Dashboard.Dashboard(self.mainContainer)
        self.configPage = Configuration.MyFrame1(self.mainContainer)
        self.calibPage = Calibration.Calibration(self.mainContainer)

        LayoutMainContainer = wx.BoxSizer(wx.VERTICAL)

        LayoutMainContainer.Add(self.dashboardPage, proportion=1, flag=wx.EXPAND | wx.ALL, border=0)
        LayoutMainContainer.Add(self.configPage, proportion=1, flag=wx.EXPAND | wx.ALL, border=0)
        LayoutMainContainer.Add(self.calibPage, proportion=1, flag=wx.EXPAND | wx.ALL, border=0)

        self.dashboardPage.Hide()
        self.configPage.Hide()
        self.calibPage.Hide()

        self.changePage(None, 1)
        self.updateNavColors(1)

        self.mainContainer.SetSizer(LayoutMainContainer)
        #LayoutMainContainer.Fit(self.mainContainer)
        self.mainContainer.Layout()

        self.Layout()

        self.Show(True)

    def changePage(self, event, pageno):
        self.current_page = pageno
        self.dashboardPage.isPlaying = False
        self.dashboardPage.galleryPauseButton.SetBitmap(wx.Bitmap("ui_elements/play.png"))
        if(self.current_page == 1):
            self.dashboardPage.Show(True)
            self.configPage.Hide()
            self.calibPage.Hide()
        elif (self.current_page == 2):
            self.configPage.Show(True)
            self.dashboardPage.Hide()
            self.calibPage.Hide()
        elif (self.current_page == 3):
            self.calibPage.Show(True)
            self.configPage.Hide()
            self.dashboardPage.Hide()
        self.Layout()
        return event

    def updateNavColors(self, pageChange):
        if(pageChange):
            if(self.current_page == 1):
                self.dashboardNavButton.SetBackgroundColour(self.Grey)
                self.cameraConfigNavButton.SetBackgroundColour(self.darkGrey)
                self.calibrationNavButton.SetBackgroundColour(self.darkGrey)
                self.helpNavButton.SetBackgroundColour(self.darkGrey)
                self.userNavButton.SetBackgroundColour(self.darkGrey)
            elif (self.current_page == 2):
                self.dashboardNavButton.SetBackgroundColour(self.darkGrey)
                self.cameraConfigNavButton.SetBackgroundColour(self.Grey)
                self.calibrationNavButton.SetBackgroundColour(self.darkGrey)
                self.helpNavButton.SetBackgroundColour(self.darkGrey)
                self.userNavButton.SetBackgroundColour(self.darkGrey)
            elif (self.current_page == 3):
                self.dashboardNavButton.SetBackgroundColour(self.darkGrey)
                self.cameraConfigNavButton.SetBackgroundColour(self.darkGrey)
                self.calibrationNavButton.SetBackgroundColour(self.Grey)
                self.helpNavButton.SetBackgroundColour(self.darkGrey)
                self.userNavButton.SetBackgroundColour(self.darkGrey)


    def scaleIcons(self, iconBitmap, iconSize):
        image = wx.Bitmap.ConvertToImage(iconBitmap)
        image = image.Scale(iconSize[0], iconSize[1], wx.IMAGE_QUALITY_HIGH)
        return wx.Bitmap(image)

    def changeColor(self, event, newcolor, pageChange):
        event.GetEventObject().SetBackgroundColour(newcolor)
        wx.CallAfter(self.updateNavColors, pageChange)

    def dashboardNavButtonClicked(self, event):
        self.parent.current_page = 1
        self.parent.changePage()
        return event

    def cameraConfigNavButtonClicked(self, event):
        self.parent.current_page = 2
        self.parent.changePage()
        return event

    def calibrationNavButtonClicked(self, event):
        self.parent.current_page = 3
        self.parent.changePage()
        return event


app = wx.App()
window = MainFrame()
app.MainLoop()