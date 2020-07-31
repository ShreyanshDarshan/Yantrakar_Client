import wx
import wx.lib.platebtn as plateButtons
from cryptography.fernet import Fernet
import ast

class Login(wx.Panel):

    def __init__(self, parent, mainParent):
        #super(Login, self).__init__(parent, title="Yantrakar Logim", size=(1100, 750))
        super(Login, self).__init__(parent, size=(1100, 750))

        self.parent = mainParent

        self.encryptionKey = b'gkmrxai04WhOcWj3EGl-2Io58Q8biOWOytdQbPhNYGU='

        self.SetMinSize((1100, 750))
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

        LayoutMain = wx.BoxSizer(wx.VERTICAL)

        self.loginPanel = wx.Panel(self, -1)
        self.loginPanel.SetBackgroundColour(self.darkGrey)

        LayoutLoginPanel = wx.BoxSizer(wx.VERTICAL)

        self.loginHeadPanel = wx.Panel(self.loginPanel, -1)
        self.loginHeadPanel.SetBackgroundColour(self.white)

        LayoutHeadPanel = wx.BoxSizer(wx.VERTICAL)

        self.loginPanelHeading = wx.StaticText(self.loginHeadPanel, -1, "LOGIN")
        self.loginPanelHeading.SetForegroundColour(self.darkGrey)
        self.loginPanelHeading.SetFont(self.fontBold)

        LayoutHeadPanel.Add(self.loginPanelHeading, proportion=1, flag=wx.ALIGN_CENTER | wx.ALL, border=15)

        self.loginHeadPanel.SetSizer(LayoutHeadPanel)
        LayoutHeadPanel.Fit(self.loginHeadPanel)

        LayoutLoginFields = wx.BoxSizer(wx.HORIZONTAL)

        self.passwordLabel = wx.StaticText(self.loginPanel, -1, "Password")
        self.passwordLabel.SetForegroundColour(self.white)
        self.passwordEntry = wx.TextCtrl(self.loginPanel, -1, style=wx.TE_PASSWORD)

        LayoutLoginFields.Add(self.passwordLabel, proportion=0, flag=wx.EXPAND | wx.ALL, border=15)
        LayoutLoginFields.Add(self.passwordEntry, proportion=0, flag=wx.EXPAND | wx.ALL, border=15)

        LayoutLoginButtons = wx.BoxSizer(wx.HORIZONTAL)

        self.loginButton = wx.Button(self.loginPanel, -1, "Login")
        self.loginButton.SetForegroundColour(self.darkGrey)
        self.loginButton.SetBackgroundColour(self.white)
        self.loginButton.Bind(wx.EVT_BUTTON, self.loginButtonClicked)

        LayoutLoginButtons.Add((0, 0), proportion=1, flag=wx.ALIGN_CENTER | wx.ALL, border=0)
        LayoutLoginButtons.Add(self.loginButton, proportion=1, flag=wx.ALIGN_CENTER | wx.ALL, border=0)
        LayoutLoginButtons.Add((0, 0), proportion=1, flag=wx.ALIGN_CENTER | wx.ALL, border=0)

        LayoutLoginPanel.Add(self.loginHeadPanel, proportion=0, flag=wx.EXPAND | wx.ALL, border=0)
        LayoutLoginPanel.Add((0, 0), proportion=0, flag=wx.EXPAND | wx.ALL, border=10)
        LayoutLoginPanel.Add(LayoutLoginFields, proportion=1, flag=wx.EXPAND | wx.ALL, border=0)
        LayoutLoginPanel.Add(LayoutLoginButtons, proportion=1, flag=wx.EXPAND | wx.ALL, border=0)

        self.loginPanel.SetSizer(LayoutLoginPanel)
        LayoutLoginPanel.Fit(self.loginPanel)

        LayoutMain.Add((0, 0), proportion=1, flag=wx.EXPAND, border=0)
        LayoutMain.Add(self.loginPanel, proportion=0, flag=wx.CENTER | wx.ALL, border=20)
        LayoutMain.Add((0, 0), proportion=1, flag=wx.EXPAND, border=0)

        self.SetSizer(LayoutMain)
        LayoutMain.Fit(self)

        self.Layout()
        #self.Show(True)

    def loginButtonClicked(self, event):
        password = self.passwordEntry.GetValue()
        with open('userSetting.txt','r') as file:
            data=file.read()
        cipher=Fernet(self.encryptionKey)
        userSetting=ast.literal_eval((cipher.decrypt(data.encode('utf-8'))).decode('utf-8'))
        if (userSetting["adminPass"] == password):
            print("ADMIN MODE")
            self.parent.onLogin(1)
        elif(userSetting["viewerPass"] == password):
            print("GUEST MODE")
            self.parent.onLogin(2)
        else:
            print("WRONG PASSWORD")
        pass


#app = wx.App()
#window = Login(None)
#app.MainLoop()