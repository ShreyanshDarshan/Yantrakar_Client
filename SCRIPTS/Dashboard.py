import datetime

import wx
import wx.lib.platebtn as plateButtons
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import json
# import mysql.connector as mysql
import pandas as pd
import os
import cv2

two_up = os.path.dirname(os.path.dirname(__file__))
passFile = open(two_up + "/DATA/pass.txt","r")
mysql_pass = passFile.readline()
passFile.close()

class DashboardGallerySlide(wx.Panel):

    def __init__(self, parent, size, image, time, cameraID, cameraAlias, color1, color2, color3):
        self.size = size
        self.image = image
        self.time = time
        self.cameraID = cameraID
        self.cameraAlias = cameraAlias
        self.color1 = color1
        self.color2 = color2
        self.color3 = color3

        self.imageBitmap = wx.Bitmap(wx.NullBitmap)
        #print("SLIDER SIZE")
        #print(size)
        super(DashboardGallerySlide, self).__init__(parent, -1, size=(self.size[0], -1), pos=wx.DefaultPosition)

        self.SetMinSize(self.size)

        self.initSlide()

    def initSlide(self):

        LayoutSlide = wx.BoxSizer(wx.VERTICAL)

        #self.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))

        #self.slideImagePanel = wx.StaticBitmap(self, -1)
        self.slideImagePanel = wx.Panel(self, -1)
        self.slideImagePanel.SetBackgroundColour(self.color2)
        self.slideDetailsPanel = wx.Panel(self, -1)
        self.slideDetailsPanel.SetBackgroundColour(self.color2)

        slideDetailsLayout = wx.BoxSizer(wx.HORIZONTAL)

        slideDetailsLayoutMain = wx.GridBagSizer(0, 0)

        self.cameraAliasLabel = wx.StaticText(self.slideDetailsPanel, -1, "Camera Alias")
        self.cameraAliasLabel.SetForegroundColour(self.color3)
        self.cameraAliasValue = wx.StaticText(self.slideDetailsPanel, -1, self.cameraAlias)
        self.cameraAliasValue.SetForegroundColour(self.color3)
        self.cameraIDLabel = wx.StaticText(self.slideDetailsPanel, -1, "Camera ID")
        self.cameraIDLabel.SetForegroundColour(self.color3)
        self.cameraIDValue = wx.StaticText(self.slideDetailsPanel, -1, self.cameraID)
        self.cameraIDValue.SetForegroundColour(self.color3)
        self.timeLabel = wx.StaticText(self.slideDetailsPanel, -1, "Time")
        self.timeLabel.SetForegroundColour(self.color3)
        self.timeValue = wx.StaticText(self.slideDetailsPanel, -1, self.time)
        self.timeValue.SetForegroundColour(self.color3)

        slideDetailsLayoutMain.Add(self.cameraAliasLabel, wx.GBPosition(0, 0), wx.GBSpan(1, 1), wx.ALL, 5)
        slideDetailsLayoutMain.Add(self.cameraAliasValue, wx.GBPosition(1, 0), wx.GBSpan(1, 1), wx.ALL, 5)
        slideDetailsLayoutMain.Add(self.cameraIDLabel, wx.GBPosition(0, 1), wx.GBSpan(1, 1), wx.ALL, 5)
        slideDetailsLayoutMain.Add(self.cameraIDValue, wx.GBPosition(1, 1), wx.GBSpan(1, 1), wx.ALL, 5)
        slideDetailsLayoutMain.Add(self.timeLabel, wx.GBPosition(0, 2), wx.GBSpan(1, 1), wx.ALL, 5)
        slideDetailsLayoutMain.Add(self.timeValue, wx.GBPosition(1, 2), wx.GBSpan(1, 1), wx.ALL, 5)

        slideDetailsLayout.Add(slideDetailsLayoutMain, proportion=0, flag=wx.EXPAND | wx.ALL, border=10)
        slideDetailsLayout.Add((0, 0), proportion=1, flag=wx.EXPAND | wx.ALL, border=10)

        self.slideDetailsPanel.SetSizer(slideDetailsLayout)
        slideDetailsLayout.Fit(self.slideDetailsPanel)

        LayoutSlide.Add(self.slideDetailsPanel, proportion=0, flag=wx.EXPAND | wx.ALL, border=0)
        LayoutSlide.Add(self.slideImagePanel, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)

        self.SetSizer(LayoutSlide)
        LayoutSlide.Fit(self)
        self.Layout()

        if (self.image is None):
            self.imageBitmap = wx.Bitmap(wx.NullBitmap)
        else:
            self.imageBitmap = wx.Bitmap(self.image, wx.BITMAP_TYPE_ANY)

        #wx.CallAfter(self.addImage)

    # def changeImage(self, newImg):
    #     self.image = newImg
    #     if (self.image is None):
    #         self.imageBitmap = wx.Bitmap(wx.NullBitmap)
    #         self.slideImagePanel.SetBitmap(self.imageBitmap)
    #     else:
    #         self.imageBitmap = wx.Bitmap(self.image, wx.BITMAP_TYPE_ANY)
    #         self.scaleImage()
    #         self.slideImagePanel.SetBitmap(self.imageBitmap)
    #
    # def addImage(self):
    #     if (self.image is None):
    #         # if(self.imageBitmap == wx.NullBitmap):
    #         # self.imageBitmapView = wx.StaticBitmap(self.slideImagePanel, -1, self.imageBitmap)
    #         self.slideImagePanel.SetBitmap(self.imageBitmap)
    #     else:
    #         self.scaleImage()
    #         # self.imageBitmapView = wx.StaticBitmap(self.slideImagePanel, -1, self.imageBitmap)
    #         self.slideImagePanel.SetBitmap(self.imageBitmap)
    #
    # def scaleImage(self):
    #     image = wx.Bitmap.ConvertToImage(self.imageBitmap)
    #     # print(self.slideImagePanel.GetSize())
    #     # print(self.slideDetailsPanel.GetSize())
    #     image = image.Scale(self.slideImagePanel.GetSize()[0], self.slideImagePanel.GetSize()[1], wx.IMAGE_QUALITY_HIGH)
    #     self.imageBitmap = wx.Bitmap(image)


class Dashboard(wx.Panel):

    def __init__(self, parent):
        #super(Dashboard, self).__init__(parent, title="Yantrakar Dashboard", size=(1100, 750))
        super(Dashboard, self).__init__(parent, size=(1100, 750))

        self.parent = parent

        #self.noOfSlides = 3
        self.noOfSlides = 0
        self.slideSpeed = 10
        self.SlidesList = []

        # self.db = mysql.connect(host="localhost", user="root", passwd=mysql_pass, database="test")
        # self.cursor = self.db.cursor()
        # self.databaseName = "cameraDatabaseFinal"

        self.cameraList = {}

        self.galleryImageList = []
        self.prevSliderPos = -1

        self.liveFeedBitmap = None
        self.distancingFeedBitmap = None
        self.maskFeedBitmap = None

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
        self.slightlyLightGrey = wx.Colour(80, 80, 80)
        self.faintWhite = wx.Colour(200, 200, 200)
        self.white = wx.Colour(255, 255, 255)

        self.SetFont(self.fontNormal)
        self.SetBackgroundColour(self.Grey)

        LayoutMain = wx.BoxSizer(wx.HORIZONTAL)

        self.dashboardPanel = wx.ScrolledWindow(self, pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.VSCROLL | wx.HSCROLL)
        self.dashboardPanel.SetScrollRate(5, 5)

        LayoutDashboard = wx.BoxSizer(wx.VERTICAL)

        LayoutDashboardControls = wx.BoxSizer(wx.HORIZONTAL)

        cameraAliasLabel = wx.StaticText(self.dashboardPanel, -1, "Camera Alias")
        cameraAliasLabel.SetForegroundColour(self.faintWhite)

        self.cameraAliasEntry = wx.ComboBox(self.dashboardPanel, -1, "", wx.DefaultPosition, wx.DefaultSize, [], wx.BORDER_NONE)
        self.cameraAliasEntry.Append("All Cameras")
        self.cameraAliasEntry.SetSelection(0)

        # durationLabel = wx.StaticText(self.dashboardPanel, -1, "Date")
        # durationLabel.SetForegroundColour(self.faintWhite)
        # self.durationEntry = wx.ComboBox(self.dashboardPanel, -1)
        #self.durationEntry.Append("All Days")
        #self.durationEntry.Append("Today")
        #self.durationEntry.Append("Last 2 days")
        #self.durationEntry.Append("Last 3 days")
        #self.durationEntry.SetSelection(0)

        self.viewButton = wx.Button(self.dashboardPanel, -1, "View", wx.DefaultPosition, wx.DefaultSize, wx.BORDER_NONE)
        self.viewButton.SetForegroundColour(self.faintWhite)
        self.viewButton.SetBackgroundColour(self.darkGrey)
        self.viewButton.Bind(wx.EVT_ENTER_WINDOW,lambda evt:  self.changeColor(evt, self.Grey))
        self.viewButton.Bind(wx.EVT_LEAVE_WINDOW,lambda evt:  self.changeColor(evt, self.darkGrey))
        self.viewButton.Bind(wx.EVT_LEFT_DOWN, lambda evt:  self.changeColor(evt, self.slightlyLightGrey))
        self.viewButton.Bind(wx.EVT_LEFT_UP, lambda evt:  self.changeColor(self.viewButtonClicked(evt), self.Grey))
        self.viewButton.SetFont(self.fontBold)

        LayoutDashboardControls.Add(wx.Size(0, 0), 1, wx.EXPAND, 0)
        LayoutDashboardControls.Add(cameraAliasLabel, 2, wx.ALL, 0)
        LayoutDashboardControls.Add(self.cameraAliasEntry, 2, wx.ALL, 0)
        LayoutDashboardControls.Add(wx.Size(0, 0), 1, wx.EXPAND, 0)
        # LayoutDashboardControls.Add(durationLabel, 2, wx.ALL, 0)
        # LayoutDashboardControls.Add(self.durationEntry, 2, wx.ALL, 0)
        LayoutDashboardControls.Add(wx.Size(0, 0), 1, wx.EXPAND, 0)
        LayoutDashboardControls.Add(self.viewButton, 2, wx.ALL, 0)
        LayoutDashboardControls.Add(wx.Size(0, 0), 1, wx.EXPAND, 0)


        DashboardGalleryPanel = wx.Panel(self.dashboardPanel, pos=wx.DefaultPosition)
        DashboardGalleryPanel.SetBackgroundColour(self.lightGrey)
        DashboardGalleryPanel.SetMinSize((-1, 500))

        LayoutDashboardGallery = wx.BoxSizer(wx.VERTICAL)

        #self.dashboardGalleryView = wx.ScrolledWindow(DashboardGalleryPanel, pos=wx.DefaultPosition, style=wx.HSCROLL)

        #self.dashboardGalleryView.SetScrollRate(self.slideSpeed, self.slideSpeed)

        self.dashboardGalleryView = wx.Panel(DashboardGalleryPanel, pos=wx.DefaultPosition)

        self.dashboardGalleryView.SetBackgroundColour(self.lightGrey)

        dashboardGalleryControls = wx.Panel(DashboardGalleryPanel, -1, pos=wx.DefaultPosition, size=wx.DefaultSize)
        LayoutDashboardGalleryControls = wx.BoxSizer(wx.HORIZONTAL)

        self.galleryLiveButton = plateButtons.PlateButton(dashboardGalleryControls, -1, "Live", None, wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL | plateButtons.PB_STYLE_SQUARE)
        self.galleryLiveButton.SetMaxSize((50, -1))
        self.galleryLiveButton.SetBackgroundColour(self.darkGrey)
        # self.galleryLiveButton.SetFont(self.fontBold)
        self.galleryLiveButton.SetForegroundColour(self.white)
        self.galleryLiveButton.SetPressColor(self.darkGrey)

        self.galleryPauseButton = plateButtons.PlateButton(dashboardGalleryControls, -1, "", wx.Bitmap(two_up + "/ui_elements/pause.png"), wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL | plateButtons.PB_STYLE_SQUARE)
        self.isPlaying = True
        self.galleryPauseButton.SetMaxSize((40, -1))
        self.galleryPauseButton.SetBackgroundColour(self.darkGrey)
        self.galleryPauseButton.SetFont(self.fontBold)
        self.galleryPauseButton.SetForegroundColour(self.white)
        self.galleryPauseButton.Bind(wx.EVT_BUTTON, self.toggle_play)
        self.galleryPauseButton.SetPressColor(self.lightGrey)


        self.gallerySlider = wx.Slider(dashboardGalleryControls, -1, 0, 0, 3)
        self.gallerySlider.SetBackgroundColour(self.darkGrey)
        self.gallerySlider.Enable(False)
        self.gallerySlider.Hide()
        # self.gallerySlider.SetForegroundColour(self.white)
        # self.galleryLiveButton.SetPressColor(self.Grey)

        LayoutDashboardGalleryControls.Add(self.galleryLiveButton, proportion=1, flag=wx.ALIGN_CENTER, border=0)
        LayoutDashboardGalleryControls.Add(self.galleryPauseButton, proportion=1, flag=wx.ALL, border=0)
        LayoutDashboardGalleryControls.Add(self.gallerySlider, proportion=8, flag=wx.ALIGN_CENTER, border=0)


        dashboardGalleryControls.SetSizer(LayoutDashboardGalleryControls)
        dashboardGalleryControls.SetBackgroundColour(self.darkGrey)
        LayoutDashboardGalleryControls.Fit(dashboardGalleryControls)

        LayoutDashboardGallery.Add(self.dashboardGalleryView, proportion=1, flag=wx.EXPAND | wx.ALL, border=0)
        LayoutDashboardGallery.Add(dashboardGalleryControls, proportion=0, flag=wx.EXPAND | wx.ALL, border=0)

        dashboardGalleryControls.Hide()

        DashboardGalleryPanel.SetSizer(LayoutDashboardGallery)
        LayoutDashboardGallery.Fit(DashboardGalleryPanel)


        # self.DashboardGraphPanel = wx.StaticBitmap(self.dashboardPanel, -1, wx.Bitmap(two_up + "/DATA/plot.png"), pos=wx.DefaultPosition, size=wx.Size(1100, 300))
        # self.DashboardGraphPanel.SetBackgroundColour(self.Grey)
        # # self.DashboardGraphPanel.AutoLayout()
        # self.DashboardGraphPanel.SetMinSize((-1, 500))

        ######################################################################################################
        # MASK GALLERY
        DashboardMaskGalleryPanel = wx.Panel(self.dashboardPanel, pos=wx.DefaultPosition)
        DashboardMaskGalleryPanel.SetBackgroundColour(self.lightGrey)
        DashboardMaskGalleryPanel.SetMinSize((-1, 500))

        LayoutDashboardMaskGallery = wx.BoxSizer(wx.VERTICAL)

        self.dashboardMaskGalleryView = wx.Panel(DashboardMaskGalleryPanel, pos=wx.DefaultPosition)

        self.dashboardMaskGalleryView.SetBackgroundColour(self.lightGrey)

        # dashboardMaskGalleryControls = wx.Panel(DashboardMaskGalleryPanel, -1, pos=wx.DefaultPosition, size=wx.DefaultSize)
        # LayoutDashboardMaskGalleryControls = wx.BoxSizer(wx.HORIZONTAL)
        #
        # self.maskGalleryLiveButton = plateButtons.PlateButton(dashboardMaskGalleryControls, -1, "Live", None,
        #                                                   wx.DefaultPosition, wx.DefaultSize,
        #                                                   wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL | plateButtons.PB_STYLE_SQUARE)
        # self.maskGalleryLiveButton.SetMaxSize((50, -1))
        # self.maskGalleryLiveButton.SetBackgroundColour(self.darkGrey)
        # # self.maskGalleryLiveButton.SetFont(self.fontBold)
        # self.maskGalleryLiveButton.SetForegroundColour(self.white)
        # self.maskGalleryLiveButton.SetPressColor(self.darkGrey)
        #
        # self.maskGalleryPauseButton = plateButtons.PlateButton(dashboardMaskGalleryControls, -1, "",
        #                                                    wx.Bitmap(two_up + "/ui_elements/pause.png"),
        #                                                    wx.DefaultPosition, wx.DefaultSize,
        #                                                    wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL | plateButtons.PB_STYLE_SQUARE)
        # self.isPlayingMaskGallery = True
        # self.maskGalleryPauseButton.SetMaxSize((40, -1))
        # self.maskGalleryPauseButton.SetBackgroundColour(self.darkGrey)
        # self.maskGalleryPauseButton.SetFont(self.fontBold)
        # self.maskGalleryPauseButton.SetForegroundColour(self.white)
        # self.maskGalleryPauseButton.Bind(wx.EVT_BUTTON, self.toggle_play)
        # self.maskGalleryPauseButton.SetPressColor(self.lightGrey)
        #
        # self.maskGallerySlider = wx.Slider(dashboardMaskGalleryControls, -1, 0, 0, 3)
        # self.maskGallerySlider.SetBackgroundColour(self.darkGrey)
        # self.maskGallerySlider.Enable(False)
        # self.maskGallerySlider.Hide()
        # # self.maskGallerySlider.SetForegroundColour(self.white)
        # # self.maskGalleryLiveButton.SetPressColor(self.Grey)
        #
        # LayoutDashboardMaskGalleryControls.Add(self.maskGalleryLiveButton, proportion=1, flag=wx.ALIGN_CENTER, border=0)
        # LayoutDashboardMaskGalleryControls.Add(self.maskGalleryPauseButton, proportion=1, flag=wx.ALL, border=0)
        # LayoutDashboardMaskGalleryControls.Add(self.maskGallerySlider, proportion=8, flag=wx.ALIGN_CENTER, border=0)
        #
        # dashboardMaskGalleryControls.SetSizer(LayoutDashboardMaskGalleryControls)
        # dashboardMaskGalleryControls.SetBackgroundColour(self.darkGrey)
        # LayoutDashboardMaskGalleryControls.Fit(dashboardMaskGalleryControls)

        LayoutDashboardMaskGallery.Add(self.dashboardMaskGalleryView, proportion=1, flag=wx.EXPAND | wx.ALL, border=0)
        # LayoutDashboardMaskGallery.Add(dashboardMaskGalleryControls, proportion=0, flag=wx.EXPAND | wx.ALL, border=0)

        DashboardMaskGalleryPanel.SetSizer(LayoutDashboardMaskGallery)
        LayoutDashboardMaskGallery.Fit(DashboardMaskGalleryPanel)
        ######################################################################################################

        #LIVE FEED Controls
        # LayoutLiveFeedControls = wx.BoxSizer(wx.HORIZONTAL)
        #
        # cameraAliasLiveFeedLabel = wx.StaticText(self.dashboardPanel, -1, "Camera Alias")
        # cameraAliasLiveFeedLabel.SetForegroundColour(self.faintWhite)
        # cameraAliasLiveFeedLabel.SetMaxSize((200, -1))
        #
        # self.cameraAliasLiveFeedEntry = wx.ComboBox(self.dashboardPanel, -1, "", wx.DefaultPosition, wx.DefaultSize, [],
        #                                     wx.BORDER_NONE)
        # self.cameraAliasLiveFeedEntry.SetMaxSize((250, -1))
        #
        # self.viewLiveFeedButton = wx.Button(self.dashboardPanel, -1, "View", wx.DefaultPosition, wx.DefaultSize, wx.BORDER_NONE)
        # self.viewLiveFeedButton.SetForegroundColour(self.faintWhite)
        # self.viewLiveFeedButton.SetBackgroundColour(self.darkGrey)
        # self.viewLiveFeedButton.Bind(wx.EVT_ENTER_WINDOW, lambda evt: self.changeColor(evt, self.Grey))
        # self.viewLiveFeedButton.Bind(wx.EVT_LEAVE_WINDOW, lambda evt: self.changeColor(evt, self.darkGrey))
        # self.viewLiveFeedButton.Bind(wx.EVT_LEFT_DOWN, lambda evt: self.changeColor(evt, self.slightlyLightGrey))
        # self.viewLiveFeedButton.Bind(wx.EVT_LEFT_UP, lambda evt: self.changeColor(self.viewLiveFeedButtonClicked(evt), self.Grey))
        # self.viewLiveFeedButton.SetFont(self.fontBold)
        # self.viewLiveFeedButton.SetMaxSize((200, -1))
        #
        # LayoutLiveFeedControls.Add(wx.Size(0, 0), 1, wx.EXPAND, 0)
        # LayoutLiveFeedControls.Add(cameraAliasLiveFeedLabel, 2, wx.ALL, 0)
        # LayoutLiveFeedControls.Add(self.cameraAliasLiveFeedEntry, 2, wx.ALL, 0)
        # LayoutLiveFeedControls.Add(wx.Size(0, 0), 1, wx.EXPAND, 0)
        # LayoutLiveFeedControls.Add(wx.Size(0, 0), 1, wx.EXPAND, 0)
        # LayoutLiveFeedControls.Add(self.viewLiveFeedButton, 2, wx.ALL, 0)
        # LayoutLiveFeedControls.Add(wx.Size(0, 0), 1, wx.EXPAND, 0)

        #LIVE FEED Panel

        DashboardLiveFeedMainPanel = wx.Panel(self.dashboardPanel, pos=wx.DefaultPosition)
        DashboardLiveFeedMainPanel.SetBackgroundColour(self.darkGrey)
        DashboardLiveFeedMainPanel.SetMinSize((-1, 500))
        DashboardLiveFeedLayout = wx.BoxSizer(wx.VERTICAL)

        DashboardLiveFeedHeadLayout = wx.GridBagSizer(0, 0)

        self.cameraAliasLiveFeedLabel = wx.StaticText(DashboardLiveFeedMainPanel, -1, "Camera Alias")
        self.cameraAliasLiveFeedLabel.SetForegroundColour(self.white)
        self.cameraAliasLiveFeedValue = wx.StaticText(DashboardLiveFeedMainPanel, -1, "")
        self.cameraAliasLiveFeedValue.SetForegroundColour(self.white)
        self.cameraIDLiveFeedLabel = wx.StaticText(DashboardLiveFeedMainPanel, -1, "Camera ID")
        self.cameraIDLiveFeedLabel.SetForegroundColour(self.white)
        self.cameraIDLiveFeedValue = wx.StaticText(DashboardLiveFeedMainPanel, -1, "")
        self.cameraIDLiveFeedValue.SetForegroundColour(self.white)

        DashboardLiveFeedHeadLayout.Add(self.cameraAliasLiveFeedLabel, wx.GBPosition(0, 0), wx.GBSpan(1, 1), wx.ALL, 5)
        DashboardLiveFeedHeadLayout.Add(self.cameraAliasLiveFeedValue, wx.GBPosition(1, 0), wx.GBSpan(1, 1), wx.ALL, 5)
        DashboardLiveFeedHeadLayout.Add(self.cameraIDLiveFeedLabel, wx.GBPosition(0, 1), wx.GBSpan(1, 1), wx.ALL, 5)
        DashboardLiveFeedHeadLayout.Add(self.cameraIDLiveFeedValue, wx.GBPosition(1, 1), wx.GBSpan(1, 1), wx.ALL, 5)

        self.DashboardLiveFeedPanel = wx.Panel(DashboardLiveFeedMainPanel, pos=wx.DefaultPosition)
        self.DashboardLiveFeedPanel.SetBackgroundColour(self.darkGrey)
        self.DashboardLiveFeedPanel.SetMinSize((-1, 500))

        DashboardLiveFeedLayout.Add(DashboardLiveFeedHeadLayout, proportion=0, flag=wx.EXPAND | wx.ALL, border=10)
        DashboardLiveFeedLayout.Add(self.DashboardLiveFeedPanel, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)

        DashboardLiveFeedMainPanel.SetSizer(DashboardLiveFeedLayout)
        DashboardLiveFeedMainPanel.Layout()
        DashboardLiveFeedLayout.Fit(DashboardLiveFeedMainPanel)

        #self.initialiseCameras()
        self.LiveFeedPlaying = False
        self.currentLiveFeedCamera = ""
        self.liveFeedFPS = 30

        ######################################################################################################

        LayoutDashboardAllViews = wx.BoxSizer(wx.HORIZONTAL)
        LayoutDashboardAllViews.Add(DashboardLiveFeedMainPanel, proportion=1, flag=wx.EXPAND | wx.ALL, border = 2)
        LayoutDashboardAllViews.Add(DashboardGalleryPanel, proportion=1, flag=wx.EXPAND | wx.ALL, border=2)
        LayoutDashboardAllViews.Add(DashboardMaskGalleryPanel, proportion=1, flag=wx.EXPAND | wx.ALL, border=2)

        #LayoutDashboard.Add(LayoutLiveFeedControls, proportion=0, flag=wx.EXPAND | wx.ALL, border=30)
        #LayoutDashboard.Add(self.DashboardLiveFeedPanel, proportion=0, flag=wx.EXPAND | wx.ALL, border=30)
        LayoutDashboard.Add(LayoutDashboardControls, proportion=1, flag=wx.EXPAND | wx.ALL, border=30)
        #LayoutDashboard.Add(DashboardGalleryPanel, proportion=1, flag=wx.EXPAND | wx.ALL, border=30)
        #LayoutDashboard.Add(DashboardMaskGalleryPanel, proportion=1, flag=wx.EXPAND | wx.ALL, border=30)
        LayoutDashboard.Add(LayoutDashboardAllViews, proportion=4, flag=wx.EXPAND | wx.ALL, border=30)
        #LayoutDashboard.Add(self.DashboardGraphPanel, proportion=1, flag=wx.ALIGN_CENTER, border=30)

        self.dashboardPanel.SetSizer(LayoutDashboard)
        self.dashboardPanel.Layout()
        LayoutDashboard.Fit(self.dashboardPanel)

        #   LayoutMain.Add(self.navPanel, proportion=0, flag=wx.EXPAND | wx.ALL, border=0)
        LayoutMain.Add(self.dashboardPanel, proportion=1, flag=wx.EXPAND | wx.ALL, border=0)

        self.LayoutDashboardGalleryView = wx.GridBagSizer(0, 0)

        #slide1 = DashboardGallerySlide(self.dashboardGalleryView, self.dashboardGalleryView.GetSize(), "ui_elements/test.png", "10:00 AM", "camera#1", "CAM1", self.lightGrey, self.darkGrey, self.white)
        #slide2 = DashboardGallerySlide(self.dashboardGalleryView, self.dashboardGalleryView.GetSize(), "ui_elements/test.png", "1:00 PM", "camera#2", "CAM2", self.lightGrey, self.darkGrey, self.white)
        #slide3 = DashboardGallerySlide(self.dashboardGalleryView, self.dashboardGalleryView.GetSize(), "ui_elements/test.png", "1:00 PM", "camera#3", "CAM3", self.lightGrey, self.darkGrey, self.white)

        #self.SlidesList.append(slide1)
        #self.SlidesList.append(slide2)
        #self.SlidesList.append(slide3)

        #self.LayoutDashboardGalleryView.Add(slide1, wx.GBPosition(0, 0), wx.GBSpan(1, 1), wx.ALL, 0)
        #self.LayoutDashboardGalleryView.Add(slide2, wx.GBPosition(0, 1), wx.GBSpan(1, 1), wx.ALL, 0)
        #self.LayoutDashboardGalleryView.Add(slide3, wx.GBPosition(0, 2), wx.GBSpan(1, 1), wx.ALL, 0)

        self.dashboardGalleryViewSlide = DashboardGallerySlide(self.dashboardGalleryView,
                                                               self.dashboardGalleryView.GetSize(),
                                                               None, "", "", "", self.lightGrey,
                                                               self.darkGrey, self.white)
        self.dashboardGalleryViewSlide.SetBackgroundColour(self.darkGrey)
        self.LayoutDashboardGalleryView.Add(self.dashboardGalleryViewSlide, wx.GBPosition(0, 0), wx.GBSpan(1, 1),
                                            wx.ALL, 0)

        self.dashboardGalleryView.SetSizer(self.LayoutDashboardGalleryView)
        self.LayoutDashboardGalleryView.Fit(self.dashboardGalleryView)
        self.dashboardGalleryView.Layout()

        ##################################################################################################
        self.LayoutDashboardMaskGalleryView = wx.GridBagSizer(0, 0)
        self.dashboardMaskGalleryViewSlide = DashboardGallerySlide(self.dashboardMaskGalleryView,
                                                               self.dashboardMaskGalleryView.GetSize(),
                                                               None, "", "", "", self.lightGrey,
                                                               self.darkGrey, self.white)
        self.dashboardMaskGalleryViewSlide.SetBackgroundColour(self.darkGrey)
        self.LayoutDashboardMaskGalleryView.Add(self.dashboardMaskGalleryViewSlide, wx.GBPosition(0, 0), wx.GBSpan(1, 1),
                                            wx.ALL, 0)

        self.dashboardMaskGalleryView.SetSizer(self.LayoutDashboardMaskGalleryView)
        self.LayoutDashboardMaskGalleryView.Fit(self.dashboardMaskGalleryView)
        self.dashboardMaskGalleryView.Layout()
        ##################################################################################################

        #self.dashboardGalleryView.ShowScrollbars(wx.SHOW_SB_NEVER, wx.SHOW_SB_NEVER)

        self.SetSizer(LayoutMain)
        self.Layout()

        self.Center()
        #self.Show(True)

        self.updateGalleryPanel()
        self.updateCameraAliasList()
        # self.updateDurationEntry()

        self.gallerySlider.Bind(wx.EVT_SLIDER, self.onGallerySlider)

        # self.timer = wx.Timer(self)
        # self.timer.Start(1)
        # self.slideshowDirection = 1
        #
        # self.waitTimer = wx.Timer(self)
        #
        # self.Bind(wx.EVT_TIMER, self.playSlideShow, self.timer)
        # self.Bind(wx.EVT_TIMER, self.pauseSlideShow, self.waitTimer)

        self.Bind(wx.EVT_SIZE, self.mainWindowSizeChange)

        self.SetWindowStyleFlag(wx.TRANSPARENT_WINDOW)

        self.liveFeedTimer = wx.Timer(self)
        self.liveFeedTimer.Start(1000 / self.liveFeedFPS)
        self.Bind(wx.EVT_TIMER, self.updateFeed, self.liveFeedTimer)
        self.DashboardLiveFeedPanel.Bind(wx.EVT_PAINT, self.putFeed)

        # self.liveDistancingTimer = wx.Timer(self)
        # self.liveDistancingTimer.Start(1000 / self.liveFeedFPS)
        # self.Bind(wx.EVT_TIMER, self.updateFeedDistancing, self.liveDistancingTimer)
        self.dashboardGalleryViewSlide.slideImagePanel.Bind(wx.EVT_PAINT, self.putFeedDistancing)

        # self.liveMaskTimer = wx.Timer(self)
        # self.liveMaskTimer.Start(1000 / self.liveFeedFPS)
        # self.Bind(wx.EVT_TIMER, self.updateFeedMask, self.liveMaskTimer)
        self.dashboardMaskGalleryViewSlide.slideImagePanel.Bind(wx.EVT_PAINT, self.putFeedMask)

        print ("can set transparent")
        print (self.CanSetTransparent())

        DashboardLiveFeedMainPanel.SetMaxSize((-1, DashboardLiveFeedMainPanel.GetSize()[0] + 80))
        DashboardGalleryPanel.SetMaxSize((-1, DashboardGalleryPanel.GetSize()[0] + 80))
        DashboardMaskGalleryPanel.SetMaxSize((-1, DashboardMaskGalleryPanel.GetSize()[0] + 80))

        self.Layout()
    # def updateDurationEntry(self):
    #     for i in range(0, 5):
    #         d = datetime.datetime.today() - datetime.timedelta(days=i)
    #         self.durationEntry.Append(str(d.date().strftime("%d-%m-%Y")))
    #     self.durationEntry.SetSelection(0)

    def getImageNames(self, cameraID, day):
        #open csv file according to day value
        #import data from csv
        #csvData = pd.read_csv("31072020.csv", dtype=str)

        stamps = []
        if(os.path.exists(two_up + "/DATA/" + day + ".csv")):
            csvData = pd.read_csv(two_up + "/DATA/" + day + ".csv", dtype=str)
            # csvData = [{'cameraid': "000001", 'frameid': "00000128063739415"},
            #            {'cameraid': "000001", 'frameid': "00000128063739415"},
            #            {'cameraid': "000001", 'frameid': "00000128063739415"},
            #            {'cameraid': "000001", 'frameid': "00000128063739415"},
            #            {'cameraid': "000001", 'frameid': "00000128063739415"},
            #            {'cameraid': "000001", 'frameid': "00000128063739415"},
            #            {'cameraid': "000001", 'frameid': "00000128063739415"},
            #            {'cameraid': "000001", 'frameid': "00000128063739415"},
            #            {'cameraid': "000001", 'frameid': "00000128063739415"},
            #            {'cameraid': "000001", 'frameid': "00000128063739415"},
            #            {'cameraid': "000001", 'frameid': "00000128063739415"},
            #            {'cameraid': "000001", 'frameid': "00000128063739415"},
            #            {'cameraid': "000001", 'frameid': "00000128063739415"},
            #            {'cameraid': "000001", 'frameid': "00000128063739415"},
            #            {'cameraid': "000001", 'frameid': "00000128063739415"}]

            df = csvData
            #df = pd.DataFrame(csvData)

            if (cameraID is None):
                stamps = df['frameID']
            else:
                cameraID = "A" + cameraID
                stamps = df.loc[df['cameraID'] == cameraID]['frameID']

            stamps = list(stamps)
            for i in range(0, len(stamps)):
                stamps[i] = stamps[i][1:]

            #print(df['cameraID'])
            #print('frameId')
            print(stamps)
            #print('DATA LENGTH')
            #print(len(stamps))

        return stamps

    def viewButtonClicked(self, event):
        cameraAlias = self.cameraAliasEntry.GetValue()
        cameraID = ""
        #day = 0
        day = "0"
        if (cameraAlias == "All Cameras"):
            cameraID = None
        else:
            cameraID = self.cameraList[cameraAlias]

        #duration = self.durationEntry.GetValue()

        # day = self.durationEntry.GetValue().split('-')
        # day = day[0] + day[1] + day[2]
        # print(day)

        # imageNamesList = self.getImageNames(cameraID, day)
        # self.noOfSlides = len(imageNamesList)
        # if (self.noOfSlides):
        #     #self.galleryActive = True
        #     self.galleryImageList = imageNamesList
        # #self.addSlides(list(imageNamesList))
        # self.updateGalleryPanel()
        # self.updateSlideData()
        # #self.plotData(list(imageNamesList))

        self.startLiveFeed()
        return event

    def updateSlideData(self):
        if(self.galleryImageList):
            currentSlide = self.gallerySlider.GetValue()
            i = self.galleryImageList[currentSlide]
            time = i[6:8] + " " + i[8:10] + ":" + i[10:12] + ":" + i[12:14] + ":" + i[14:18]
            cameraID = i[0:6]
            cameraAlias = list(self.cameraList.keys())[list(self.cameraList.values()).index(cameraID)]
            self.dashboardGalleryViewSlide.changeImage(two_up + "/FRAMES/" + list(self.galleryImageList)[currentSlide] + ".png")
            self.dashboardGalleryViewSlide.cameraIDValue.SetLabel(cameraID)
            self.dashboardGalleryViewSlide.cameraAliasValue.SetLabel(cameraAlias)
            self.dashboardGalleryViewSlide.timeValue.SetLabel(time)
            self.Layout()
        pass

    # Plot graph for a particular day
    # def plotData(self, imageNameList):
    #     timeInterval = 1
    #     y = [0] * 24
    #     x_list = [item for item in range(1, 25)]
    #
    #     for img in imageNameList:
    #         hour = int(img[8:10])
    #         if (hour == 0 and int(img[10:12]) == 0):
    #             y[23] = y[23] + 1
    #         else:
    #             if (int(img[10:12]) == 0):
    #                 y[hour - 1] = y[hour - 1] + 1
    #             else:
    #                 y[hour] = y[hour] + 1
    #
    #     x_labels = []
    #     for i in range(0, 24):
    #         x_labels.append("TIME:\n" + str((i)) + "-" + str(((i + 1))))
    #
    #     plt.style.use(u'dark_background')
    #     fig = plt.figure()
    #     plt.xticks(x_list, x_labels)
    #     ax = plt.subplot(111)
    #     ax.plot(x_list, y, label='$y = numbers')
    #     plt.title('Legend inside')
    #     ax.legend()
    #     # plt.show()
    #     fig.set_size_inches(15, 5)
    #     fig.tight_layout()
    #     fig.savefig(two_up + '/DATA/plot.png', transparent=True)
    #     self.DashboardGraphPanel.SetBitmap(wx.Bitmap(two_up + "/DATA/plot.png"))
    #     self.DashboardGraphPanel.Refresh()
    #     self.Layout()


    def updateCameraAliasList(self):
        self.cameraAliasEntry.Clear()
        self.cameraAliasEntry.Append("All Cameras")
        self.cameraAliasEntry.SetSelection(0)

        #self.cameraAliasLiveFeedEntry.Clear()
        try:
            with open(two_up + "/DATA/cameraDatabase.json", 'r') as jsonFile:
                self.cameraDatabase = json.load(jsonFile)
                for key in self.cameraDatabase:
                    self.cameraList[self.cameraDatabase[key]['cameraAlias']] = key
                    self.cameraAliasEntry.Append(self.cameraDatabase[key]['cameraAlias'])
                    #self.cameraAliasLiveFeedEntry.Append(self.cameraDatabase[key]['cameraAlias'])

            self.initialiseCameras()

            self.cameraAliasEntry.Enable(True)
            # self.durationEntry.Enable(True)
            self.viewButton.Enable(True)

            #self.cameraAliasLiveFeedEntry.Enable(True)
            #self.viewLiveFeedButton.Enable(True)
        except:
            self.cameraAliasEntry.Enable(False)
            # self.durationEntry.Enable(False)
            self.viewButton.Enable(False)

            #self.cameraAliasLiveFeedEntry.Enable(False)
            #self.viewLiveFeedButton.Enable(False)

    def updateSlideImages(self, value):
        currSliderPos = int(
            (self.gallerySlider.GetValue() / (self.dashboardGalleryView.GetSize()[0])) * self.slideSpeed + 0.5)

        if((currSliderPos - self.prevSliderPos) > 0):
            self.prevSliderPos = currSliderPos
            deletepos = currSliderPos - 5
            addPos = currSliderPos + 4

            if(deletepos >= 0):
                slide = self.SlidesList[deletepos]
                slide.changeImage(None)
                self.Layout()

            if(addPos < self.noOfSlides):
                slide = self.SlidesList[addPos]
                slide.changeImage(two_up + "/FRAMES/" + list(self.galleryImageList)[addPos] + ".png")
                self.Layout()
            pass
        elif((currSliderPos - self.prevSliderPos) < 0):
            deletepos = self.prevSliderPos + 5
            addPos = self.prevSliderPos - 3

            if(deletepos < self.noOfSlides):
                slide = self.SlidesList[deletepos]
                slide.changeImage(None)
                #slide.Refresh()
                self.Layout()
            if(addPos >= 0):
                slide = self.SlidesList[addPos]
                #print(list(self.galleryImageList)[addPos])
                slide.changeImage(two_up + "/FRAMES/" + list(self.galleryImageList)[addPos] + ".png")
                #slide.Refresh()
                self.Layout()
            self.prevSliderPos = currSliderPos
            pass

    def addSlides(self, imgNameList):
        self.isPlaying = False
        self.timer.Stop()
        self.LayoutDashboardGalleryView.Clear(True)

        # for i in self.SlidesList:
        #    i.Remove(self.LayoutDashboardGalleryView)
        self.SlidesList.clear()

        slideNo = 0
        for i in imgNameList:
            time = i[6:8] + " " + i[8:10] + ":" + i[10:12] + ":" + i[12:14] + ":" + i[14:18]
            cameraID = i[0:6]
            cameraAlias = list(self.cameraList.keys())[list(self.cameraList.values()).index(cameraID)]

            # slide1 = DashboardGallerySlide(self.dashboardGalleryView, self.dashboardGalleryView.GetSize(), "./FRAMES/" + i + ".png", time, cameraID, cameraAlias, self.lightGrey, self.darkGrey, self.white)
            slide1 = DashboardGallerySlide(self.dashboardGalleryView, self.dashboardGalleryView.GetSize(),
                                           None, time, cameraID, cameraAlias, self.lightGrey,
                                           self.darkGrey, self.white)
            self.SlidesList.append(slide1)
            self.LayoutDashboardGalleryView.Add(slide1, wx.GBPosition(0, slideNo), wx.GBSpan(1, 1), wx.ALL, 0)
            slideNo = slideNo + 1

        self.Layout()

        self.prevSliderPos = 0
        currentSliderPos = 0

        for i in range(0, len(imgNameList)):
            if (i < 5):
                slide = self.SlidesList[i]
                slide.changeImage(two_up + "/FRAMES/" + imgNameList[i] + ".png")

        self.Layout()
        self.timer.Start(1)


        #For drawing line
        # sampleItem = "10 20|30 40,100 120|150 200"
        # pointList = sampleItem.split(',')

        # for i in pointList:
        #    points = pointList[i].split('|')
        #    point1 = points[0]
        #    point2 = points[1]
        #    point1 = point1.split(' ')
        #    point1 = (int(point1[0]), int(point1[1]))
        #    point2 = point2.split(' ')
        #    point2 = (int(point2[0]), int(point2[1]))
        #    #cv2.line(img, point1, point2, (0, 0, 255), 1)
        #    #cv2.imwrite(imgname, img)
        pass

    def scaleIcons(self, iconBitmap, iconSize):
        image = wx.Bitmap.ConvertToImage(iconBitmap)
        image = image.Scale(iconSize[0], iconSize[1], wx.IMAGE_QUALITY_HIGH)
        return wx.Bitmap(image)

    def updateGalleryPanel(self):
        if(self.noOfSlides > 1):
            self.gallerySlider.Enable(True)
            #self.gallerySlider.SetRange(0, int((self.dashboardGalleryView.GetSize()[0]) * (self.noOfSlides - 1)/ self.slideSpeed))
            self.gallerySlider.SetRange(0, self.noOfSlides)
            self.galleryPauseButton.Enable(True)
        else:
            self.gallerySlider.SetRange(0, 1)
            self.gallerySlider.Enable(False)

        if(self.noOfSlides <= 1):
            self.galleryPauseButton.Enable(False)
            self.isPlaying = False


    # def pauseSlideShow(self, event):
    #     if(self.isPlaying):
    #         self.waitTimer.Stop()
    #         self.timer.Start(1)

    # def playSlideShow(self, event):
    #     if(self.isPlaying):
    #         # if (self.gallerySlider.GetValue() % int(self.gallerySlider.GetRange()[1] / (self.noOfSlides - 1)) == 0):
    #         #     self.waitTimer.Start(1000)
    #         #     self.timer.Stop()
    #
    #         if(self.slideshowDirection == 1):
    #             self.gallerySlider.SetValue(self.gallerySlider.GetValue() + 1)
    #             self.waitTimer.Start(2000)
    #             self.timer.Stop()
    #         else:
    #             self.gallerySlider.SetValue(self.gallerySlider.GetValue() - 1)
    #             self.waitTimer.Start(2000)
    #             self.timer.Stop()
    #
    #         self.onGallerySlider(event)

    def onGallerySlider(self, event):
        val = self.gallerySlider.GetValue()

        #if(self.noOfSlides > 5):
        #    wx.CallAfter(self.updateSlideImages, val)

        wx.CallAfter(self.updateSlideData)

        if(val >= self.gallerySlider.GetRange()[1]):
            self.slideshowDirection = -1
        elif(val == 0):
            self.slideshowDirection = 1

        #self.dashboardGalleryView.Scroll(int(val), -1)

    def mainWindowSizeChangeUpdate(self, event):
        for i in self.SlidesList:
            i.size = self.dashboardGalleryView.GetSize()
            i.SetSize((self.dashboardGalleryView.GetSize()[0], -1))
            i.SetMinSize(self.dashboardGalleryView.GetSize())
            i.addImage()

        self.dashboardGalleryViewSlide.size = self.dashboardGalleryView.GetSize()
        self.dashboardGalleryViewSlide.SetSize((self.dashboardGalleryView.GetSize()[0], -1))
        self.dashboardGalleryViewSlide.SetMinSize(self.dashboardGalleryView.GetSize())
        #self.dashboardGalleryViewSlide.addImage()

        self.dashboardMaskGalleryViewSlide.size = self.dashboardMaskGalleryView.GetSize()
        self.dashboardMaskGalleryViewSlide.SetSize((self.dashboardMaskGalleryView.GetSize()[0], -1))
        self.dashboardMaskGalleryViewSlide.SetMinSize(self.dashboardMaskGalleryView.GetSize())
        #self.dashboardMaskGalleryViewSlide.addImage()

        self.dashboardGalleryView.Refresh()
        self.dashboardMaskGalleryView.Refresh()
        #self.gallerySlider.SetRange(0, int((self.dashboardGalleryView.GetSize()[0]) * (self.noOfSlides - 1) / self.slideSpeed))
        self.gallerySlider.SetRange(0, self.noOfSlides)
        wx.CallAfter(self.Layout)

    def mainWindowSizeChange(self, event):
        self.Layout()
        wx.CallAfter(self.mainWindowSizeChangeUpdate, event)


    def toggle_play(self, event):
        if self.isPlaying:
            self.galleryPauseButton.SetBitmap(wx.Bitmap(two_up + "/ui_elements/play.png"))
            self.isLive = False
            self.isPlaying = False
        else:
            self.galleryPauseButton.SetBitmap(wx.Bitmap(two_up + "/ui_elements/pause.png"))
            self.isPlaying = True

    def changeColor(self, event, newcolor):
        event.GetEventObject().SetBackgroundColour(newcolor)

    def startLiveFeed(self):
        # if (not self.cameraAliasLiveFeedEntry.GetSelection() is wx.NOT_FOUND):
        #     self.LiveFeedPlaying = True
        #     cameraID = self.cameraList[self.cameraAliasLiveFeedEntry.GetValue()]
        #     self.currentLiveFeedCamera = cameraID
        self.LiveFeedPlaying = True
        cameraAlias = self.cameraAliasEntry.GetValue()
        cameraID = ""
        day = 0
        if (cameraAlias == "All Cameras"):
            if(len(self.cameraList)):
                camera_Alias = list(self.cameraList.keys())[0]
                camera_ID = self.cameraList[camera_Alias]
                self.currentLiveFeedCamera = camera_ID
                self.cameraIDLiveFeedValue.SetLabel(camera_ID)
                self.cameraAliasLiveFeedValue.SetLabel(camera_Alias)
        else:
            cameraID = self.cameraList[cameraAlias]
            self.currentLiveFeedCamera = cameraID
            self.cameraIDLiveFeedValue.SetLabel(cameraID)
            self.cameraAliasLiveFeedValue.SetLabel(cameraAlias)

    def initialiseCameras(self):
        self.cap={}
        for camerakey,cameraData in self.cameraDatabase.items():
            #self.cap[camerakey] = cv2.VideoCapture("rtsp://"+cameraData["cameraID"]+":"+cameraData["cameraPassword"]+"@"+cameraData["cameraIP"])
            self.cap[camerakey] = cv2.VideoCapture(two_up + "/test_video/top.mp4") # cv2.VideoCapture(cameraData["url"])
            self.cap[camerakey].set(cv2.CAP_PROP_FPS,1)
            self.cap[camerakey].set(cv2.CAP_PROP_FRAME_HEIGHT, 300)
            self.cap[camerakey].set(cv2.CAP_PROP_FRAME_HEIGHT, 300)

    def putFeed(self, event):
        if(self.LiveFeedPlaying):
            if(not self.liveFeedBitmap is None):
                dc = wx.BufferedPaintDC(self.DashboardLiveFeedPanel)
                dc.DrawBitmap(self.liveFeedBitmap, 0, 0)

    def putFeedDistancing(self, event):
        if(self.LiveFeedPlaying):
            if(not self.distancingFeedBitmap is None):
                dc = wx.BufferedPaintDC(self.dashboardGalleryViewSlide.slideImagePanel)
                dc.DrawBitmap(self.distancingFeedBitmap, 0, 0)

    def putFeedMask(self, event):
        if(self.LiveFeedPlaying):
            if(not self.maskFeedBitmap is None):
                dc = wx.BufferedPaintDC(self.dashboardMaskGalleryViewSlide.slideImagePanel)
                dc.DrawBitmap(self.maskFeedBitmap, 0, 0)

    def scaleFeed(self, tmpBmp):
        image = wx.Bitmap.ConvertToImage(tmpBmp)
        image = image.Scale(self.DashboardLiveFeedPanel.GetSize()[0], self.DashboardLiveFeedPanel.GetSize()[1], wx.IMAGE_QUALITY_HIGH)
        #self.liveFeedBitmap = wx.Bitmap(image)
        return wx.Bitmap(image)

    def updateFeed(self, event):
        if (self.LiveFeedPlaying):

            # Get Frame from source
            # rvt, self.feed = self.capture.read()

            #Get live feed from URL
            if (not self.currentLiveFeedCamera == ""):
                if (self.currentLiveFeedCamera in self.cap.keys()):
                    ret, frame = self.cap[self.currentLiveFeedCamera].read()

                    if (ret):
                        self.feed = frame
                        frame = cv2.cvtColor(self.feed, cv2.COLOR_BGR2RGB)
                        tmpBmp = wx.Bitmap.FromBuffer(frame.shape[1], frame.shape[0], frame)
                        self.liveFeedBitmap = self.scaleFeed(tmpBmp)
                    self.DashboardLiveFeedPanel.Refresh()

            # Get social distancing violation feed from URL
            if (not self.currentLiveFeedCamera == ""):
                if (self.currentLiveFeedCamera in self.cap.keys()):
                    ret, frame = self.cap[self.currentLiveFeedCamera].read()

                    if (ret):
                        self.feed = frame
                        frame = cv2.cvtColor(self.feed, cv2.COLOR_BGR2RGB)
                        tmpBmp = wx.Bitmap.FromBuffer(frame.shape[1], frame.shape[0], frame)
                        self.distancingFeedBitmap = self.scaleFeed(tmpBmp)
                    self.dashboardGalleryViewSlide.slideImagePanel.Refresh()

            # Get social distancing violation feed from URL
            if (not self.currentLiveFeedCamera == ""):
                if (self.currentLiveFeedCamera in self.cap.keys()):
                    ret, frame = self.cap[self.currentLiveFeedCamera].read()

                    if (ret):
                        self.feed = frame
                        frame = cv2.cvtColor(self.feed, cv2.COLOR_BGR2RGB)
                        tmpBmp = wx.Bitmap.FromBuffer(frame.shape[1], frame.shape[0], frame)
                        self.maskFeedBitmap = self.scaleFeed(tmpBmp)
                    self.dashboardMaskGalleryViewSlide.slideImagePanel.Refresh()
                pass

    # def go_live(self, event):
    #     if self.isLive:

import random 

# y = []
# for i in range (200):
#     y.append(random.randrange(0, 200, 1))
# x = np.arange(200)
# # y = np.random()
# plt.style.use(u'dark_background')
# fig = plt.figure()
# ax = plt.subplot(111)
# ax.plot(x, y, label='$y = numbers')
# plt.title('Legend inside')
# ax.legend()
# #plt.show()
# fig.set_size_inches(15, 5)
# fig.tight_layout()
# fig.savefig('plot.png', transparent=True)

#app = wx.App()
#window = Dashboard(None)
#app.MainLoop()


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
        cameraAliasLabel = wx.StaticText(self.panel, label="Camera ID", pos=(50, 40), size=(100, 40))
        self.cameraAliasEntry = wx.ComboBox(self.panel, pos=(180, 35), size=(200, 40))
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
