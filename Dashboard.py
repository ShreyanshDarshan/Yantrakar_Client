import wx
import wx.lib.platebtn as plateButtons

class DashboardGallerySlide(wx.Panel):

    def __init__(self, parent, size, image, time, cameraID, cameraAlias):
        self.size = size
        self.image = image
        self.time = time
        self.cameraID = cameraID
        self.cameraAlias = cameraAlias
        #print("SLIDER SIZE")
        #print(size)
        super(DashboardGallerySlide, self).__init__(parent, -1, size=(self.size[0], -1), pos=wx.DefaultPosition)

        self.SetMinSize(self.size)

        self.initSlide()

    def initSlide(self):

        LayoutSlide = wx.BoxSizer(wx.HORIZONTAL)

        self.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))

        self.slideImagePanel = wx.Panel(self, -1)
        self.slideImagePanel.SetBackgroundColour(wx.Colour(24, 29, 184))
        self.slideDetailsPanel = wx.Panel(self, -1)
        self.slideDetailsPanel.SetBackgroundColour(wx.Colour(0, 144, 212))

        slideDetailsLayout = wx.BoxSizer(wx.VERTICAL)

        slideDetailsLayoutMain = wx.GridBagSizer(0, 0)

        self.cameraAliasLabel = wx.StaticText(self.slideDetailsPanel, -1, "Camera Alias")
        self.cameraAliasLabel.SetForegroundColour(wx.Colour(255, 255, 255))
        self.cameraAliasValue = wx.StaticText(self.slideDetailsPanel, -1, self.cameraAlias)
        self.cameraAliasValue.SetForegroundColour(wx.Colour(255, 255, 255))
        self.cameraIDLabel = wx.StaticText(self.slideDetailsPanel, -1, "Camera ID")
        self.cameraIDLabel.SetForegroundColour(wx.Colour(255, 255, 255))
        self.cameraIDValue = wx.StaticText(self.slideDetailsPanel, -1, self.cameraID)
        self.cameraIDValue.SetForegroundColour(wx.Colour(255, 255, 255))
        self.timeLabel = wx.StaticText(self.slideDetailsPanel, -1, "Time")
        self.timeLabel.SetForegroundColour(wx.Colour(255, 255, 255))
        self.timeValue = wx.StaticText(self.slideDetailsPanel, -1, self.time)
        self.timeValue.SetForegroundColour(wx.Colour(255, 255, 255))

        slideDetailsLayoutMain.Add(self.cameraAliasLabel, wx.GBPosition(0, 0), wx.GBSpan(1, 1), wx.ALL, 5)
        slideDetailsLayoutMain.Add(self.cameraAliasValue, wx.GBPosition(0, 1), wx.GBSpan(1, 1), wx.ALL, 5)
        slideDetailsLayoutMain.Add(self.cameraIDLabel, wx.GBPosition(1, 0), wx.GBSpan(1, 1), wx.ALL, 5)
        slideDetailsLayoutMain.Add(self.cameraIDValue, wx.GBPosition(1, 1), wx.GBSpan(1, 1), wx.ALL, 5)
        slideDetailsLayoutMain.Add(self.timeLabel, wx.GBPosition(2, 0), wx.GBSpan(1, 1), wx.ALL, 5)
        slideDetailsLayoutMain.Add(self.timeValue, wx.GBPosition(2, 1), wx.GBSpan(1, 1), wx.ALL, 5)

        slideDetailsLayout.Add(slideDetailsLayoutMain, proportion=0, flag=wx.EXPAND | wx.ALL, border=10)
        slideDetailsLayout.Add((0, 0), proportion=1, flag=wx.EXPAND | wx.ALL, border=10)

        self.slideDetailsPanel.SetSizer(slideDetailsLayout)
        slideDetailsLayout.Fit(self.slideDetailsPanel)

        LayoutSlide.Add(self.slideImagePanel, proportion=1, flag=wx.EXPAND | wx.ALL, border=0)
        LayoutSlide.Add(self.slideDetailsPanel, proportion=0, flag=wx.EXPAND | wx.ALL, border=0)

        self.SetSizer(LayoutSlide)
        LayoutSlide.Fit(self)
        self.Layout()

        self.imageBitmap = wx.Bitmap(self.image, wx.BITMAP_TYPE_ANY)

        wx.CallAfter(self.addImage)

    def addImage(self):
        self.scaleImage()
        self.imageBitmapView = wx.StaticBitmap(self.slideImagePanel, -1, self.imageBitmap)

    def scaleImage(self):
        image = wx.Bitmap.ConvertToImage(self.imageBitmap)
        #print(self.slideImagePanel.GetSize())
        #print(self.slideDetailsPanel.GetSize())
        image = image.Scale(self.slideImagePanel.GetSize()[0], self.slideImagePanel.GetSize()[1], wx.IMAGE_QUALITY_HIGH)
        self.imageBitmap = wx.Bitmap(image)


class Dashboard(wx.Frame):

    def __init__(self, parent):
        super(Dashboard, self).__init__(parent, title="Yantrakar Dashboard", size=(1100, 750))

        self.noOfSlides = 3
        self.slideShowOn = 0
        self.slideSpeed = 10

        self.SetMinSize((1100, 750))
        self.initUI()

    def initUI(self):
        self.fontNormal = wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        self.fontBold = wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        self.darkOrange = wx.Colour(24, 29, 184)
        self.lightOrange = wx.Colour(0, 144, 212)

        self.SetFont(self.fontNormal)
        self.SetBackgroundColour(wx.Colour(wx.WHITE))

        LayoutMain = wx.BoxSizer(wx.HORIZONTAL)

        self.navPanel = wx.Panel(self, pos=wx.DefaultPosition)
        self.navPanel.SetBackgroundColour(self.darkOrange)

        LayoutnavPanel = wx.BoxSizer(wx.VERTICAL)

        LayoutnavPanelUpper = wx.GridBagSizer(0, 0)
        LayoutnavPanelUpper.SetFlexibleDirection(wx.BOTH)
        LayoutnavPanelUpper.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.dashboardNavButton = plateButtons.PlateButton(self.navPanel, -1, u"Dashboard", None, wx.DefaultPosition, wx.DefaultSize, plateButtons.PB_STYLE_SQUARE)
        self.dashboardNavButton.SetForegroundColour(wx.Colour(255, 255, 255))
        self.dashboardNavButton.SetBackgroundColour(self.lightOrange)
        self.dashboardNavButton.SetFont(self.fontBold)
        self.dashboardNavButton.SetMinSize(wx.Size(200, 50))

        self.cameraConfigNavButton = plateButtons.PlateButton(self.navPanel, -1, u"Camera Config", None, wx.DefaultPosition, wx.DefaultSize, plateButtons.PB_STYLE_SQUARE)
        self.cameraConfigNavButton.SetForegroundColour(wx.Colour(255, 255, 255))
        self.cameraConfigNavButton.SetBackgroundColour(self.darkOrange)
        self.cameraConfigNavButton.SetFont(self.fontBold)
        self.cameraConfigNavButton.SetMinSize(wx.Size(200, 50))

        self.calibrationNavButton = plateButtons.PlateButton(self.navPanel, -1, u"Calibration", None, wx.DefaultPosition, wx.DefaultSize, plateButtons.PB_STYLE_SQUARE)
        self.calibrationNavButton.SetForegroundColour(wx.Colour(255, 255, 255))
        self.calibrationNavButton.SetBackgroundColour(self.darkOrange)
        self.calibrationNavButton.SetFont(self.fontBold)
        self.calibrationNavButton.SetMinSize(wx.Size(200, 50))

        self.helpNavButton = plateButtons.PlateButton(self.navPanel, -1, u"Help", None, wx.DefaultPosition, wx.DefaultSize, plateButtons.PB_STYLE_SQUARE)
        self.helpNavButton.SetForegroundColour(wx.Colour(255, 255, 255))
        self.helpNavButton.SetBackgroundColour(self.darkOrange)
        self.helpNavButton.SetFont(self.fontBold)
        self.helpNavButton.SetMinSize(wx.Size(200, 50))

        LayoutnavPanelUpper.Add(self.dashboardNavButton, wx.GBPosition(0, 0), wx.GBSpan(1, 1), wx.ALL, 10)
        LayoutnavPanelUpper.Add(self.cameraConfigNavButton, wx.GBPosition(1, 0), wx.GBSpan(1, 1), wx.ALL, 10)
        LayoutnavPanelUpper.Add(self.calibrationNavButton, wx.GBPosition(2, 0), wx.GBSpan(1, 1), wx.ALL, 10)
        LayoutnavPanelUpper.Add(self.helpNavButton, wx.GBPosition(3, 0), wx.GBSpan(1, 1), wx.ALL, 10)

        LayoutnavPanelLower = wx.GridBagSizer(0, 0)
        LayoutnavPanelLower.SetFlexibleDirection(wx.BOTH)
        LayoutnavPanelLower.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.userNavButton = plateButtons.PlateButton(self.navPanel, -1, u"User", None, wx.DefaultPosition, wx.DefaultSize, plateButtons.PB_STYLE_SQUARE)
        self.userNavButton.SetForegroundColour(wx.Colour(255, 255, 255))
        self.userNavButton.SetBackgroundColour(self.darkOrange)
        self.userNavButton.SetFont(self.fontBold)
        self.userNavButton.SetMinSize(wx.Size(200, 50))

        LayoutnavPanelLower.Add(self.userNavButton, wx.GBPosition(0, 0), wx.GBSpan(1, 1), wx.ALL, 10)

        LayoutnavPanel.Add(LayoutnavPanelUpper, 1, wx.EXPAND, 0)
        LayoutnavPanel.Add(LayoutnavPanelLower, 0, wx.EXPAND, 0)

        self.navPanel.SetSizer(LayoutnavPanel)
        self.navPanel.Layout()
        LayoutnavPanel.Fit(self.navPanel)


        self.dashboardPanel = wx.ScrolledWindow(self, pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.VSCROLL | wx.HSCROLL)
        self.dashboardPanel.SetScrollRate(5, 5)

        LayoutDashboard = wx.BoxSizer(wx.VERTICAL)

        LayoutDashboardControls = wx.BoxSizer(wx.HORIZONTAL)

        cameraIDLabel = wx.StaticText(self.dashboardPanel, -1, "Camera ID")
        self.cameraIDEntry = wx.ComboBox(self.dashboardPanel, -1)
        self.cameraIDEntry.Append("All Cameras")
        self.cameraIDEntry.SetSelection(0)
        durationLabel = wx.StaticText(self.dashboardPanel, -1, "Duration")
        self.durationEntry = wx.ComboBox(self.dashboardPanel, -1)
        self.durationEntry.Append("All Days")
        self.durationEntry.SetSelection(0)
        self.viewButton = wx.Button(self.dashboardPanel, -1, "View")
        self.viewButton.SetBackgroundColour(self.lightOrange)
        self.viewButton.SetForegroundColour(wx.Colour(255, 255, 255))
        self.viewButton.SetFont(self.fontBold)

        LayoutDashboardControls.Add(wx.Size(0, 0), 1, wx.EXPAND, 0)
        LayoutDashboardControls.Add(cameraIDLabel, 2, wx.ALL, 0)
        LayoutDashboardControls.Add(self.cameraIDEntry, 2, wx.ALL, 0)
        LayoutDashboardControls.Add(wx.Size(0, 0), 1, wx.EXPAND, 0)
        LayoutDashboardControls.Add(durationLabel, 2, wx.ALL, 0)
        LayoutDashboardControls.Add(self.durationEntry, 2, wx.ALL, 0)
        LayoutDashboardControls.Add(wx.Size(0, 0), 1, wx.EXPAND, 0)
        LayoutDashboardControls.Add(self.viewButton, 2, wx.ALL, 0)
        LayoutDashboardControls.Add(wx.Size(0, 0), 1, wx.EXPAND, 0)


        DashboardGalleryPanel = wx.Panel(self.dashboardPanel, pos=wx.DefaultPosition)
        DashboardGalleryPanel.SetBackgroundColour(self.lightOrange)
        DashboardGalleryPanel.SetMinSize((-1, 500))

        LayoutDashboardGallery = wx.BoxSizer(wx.VERTICAL)

        self.dashboardGalleryView = wx.ScrolledWindow(DashboardGalleryPanel, pos=wx.DefaultPosition, style=wx.HSCROLL)
        self.dashboardGalleryView.SetScrollRate(self.slideSpeed, self.slideSpeed)
        self.dashboardGalleryView.SetBackgroundColour(self.lightOrange)

        dashboardGalleryControls = wx.Panel(DashboardGalleryPanel, -1, pos=wx.DefaultPosition, size=wx.DefaultSize)
        LayoutDashboardGalleryControls = wx.BoxSizer(wx.HORIZONTAL)

        self.galleryPlayButton = plateButtons.PlateButton(dashboardGalleryControls, -1, u"Play", None, wx.DefaultPosition, wx.DefaultSize, plateButtons.PB_STYLE_DEFAULT)
        self.galleryPlayButton.SetMaxSize((80, -1))
        self.galleryPlayButton.SetBackgroundColour(self.lightOrange)
        self.galleryPlayButton.SetFont(self.fontBold)
        self.galleryPlayButton.SetForegroundColour(wx.Colour(255, 255, 255))
        self.galleryPlayButton.Bind(wx.EVT_BUTTON, self.galleryPlayButtonClicked)

        self.galleryPauseButton = plateButtons.PlateButton(dashboardGalleryControls, -1, u"Pause", None, wx.DefaultPosition, wx.DefaultSize, plateButtons.PB_STYLE_DEFAULT)
        self.galleryPauseButton.SetMaxSize((80, -1))
        self.galleryPauseButton.SetBackgroundColour(self.lightOrange)
        self.galleryPauseButton.SetFont(self.fontBold)
        self.galleryPauseButton.SetForegroundColour(wx.Colour(255, 255, 255))
        self.galleryPauseButton.Bind(wx.EVT_BUTTON, self.galleryPauseButtonClicked)

        #if(not self.noOfSlides == 0):
        #    self.gallerySlider = wx.Slider(dashboardGalleryControls, -1, 0, 0, self.noOfSlides - 1)
        #else:
            #self.gallerySlider = wx.Slider(dashboardGalleryControls, -1, 0, 0, 1)
            #self.gallerySlider.Enable(False)
        self.gallerySlider = wx.Slider(dashboardGalleryControls, -1, 0, 0, 1)
        self.gallerySlider.Enable(False)
        self.gallerySlider.SetBackgroundColour(self.lightOrange)

        #if(self.gallerySlider.IsEnabled()):
        #    if(self.slideShowOn):
        #        self.gallerySlider.Enable(False)

        LayoutDashboardGalleryControls.Add(self.galleryPlayButton, proportion=1, flag=wx.EXPAND | wx.ALL, border=0)
        LayoutDashboardGalleryControls.Add(self.galleryPauseButton, proportion=1, flag=wx.EXPAND | wx.ALL, border=0)
        LayoutDashboardGalleryControls.Add(self.gallerySlider, proportion=8, flag=wx.EXPAND | wx.ALL, border=0)

        dashboardGalleryControls.SetSizer(LayoutDashboardGalleryControls)
        LayoutDashboardGalleryControls.Fit(dashboardGalleryControls)

        LayoutDashboardGallery.Add(self.dashboardGalleryView, proportion=1, flag=wx.EXPAND | wx.ALL, border=0)
        LayoutDashboardGallery.Add(dashboardGalleryControls, proportion=0, flag=wx.EXPAND | wx.ALL, border=0)

        DashboardGalleryPanel.SetSizer(LayoutDashboardGallery)
        LayoutDashboardGallery.Fit(DashboardGalleryPanel)


        DashboardGraphPanel = wx.Panel(self.dashboardPanel, pos=wx.DefaultPosition)
        DashboardGraphPanel.SetBackgroundColour(self.lightOrange)
        DashboardGraphPanel.SetMinSize((-1, 500))

        LayoutDashboard.Add(LayoutDashboardControls, proportion=0, flag=wx.EXPAND | wx.ALL, border=30)
        LayoutDashboard.Add(DashboardGalleryPanel, proportion=1, flag=wx.EXPAND | wx.ALL, border=30)
        LayoutDashboard.Add(DashboardGraphPanel, proportion=1, flag=wx.EXPAND | wx.ALL, border=30)

        self.dashboardPanel.SetSizer(LayoutDashboard)
        self.dashboardPanel.Layout()
        LayoutDashboard.Fit(self.dashboardPanel)

        LayoutMain.Add(self.navPanel, proportion=0, flag=wx.EXPAND | wx.ALL, border=0)
        LayoutMain.Add(self.dashboardPanel, proportion=1, flag=wx.EXPAND | wx.ALL, border=0)

        self.LayoutDashboardGalleryView = wx.GridBagSizer(0, 0)

        self.SlidesList = []

        slide1 = DashboardGallerySlide(self.dashboardGalleryView, self.dashboardGalleryView.GetSize(), "./test.png", "10:00 AM", "camera#1", "CAM1")
        slide2 = DashboardGallerySlide(self.dashboardGalleryView, self.dashboardGalleryView.GetSize(), "./test.png", "1:00 PM", "camera#2", "CAM2")
        slide3 = DashboardGallerySlide(self.dashboardGalleryView, self.dashboardGalleryView.GetSize(), "./test.png", "1:00 PM",
                                       "camera#3", "CAM3")

        self.SlidesList.append(slide1)
        self.SlidesList.append(slide2)
        self.SlidesList.append(slide3)

        self.LayoutDashboardGalleryView.Add(slide1, wx.GBPosition(0, 0), wx.GBSpan(1, 1), wx.ALL, 0)
        self.LayoutDashboardGalleryView.Add(slide2, wx.GBPosition(0, 1), wx.GBSpan(1, 1), wx.ALL, 0)
        self.LayoutDashboardGalleryView.Add(slide3, wx.GBPosition(0, 2), wx.GBSpan(1, 1), wx.ALL, 0)

        self.dashboardGalleryView.SetSizer(self.LayoutDashboardGalleryView)
        self.LayoutDashboardGalleryView.Fit(self.dashboardGalleryView)
        self.dashboardGalleryView.Layout()

        self.dashboardGalleryView.ShowScrollbars(wx.SHOW_SB_NEVER, wx.SHOW_SB_NEVER)

        self.SetSizer(LayoutMain)
        self.Layout()

        self.Center()
        self.Show(True)

        self.updateGalleryPanel()

        #self.gallerySlider.SetRange(0, int((self.dashboardGalleryView.GetSize()[0]) * (self.noOfSlides - 1)/ self.slideSpeed))
        self.gallerySlider.Bind(wx.EVT_SLIDER, self.onGallerySlider)

        self.timer = wx.Timer(self)
        self.timer.Start(1)
        self.slideshowDirection = 1

        self.waitTimer = wx.Timer(self)

        self.Bind(wx.EVT_TIMER, self.playSlideShow, self.timer)
        self.Bind(wx.EVT_TIMER, self.pauseSlideShow, self.waitTimer)

        self.Bind(wx.EVT_SIZE, self.mainWindowSizeChange)
        #self.Bind(wx.EVT_MAXIMIZE, self.mainWindowSizeChange2)
        #self.Bind(wx.wxEVT_MAXIMIZE, self.mainWindowSizeChange2)

    def galleryPlayButtonClicked(self, event):
        print("Here")
        self.slideShowOn = 1
        self.galleryPlayButton.Enable(False)
        self.galleryPauseButton.Enable(True)

    def galleryPauseButtonClicked(self, event):
        self.slideShowOn = 0
        self.galleryPlayButton.Enable(True)
        self.galleryPauseButton.Enable(False)

    def updateGalleryPanel(self):
        if(self.noOfSlides > 1):
            self.gallerySlider.Enable(True)
            self.gallerySlider.SetRange(0, int((self.dashboardGalleryView.GetSize()[0]) * (self.noOfSlides - 1)/ self.slideSpeed))
        else:
            self.gallerySlider.SetRange(0, 1)
            self.gallerySlider.Enable(False)

        if (self.slideShowOn):
            self.galleryPlayButton.Enable(False)
            self.galleryPauseButton.Enable(True)
        else:
            self.galleryPlayButton.Enable(True)
            self.galleryPauseButton.Enable(False)

        if(self.noOfSlides <= 1):
            self.galleryPlayButton.Enable(False)
            self.galleryPauseButton.Enable(False)
            self.slideShowOn = 0


    def pauseSlideShow(self, event):
        if(self.slideShowOn):
            self.waitTimer.Stop()
            self.timer.Start(1)

    def playSlideShow(self, event):
        if(self.slideShowOn):
            if (self.gallerySlider.GetValue() % int(self.gallerySlider.GetRange()[1] / (self.noOfSlides - 1)) == 0):
                self.waitTimer.Start(1000)
                self.timer.Stop()

            if(self.slideshowDirection == 1):
                self.gallerySlider.SetValue(self.gallerySlider.GetValue() + 1)
            else:
                self.gallerySlider.SetValue(self.gallerySlider.GetValue() - 1)

            self.onGallerySlider(event)

    def onGallerySlider(self, event):
        #obj = event.GetEventObject()
        val = self.gallerySlider.GetValue()

        if(val >= self.gallerySlider.GetRange()[1]):
            self.slideshowDirection = -1
        elif(val == 0):
            self.slideshowDirection = 1

        #print(self.dashboardGalleryView.GetSize())
        #self.dashboardGalleryView.Scroll(int(val * self.dashboardGalleryView.GetSize()[0] - 20), -1)
        self.dashboardGalleryView.Scroll(int(val), -1)
        #self.dashboardGalleryView.Refresh()

    def mainWindowSizeChangeUpdate(self, event):
        for i in self.SlidesList:
            i.size = self.dashboardGalleryView.GetSize()
            #print(i.size)
            i.SetSize((self.dashboardGalleryView.GetSize()[0], -1))
            i.SetMinSize(self.dashboardGalleryView.GetSize())
            i.addImage()
            #print(i.GetMinSize())

        self.dashboardGalleryView.Refresh()
        self.gallerySlider.SetRange(0, int((self.dashboardGalleryView.GetSize()[0]) * (self.noOfSlides - 1) / self.slideSpeed))
        wx.CallAfter(self.Layout)

    def mainWindowSizeChange(self, event):
        self.Layout()
        wx.CallAfter(self.mainWindowSizeChangeUpdate, event)

app = wx.App()
window = Dashboard(None)
app.MainLoop()


'''
import wx
import wx.lib.scrolledpanel

class MainFrame(wx.Frame):

    def __init__(self, parent, title, size):
        self.size = size
        super(MainFrame, self).__init__(parent, title=title, size=size)
        self.initUI();

    def initUI(self):

        self.SetFont(wx.Font(15, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        self.panel = wx.Panel(self, pos=(0, 0), size=self.size)
        cameraIDLabel = wx.StaticText(self.panel, label="Camera ID", pos=(50, 40), size=(100, 40))
        self.cameraIDEntry = wx.ComboBox(self.panel, pos=(180, 35), size=(200, 40))
        self.viewButton = wx.Button(self.panel, pos=(420, 30), size=(100, 40), label="View")
        self.viewButton.SetBackgroundColour(wx.Colour(wx.WHITE))

        self.detailsPanel = wx.lib.scrolledpanel.ScrolledPanel(parent=self, pos=(50, 120), size=(self.size[0] - 100, self.size[1] - 180))
        self.detailsPanel.SetBackgroundColour(wx.Colour(227, 204, 205))

        self.SetBackgroundColour(wx.Colour(wx.WHITE))
        self.Center()
        self.Show(True)

app = wx.App()
window = MainFrame(None, "Yantrakar Dashboard", (750, 750))
app.MainLoop()
'''