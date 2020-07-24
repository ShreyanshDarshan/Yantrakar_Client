import wx
import wx.lib.platebtn as plateButtons
import cv2
import cameraCalib
import json
import numpy as np

class Calibration(wx.Panel):

    def __init__(self, parent):
        #super(Calibration, self).__init__(parent, title="Yantrakar Calibration", size=(1100, 750))
        super(Calibration, self).__init__(parent, size=(1100, 750))

        self.parent = parent

        self.isCalibrating = False
        self.feedPlaying = False
        self.feedFPS = 30
        self.feed = None
        self.feedBitmap = None

        self.calibrater = cameraCalib.CameraCalibration()

        self.instructionStatus = -1

        self.cameraDatabase = None
        self.cameraList = {}

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

        self.capture = cv2.VideoCapture(0)
        ret, self.feed = self.capture.read()

        self.SetFont(self.fontNormal)
        self.SetBackgroundColour(self.Grey)

        LayoutMain = wx.BoxSizer(wx.HORIZONTAL)

        self.calibrationPanel = wx.ScrolledWindow(self, pos=wx.DefaultPosition, size=wx.DefaultSize,
                                                style=wx.VSCROLL | wx.HSCROLL)
        self.calibrationPanel.SetScrollRate(5, 5)

        #LayoutMain.Add(self.navPanel, proportion=0, flag=wx.EXPAND | wx.ALL, border=0)
        LayoutMain.Add(self.calibrationPanel, proportion=1, flag=wx.EXPAND | wx.ALL, border=0)

        self.SetSizer(LayoutMain)
        self.Layout()

        LayoutCalibrationPanel = wx.BoxSizer(wx.VERTICAL)

        self.calibrationPanelHeadPanel = wx.Panel(self.calibrationPanel, -1)
        self.calibrationPanelHeadPanel.SetBackgroundColour(self.darkGrey)

        LayoutHeadPanel = wx.BoxSizer(wx.VERTICAL)

        self.calibrationPanelHeading = wx.StaticText(self.calibrationPanelHeadPanel, -1, "CALIBRATION")
        self.calibrationPanelHeading.SetForegroundColour(self.white)
        self.calibrationPanelHeading.SetFont(self.fontBold)

        LayoutHeadPanel.Add(self.calibrationPanelHeading, proportion=1, flag=wx.ALIGN_CENTER | wx.ALL, border=15)

        self.calibrationPanelHeadPanel.SetSizer(LayoutHeadPanel)
        LayoutHeadPanel.Fit(self.calibrationPanelHeadPanel)

        self.calibrationButtonsPanel = wx.Panel(self.calibrationPanel, -1)
        self.calibrationButtonsPanel.SetBackgroundColour(self.Grey)
        self.calibrationFeedPanel = wx.Panel(self.calibrationPanel, -1)
        self.calibrationFeedPanel.SetBackgroundColour(self.Grey)

        LayoutCalibrationPanel.Add(self.calibrationPanelHeadPanel, proportion=0, flag=wx.EXPAND | wx.ALL, border=0)
        LayoutCalibrationPanel.Add(self.calibrationButtonsPanel, proportion=0, flag=wx.EXPAND | wx.ALL, border=0)
        LayoutCalibrationPanel.Add(self.calibrationFeedPanel, proportion=1, flag=wx.EXPAND | wx.ALL, border=30)

        self.calibrationPanel.SetSizer(LayoutCalibrationPanel)
        LayoutCalibrationPanel.Fit(self.calibrationPanel)

        LayoutButtonPanel = wx.GridBagSizer(0, 0)

        self.howToCalibButton = wx.Button(self.calibrationButtonsPanel, -1, "How to Calibrate?", wx.DefaultPosition, wx.DefaultSize, wx.BORDER_NONE)
        self.howToCalibButton.SetForegroundColour(self.white)
        self.howToCalibButton.SetBackgroundColour(self.darkGrey)
        self.howToCalibButton.Bind(wx.EVT_ENTER_WINDOW,lambda evt:  self.changeColor(evt, self.slightlyLightGrey))
        self.howToCalibButton.Bind(wx.EVT_LEAVE_WINDOW,lambda evt:  self.changeColor(evt, self.darkGrey))
        self.howToCalibButton.Bind(wx.EVT_LEFT_DOWN, lambda evt:  self.changeColor(evt, self.lightGrey))
        self.howToCalibButton.Bind(wx.EVT_LEFT_UP, lambda evt:  self.changeColor(evt, self.slightlyLightGrey))

        cameraAliasLabel = wx.StaticText(self.calibrationButtonsPanel, -1, "Camera Alias")
        cameraAliasLabel.SetForegroundColour(self.faintWhite)
        self.cameraAliasEntry = wx.ComboBox(self.calibrationButtonsPanel, -1, size=(200, -1))
        self.cameraAliasEntry.SetEditable(wx.TE_READONLY)
        self.cameraAliasEntry.Bind(wx.EVT_COMBOBOX, self.cameraAliasEntryChanged)
        self.calibrateStartButton = wx.Button(self.calibrationButtonsPanel, -1, "Start", wx.DefaultPosition, wx.DefaultSize, wx.BORDER_NONE)
        self.calibrateStartButton.SetForegroundColour(self.white)
        self.calibrateStartButton.SetBackgroundColour(self.darkGrey)
        self.calibrateStartButton.Bind(wx.EVT_ENTER_WINDOW,lambda evt:  self.changeColor(evt, self.slightlyLightGrey))
        self.calibrateStartButton.Bind(wx.EVT_LEAVE_WINDOW,lambda evt:  self.changeColor(evt, self.darkGrey))
        self.calibrateStartButton.Bind(wx.EVT_LEFT_DOWN, lambda evt:  self.changeColor(evt, self.lightGrey))
        self.calibrateStartButton.Bind(wx.EVT_LEFT_UP, lambda evt:  self.changeColor(evt, self.slightlyLightGrey))
        
        self.calibrateStartButton.Bind(wx.EVT_BUTTON, self.calibStartButtonClicked)

        self.calibrateSaveButton = wx.Button(self.calibrationButtonsPanel, -1, "Save", wx.DefaultPosition, wx.DefaultSize, wx.BORDER_NONE)
        self.calibrateSaveButton.SetForegroundColour(self.white)
        self.calibrateSaveButton.SetBackgroundColour(self.darkGrey)
        self.calibrateSaveButton.Bind(wx.EVT_ENTER_WINDOW,lambda evt:  self.changeColor(evt, self.slightlyLightGrey))
        self.calibrateSaveButton.Bind(wx.EVT_LEAVE_WINDOW,lambda evt:  self.changeColor(evt, self.darkGrey))
        self.calibrateSaveButton.Bind(wx.EVT_LEFT_DOWN, lambda evt:  self.changeColor(evt, self.lightGrey))
        self.calibrateSaveButton.Bind(wx.EVT_LEFT_UP, lambda evt:  self.changeColor(evt, self.slightlyLightGrey))
        self.calibrateSaveButton.Enable(False)
        self.calibrateSaveButton.Bind(wx.EVT_BUTTON, self.calibrateSaveButtonClicked)

        markerSideLabel = wx.StaticText(self.calibrationButtonsPanel, -1, "Marker Side Dimension (in cm)")
        markerSideLabel.SetForegroundColour(self.faintWhite)
        self.markerSideEntry = wx.TextCtrl(self.calibrationButtonsPanel, -1, "14.0")

        LayoutButtonPanel.Add((0, 0), wx.GBPosition(0, 0), wx.GBSpan(1, 1), wx.EXPAND | wx.ALL, 10)
        LayoutButtonPanel.Add(self.howToCalibButton, wx.GBPosition(0, 1), wx.GBSpan(1, 2), wx.EXPAND | wx.ALL, 15)
        LayoutButtonPanel.Add((0, 0), wx.GBPosition(0, 3), wx.GBSpan(1, 1), wx.EXPAND | wx.ALL, 10)
        LayoutButtonPanel.Add(cameraAliasLabel, wx.GBPosition(0, 4), wx.GBSpan(1, 1), wx.EXPAND | wx.ALL, 15)
        LayoutButtonPanel.Add(self.cameraAliasEntry, wx.GBPosition(0, 5), wx.GBSpan(1, 2), wx.EXPAND | wx.ALL, 15)
        LayoutButtonPanel.Add((80, 0), wx.GBPosition(0, 7), wx.GBSpan(1, 3), wx.EXPAND | wx.ALL, 10)
        LayoutButtonPanel.Add(self.calibrateStartButton, wx.GBPosition(0, 11), wx.GBSpan(1, 1), wx.EXPAND | wx.ALL, 15)
        LayoutButtonPanel.Add(self.calibrateSaveButton, wx.GBPosition(0, 12), wx.GBSpan(1, 1), wx.EXPAND | wx.ALL, 15)
        LayoutButtonPanel.Add((0, 0), wx.GBPosition(0, 13), wx.GBSpan(1, 1), wx.EXPAND | wx.ALL, 10)
        LayoutButtonPanel.Add((0, 0), wx.GBPosition(1, 0), wx.GBSpan(1, 1), wx.EXPAND | wx.ALL, 10)
        LayoutButtonPanel.Add(markerSideLabel, wx.GBPosition(1, 1), wx.GBSpan(1, 3), wx.EXPAND | wx.ALL, 15)
        LayoutButtonPanel.Add(self.markerSideEntry, wx.GBPosition(1, 4), wx.GBSpan(1, 1), wx.EXPAND | wx.ALL, 15)
        LayoutButtonPanel.Add((0, 0), wx.GBPosition(1, 5), wx.GBSpan(1, 9), wx.EXPAND | wx.ALL, 10)

        self.calibrationButtonsPanel.SetSizer(LayoutButtonPanel)
        LayoutButtonPanel.Fit(self.calibrationButtonsPanel)

        LayoutCalibFeedPanel = wx.BoxSizer(wx.HORIZONTAL)

        self.calibFeedPanelLeft = wx.Panel(self.calibrationFeedPanel, -1)
        self.calibFeedPanelLeft.SetBackgroundColour(self.faintWhite)
        self.calibFeedPanelRight = wx.Panel(self.calibrationFeedPanel, -1)
        self.calibFeedPanelRight.SetBackgroundColour(self.darkGrey)
        #self.calibFeedPanelRight.SetMinSize((250, -1))

        LayoutCalibFeedPanel.Add(self.calibFeedPanelLeft, proportion=8, flag=wx.EXPAND | wx.ALL, border=0)
        LayoutCalibFeedPanel.Add(self.calibFeedPanelRight, proportion=5, flag=wx.EXPAND | wx.ALL, border=0)

        self.calibrationFeedPanel.SetSizer(LayoutCalibFeedPanel)
        LayoutCalibFeedPanel.Fit(self.calibrationFeedPanel)

        LayoutFeedLeftPanel = wx.BoxSizer(wx.VERTICAL)

        self.calibrationFeed = wx.Panel(self.calibFeedPanelLeft, -1)

        LayoutFeedLeftPanel.Add(self.calibrationFeed, proportion=1, flag=wx.EXPAND | wx.ALL, border=20)

        self.calibFeedPanelLeft.SetSizer(LayoutFeedLeftPanel)
        LayoutFeedLeftPanel.Fit(self.calibFeedPanelLeft)

        LayoutFeedRightPanel = wx.BoxSizer(wx.VERTICAL)

        self.instructionPanel = wx.Panel(self.calibFeedPanelRight, -1)
        self.instructionPanel.SetBackgroundColour(self.white)

        LayoutFeedRightPanel.Add((0, 0), proportion=1, flag=wx.EXPAND)
        LayoutFeedRightPanel.Add(self.instructionPanel, proportion=0, flag=wx.CENTER | wx.ALL, border=20)
        LayoutFeedRightPanel.Add((0, 0), proportion=1, flag=wx.EXPAND)

        self.calibFeedPanelRight.SetSizer(LayoutFeedRightPanel)
        LayoutFeedRightPanel.Fit(self.calibFeedPanelRight)

        LayoutInstructionPanel = wx.BoxSizer(wx.VERTICAL)

        self.instructionText = wx.StaticText(self.instructionPanel, -1, "", style=wx.ALIGN_CENTER)
        self.instructionText.SetForegroundColour(self.faintWhite)
        self.instructionText.Wrap(280)
        #self.instructionText.SetMinSize((-1, 20))
        self.instructionImage = wx.Panel(self.instructionPanel, -1)
        self.instructionImage.SetMinSize((300, 300))
        self.instructionImage.SetBackgroundColour(wx.BLACK)

        LayoutInstructionPanel.Add(self.instructionText, proportion=0, flag=wx.ALL | wx.CENTER, border=10)
        LayoutInstructionPanel.Add(self.instructionImage, proportion=0, flag=wx.ALL | wx.EXPAND  | wx.SHAPED, border=0)

        self.instructionPanel.SetSizer(LayoutInstructionPanel)
        LayoutInstructionPanel.Fit(self.instructionPanel)

        self.feedTimer = wx.Timer(self)
        self.feedTimer.Start(1000 / self.feedFPS)
        self.Bind(wx.EVT_TIMER, self.updateFeed, self.feedTimer)
        self.calibrationFeed.Bind(wx.EVT_PAINT, self.putFeed)

        self.Center()
        #self.Show(True)
        self.Layout()

        self.updateCameraAliasList()

    def calibrateSaveButtonClicked(self, event):
        cameraID = self.cameraList[self.cameraAliasEntry.GetValue()]
        calibrationData = {
            'calibrationMatrix': self.calibrater.topViewTransform.tolist(),
            'worldRatio': self.calibrater.worldRatio
        }

        self.cameraDatabase[cameraID]['cameraStatus']['calibAvailable'] = True
        self.cameraDatabase[cameraID]['CalibrationData'] = calibrationData

        with open("cameraDatabase.json", 'w') as jsonFile:
            json.dump(self.cameraDatabase,jsonFile,sort_keys=True, indent=4)

        self.calibrateSaveButton.Enable(False)

    def cameraAliasEntryChanged(self, event):
        if (not self.cameraAliasEntry.GetSelection() is wx.NOT_FOUND):
            #if(self.cameraDatabase[self.cameraAliasEntry.ge])
            self.feedPlaying = True
            self.instructionStatus = - 1
            self.calibrateSaveButton.Enable(False)
            cameraID = self.cameraList[self.cameraAliasEntry.GetValue()]
            if(self.cameraDatabase[cameraID]['cameraStatus']['calibAvailable']):
                print("HERE")
                self.calibrater.topViewTransform = np.array(self.cameraDatabase[cameraID]['CalibrationData']['calibrationMatrix'])
                self.calibrater.worldRatio = self.cameraDatabase[cameraID]['CalibrationData']['worldRatio']
                self.calibrater.calibrationDone = 1
            else:
                self.calibrater.calibrationDone = 0


    def updateCameraAliasList(self):
        try:
            with open("cameraDatabase.json", 'r') as jsonFile:
                self.cameraDatabase = json.load(jsonFile)
                for key in self.cameraDatabase:
                    self.cameraList[self.cameraDatabase[key]['cameraAlias']] = key
                    self.cameraAliasEntry.Append(self.cameraDatabase[key]['cameraAlias'])

            self.cameraAliasEntry.Enable(True)
            self.calibrateStartButton.Enable(True)
            self.markerSideEntry.Enable(True)
        except:
            self.cameraAliasEntry.Enable(False)
            self.calibrateStartButton.Enable(False)
            self.markerSideEntry.Enable(False)

    def putFeed(self, event):
        if(self.feedPlaying):
            if(not self.feedBitmap is None):
                dc = wx.BufferedPaintDC(self.calibrationFeed)
                dc.DrawBitmap(self.feedBitmap, 0, 0)

    def scaleFeed(self, tmpBmp):
        image = wx.Bitmap.ConvertToImage(tmpBmp)
        image = image.Scale(self.calibrationFeed.GetSize()[0], self.calibrationFeed.GetSize()[1], wx.IMAGE_QUALITY_HIGH)
        self.feedBitmap = wx.Bitmap(image)

    def updateFeed(self, event):
        if(self.feedPlaying):

            #Get Frame from source
            rvt, self.feed = self.capture.read()

            if(self.isCalibrating):
                if (not self.calibrater.calibrationDone):
                    self.calibrater.calibrate(self.feed, float(self.markerSideEntry.GetValue()))
            else:
                if(self.calibrater.calibrationDone):
                    #print("HERE")
                    self.feed = self.calibrater.drawGroundPlane(self.feed)
                    #self.feed = self.calibrater.findTopView(self.feed)

            if (self.isCalibrating):
                if (not (self.instructionStatus == self.calibrater.calibrationLEDStatus)):
                    print("HERE")
                    #print(self.instructionStatus)
                    #print(self.calibrater.calibrationLEDStatus)
                    self.instructionStatus = self.calibrater.calibrationLEDStatus
                    if (self.calibrater.calibrationLEDStatus == 0):
                        self.instructionText.SetLabel(
                            "Marker Not Found! Marker is either not present or too small to detect")
                        self.instructionText.Wrap(280)
                        self.instructionPanel.Refresh()
                        self.calibrationFeedPanel.Layout()
                    elif (self.calibrater.calibrationLEDStatus == 1):
                        self.instructionText.SetLabel("Wait Calibrating! Do not move the marker")
                        self.instructionText.Wrap(280)
                        self.instructionPanel.Refresh()
                        self.calibrationFeedPanel.Layout()
                    else:
                        #print("Here")
                        self.instructionText.SetLabel("CALIBRATION COMPLETE! Now you can remove marker")
                        self.instructionText.Wrap(280)
                        self.instructionPanel.Refresh()
                        self.calibrationFeedPanel.Layout()
                        self.isCalibrating = False
                        self.calibrateStartButton.SetLabel("Start")
                        self.calibrateSaveButton.Enable(True)
                        self.cameraAliasEntry.Enable(True)
                        self.markerSideEntry.Enable(True)
                else:
                    print(self.instructionStatus)

            frame = cv2.cvtColor(self.feed, cv2.COLOR_BGR2RGB)
            tmpBmp = wx.Bitmap.FromBuffer(frame.shape[1], frame.shape[0], frame)
            self.scaleFeed(tmpBmp)
            self.calibrationFeed.Refresh()

            # check calibration LED status with calibration code
            # if(status == 0)
            # Set instruction text to Aruco not detected place marker on ground
            # if(status == 1)
            # Set instruction text to Calibrating Do not move aruco marker
            # if(status == 2)
            # Set instruction text to Calibration Complete

    def changeColor(self, event, newcolor):
        event.GetEventObject().SetBackgroundColour(newcolor)

    def scaleIcons(self, iconBitmap, iconSize):
        image = wx.Bitmap.ConvertToImage(iconBitmap)
        image = image.Scale(iconSize[0], iconSize[1], wx.IMAGE_QUALITY_HIGH)
        return wx.Bitmap(image)

    def calibStartButtonClicked(self, event):
        if(self.cameraAliasEntry.GetSelection() is wx.NOT_FOUND):
            self.instructionText.SetLabel("Select a camera to calibrate")
            self.instructionText.Wrap(280)
            self.calibrationFeedPanel.Layout()
        else:
            if(self.markerSideEntry.GetValue() == ""):
                self.instructionText.SetLabel("Enter the marker length")
                self.instructionText.Wrap(280)
                self.calibrationFeedPanel.Layout()
            else:
                #self.instructionText.SetLabel("")
                #self.instructionPanel.Layout()
                if(self.isCalibrating):
                    self.isCalibrating = False
                    print(self.isCalibrating)
                    self.calibrateStartButton.SetLabel("Start")
                    self.cameraAliasEntry.Enable(True)
                    self.markerSideEntry.Enable(True)
                    self.instructionStatus = -1
                else:
                    self.isCalibrating = True
                    print(self.isCalibrating)
                    self.calibrateStartButton.SetLabel("Stop")
                    self.cameraAliasEntry.Enable(False)
                    self.markerSideEntry.Enable(False)
                    self.calibrater.calibrationDone = 0
                    self.instructionStatus = -1


#app = wx.App()
#window = Calibration(None)
#app.MainLoop()