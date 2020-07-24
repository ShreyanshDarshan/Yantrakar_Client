import wx
import Dashboard
import Calibration
import Configuration

class MainFrame(wx.Frame):

    def __init__(self):
        super(MainFrame, self).__init__(None, title="Yantrakar", size=(1100, 750))
        self.SetMinSize((1100, 750))

        self.current_page = 2

        self.initUI()

    def changePage(self):
        timeout = 1000
        if(self.current_page == 1):
            self.dashboardPage.Show()
            self.configPage.Hide()
            self.calibPage.Hide()
        elif(self.current_page == 2):
            self.configPage.Show()
            self.calibPage.Hide()
            self.dashboardPage.Hide()
        elif(self.current_page == 3):
            self.calibPage.Show()
            self.configPage.Hide()
            self.dashboardPage.Hide()

        self.Layout()

    def initUI(self):
        self.dashboardPage = Dashboard.Dashboard(self)
        self.configPage = Configuration.MyFrame1(self)
        self.calibPage = Calibration.Calibration(self)

        self.LayoutMain = wx.BoxSizer(wx.VERTICAL)

        self.LayoutMain.Add(self.dashboardPage, proportion=1, flag=wx.EXPAND | wx.ALL, border=0)
        self.LayoutMain.Add(self.configPage, proportion=1, flag=wx.EXPAND | wx.ALL, border=0)
        self.LayoutMain.Add(self.calibPage, proportion=1, flag=wx.EXPAND | wx.ALL, border=0)


        #self.dashboardPage.Hide()
        self.configPage.Hide()
        self.calibPage.Hide()

        self.SetSizer(self.LayoutMain)
        self.LayoutMain.Fit(self)

        self.Show(True)
        self.Layout()

app = wx.App()
window = MainFrame()
app.MainLoop()