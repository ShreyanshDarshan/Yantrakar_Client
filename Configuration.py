import wx
import wx.xrc
import json
import os
from os import path
import wx.lib.platebtn as plateButtons

class MyFrame1 ( wx.Panel ):
    
    def __init__( self, parent ):
        #wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 1182,785 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.Size(1182, 785))

        self.parent = parent


        self.refreshrate = 1000
        self.timer = wx.Timer(self)
        self.timer.Start(self.refreshrate)
        self.Bind(wx.EVT_TIMER, self.checkUpdate)

        self.oldUpdateIndex = 0
        self.newUpdateIndex = 0

        self.darkOrange = wx.Colour(255, 191, 0)
        self.lightOrange = wx.Colour(248, 217, 122)
        self.darkGrey = wx.Colour(50, 50, 50)
        self.Grey = wx.Colour(70, 70, 70)
        self.lightGrey = wx.Colour(100, 100, 100)
        self.faintWhite = wx.Colour(200, 200, 200)
        self.white = wx.Colour(255, 255, 255)
        self.slightlyLightGrey = wx.Colour(80, 80, 80)
        self.fontNormal = wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        self.fontBold = wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)

        self.lastCameraIndex="01"
        self.didUpdate=False
        
        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
        #self.SetFont( wx.Font( 10, 70, 90, 90, False, wx.EmptyString ) )
        self.SetForegroundColour(self.white)
        self.SetBackgroundColour( self.darkGrey )

        LayoutMain = wx.BoxSizer(wx.HORIZONTAL)

        self.configurationPanel = wx.ScrolledWindow(self, pos=wx.DefaultPosition, size=wx.DefaultSize,
                                                  style=wx.VSCROLL | wx.HSCROLL)
        self.configurationPanel.SetScrollRate(5, 5)

        #LayoutMain.Add(self.navPanel, proportion=0, flag=wx.EXPAND | wx.ALL, border=0)
        LayoutMain.Add(self.configurationPanel, proportion=1, flag=wx.EXPAND | wx.ALL, border=0)

        self.SetSizer(LayoutMain)
        self.Layout()

        LayoutConfigurationPanel = wx.BoxSizer(wx.VERTICAL)

        self.configurationPanelHeadPanel = wx.Panel(self.configurationPanel, -1)
        self.configurationPanelHeadPanel.SetBackgroundColour(self.darkGrey)

        LayoutHeadPanel = wx.BoxSizer(wx.VERTICAL)

        self.configurationPanelHeading = wx.StaticText(self.configurationPanelHeadPanel, -1, "CONFIGURATION")
        self.configurationPanelHeading.SetForegroundColour(self.white)
        self.configurationPanelHeading.SetFont(self.fontBold)

        LayoutHeadPanel.Add(self.configurationPanelHeading, proportion=1, flag=wx.ALIGN_CENTER | wx.ALL, border=15)

        self.configurationPanelHeadPanel.SetSizer(LayoutHeadPanel)
        LayoutHeadPanel.Fit(self.configurationPanelHeadPanel)

        self.configurationMainPanel = wx.Panel(self.configurationPanel, -1)
        self.configurationMainPanel.SetBackgroundColour(self.Grey)

        LayoutConfigurationPanel.Add(self.configurationPanelHeadPanel, proportion=0, flag=wx.EXPAND | wx.ALL, border=0)
        LayoutConfigurationPanel.Add(self.configurationMainPanel, proportion=1, flag=wx.EXPAND | wx.ALL, border=0)

        self.configurationPanel.SetSizer(LayoutConfigurationPanel)
        LayoutConfigurationPanel.Fit(self.configurationPanel)
        
        bSizer3 = wx.BoxSizer( wx.VERTICAL )
        #Central Panel
        self.m_panel1 = wx.Panel( self.configurationMainPanel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        self.m_panel1.SetBackgroundColour( self.Grey )
        
        #Central FlexGrid (1 Column)
        fgSizer31 = wx.FlexGridSizer( 0, 1, 0, 0 )
        fgSizer31.AddGrowableCol( 0 )
        fgSizer31.AddGrowableRow( 1 )
        fgSizer31.SetFlexibleDirection( wx.BOTH )
        fgSizer31.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
        
        #Configuration Control Buttons
        bSizer41 = wx.BoxSizer( wx.HORIZONTAL )
        #The FlexGrid Sizer to get Add New Button to one side
        fgSizer6 = wx.FlexGridSizer( 0, 2, 0, 0 )
        fgSizer6.AddGrowableCol( 0 )
        fgSizer6.SetFlexibleDirection( wx.BOTH )
        fgSizer6.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
        
        bSizer6 = wx.BoxSizer( wx.HORIZONTAL )
        
        self.numberOfCamera=1

        self.m_button1 = wx.Button( self.m_panel1, wx.ID_ANY, u"+ Add New Camera", wx.DefaultPosition, wx.Size( -1,40 ), wx.BU_AUTODRAW | wx.BORDER_NONE)
        self.m_button1.SetFont( wx.Font( 12, 70, 90, 90, False, wx.EmptyString ) )
        self.m_button1.Bind(wx.EVT_BUTTON,lambda evt: (
                self.addNewCamera(evt,fgSizer4,self.m_scrolledWindow1)
            ))
        self.m_button1.SetForegroundColour(self.white)
        self.m_button1.SetBackgroundColour(self.darkGrey)
        self.m_button1.Bind(wx.EVT_ENTER_WINDOW,lambda evt:  self.changeColor(evt, self.slightlyLightGrey))
        self.m_button1.Bind(wx.EVT_LEAVE_WINDOW,lambda evt:  self.changeColor(evt, self.darkGrey))
        self.m_button1.Bind(wx.EVT_LEFT_DOWN, lambda evt:  self.changeColor(evt, self.lightGrey))
        self.m_button1.Bind(wx.EVT_LEFT_UP, lambda evt:  self.changeColor(evt, self.slightlyLightGrey))
        
        bSizer6.Add( self.m_button1, 0, wx.ALL, 5 )
        
        
        fgSizer6.Add( bSizer6, 1, wx.EXPAND, 5 )
        
        bSizer7 = wx.BoxSizer( wx.HORIZONTAL )
        
        self.m_button2 = wx.Button( self.m_panel1, wx.ID_ANY, u"Stop All", wx.DefaultPosition, wx.Size( -1,40 ), wx.BU_AUTODRAW | wx.BORDER_NONE)
        self.m_button2.SetFont( wx.Font( 12, 70, 90, 90, False, wx.EmptyString ) )
        self.m_button2.Bind(wx.EVT_BUTTON,lambda evt: self.stopAll(evt,fgSizer4))
        self.m_button2.SetForegroundColour(self.white)
        self.m_button2.SetBackgroundColour(self.darkGrey)
        self.m_button2.Bind(wx.EVT_ENTER_WINDOW,lambda evt:  self.changeColor(evt, self.slightlyLightGrey))
        self.m_button2.Bind(wx.EVT_LEAVE_WINDOW,lambda evt:  self.changeColor(evt, self.darkGrey))
        self.m_button2.Bind(wx.EVT_LEFT_DOWN, lambda evt:  self.changeColor(evt, self.lightGrey))
        self.m_button2.Bind(wx.EVT_LEFT_UP, lambda evt:  self.changeColor(evt, self.slightlyLightGrey))
        
        bSizer7.Add( self.m_button2, 0, wx.ALL, 5 )
        
        self.m_button3 = wx.Button( self.m_panel1, wx.ID_ANY, u"Start All", wx.DefaultPosition, wx.Size( -1,40 ), wx.BU_AUTODRAW | wx.BORDER_NONE)
        self.m_button3.SetFont( wx.Font( 12, 70, 90, 90, False, wx.EmptyString ) )
        self.m_button3.Bind(wx.EVT_BUTTON,lambda evt: self.startAll(evt,fgSizer4))
        self.m_button3.SetForegroundColour(self.white)
        self.m_button3.SetBackgroundColour(self.darkGrey)
        self.m_button3.Bind(wx.EVT_ENTER_WINDOW,lambda evt:  self.changeColor(evt, self.slightlyLightGrey))
        self.m_button3.Bind(wx.EVT_LEAVE_WINDOW,lambda evt:  self.changeColor(evt, self.darkGrey))
        self.m_button3.Bind(wx.EVT_LEFT_DOWN, lambda evt:  self.changeColor(evt, self.lightGrey))
        self.m_button3.Bind(wx.EVT_LEFT_UP, lambda evt:  self.changeColor(evt, self.slightlyLightGrey))

        bSizer7.Add( self.m_button3, 0, wx.ALL, 5 )
        
        fgSizer6.Add( bSizer7, 1, wx.EXPAND, 5 )
        
        
        bSizer41.Add( fgSizer6, 1, wx.EXPAND, 5 )
        
        
        fgSizer31.Add( bSizer41, 1, wx.EXPAND, 5 )
        #The Table scroll window
        self.m_scrolledWindow1 = wx.ScrolledWindow( self.m_panel1, wx.ID_ANY, wx.DefaultPosition, wx.Size( -1,-1 ), wx.HSCROLL|wx.VSCROLL )
        self.m_scrolledWindow1.SetScrollRate( 5, 5 )
        self.m_scrolledWindow1.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 90, False, wx.EmptyString ) )
        #The Column Setup
        fgSizer4 = wx.FlexGridSizer( 0, 11, 0, 0 )
        fgSizer4.AddGrowableCol( 0 )
        fgSizer4.AddGrowableCol( 1 )
        fgSizer4.AddGrowableCol( 2 )
        fgSizer4.AddGrowableCol( 3 )
        fgSizer4.AddGrowableCol( 4 )
        fgSizer4.AddGrowableCol( 5 )
        fgSizer4.AddGrowableCol( 6 )
        fgSizer4.AddGrowableCol( 7 )
        fgSizer4.AddGrowableCol( 8 )
        fgSizer4.AddGrowableCol( 9 )
        fgSizer4.AddGrowableCol( 10 )
        fgSizer4.SetFlexibleDirection( wx.BOTH )
        fgSizer4.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
        
        #The Title Row in Table
        self.m_staticText2 = wx.StaticText( self.m_scrolledWindow1, wx.ID_ANY, u"#", wx.DefaultPosition, wx.Size( -1,-1 ), 0 )
        self.m_staticText2.Wrap( -1 )
        self.m_staticText2.SetFont( wx.Font( 12, 70, 90, 90, False, wx.EmptyString ) )
        self.m_staticText2.SetForegroundColour(self.faintWhite)
        
        fgSizer4.Add( self.m_staticText2, 1, wx.ALIGN_CENTER|wx.ALL, 5 )
        
        self.m_staticText2 = wx.StaticText( self.m_scrolledWindow1, wx.ID_ANY, u"Camera Key", wx.DefaultPosition, wx.Size( -1,-1 ), 0 )
        self.m_staticText2.Wrap( -1 )
        self.m_staticText2.SetFont( wx.Font( 12, 70, 90, 90, False, wx.EmptyString ) )
        self.m_staticText2.SetForegroundColour(self.faintWhite)

        fgSizer4.Add( self.m_staticText2, 1, wx.ALIGN_CENTER|wx.ALL, 5 )
        
        self.m_staticText3 = wx.StaticText( self.m_scrolledWindow1, wx.ID_ANY, u"Alias", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText3.Wrap( -1 )
        self.m_staticText3.SetFont( wx.Font( 12, 70, 90, 90, False, wx.EmptyString ) )
        self.m_staticText3.SetForegroundColour(self.faintWhite)
        
        fgSizer4.Add( self.m_staticText3, 1, wx.ALIGN_CENTER|wx.ALL, 5 )
        
        self.m_staticText4 = wx.StaticText( self.m_scrolledWindow1, wx.ID_ANY, u"Camera-ID", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText4.Wrap( -1 )
        self.m_staticText4.SetFont( wx.Font( 12, 70, 90, 90, False, wx.EmptyString ) )
        self.m_staticText4.SetForegroundColour(self.faintWhite)
        
        fgSizer4.Add( self.m_staticText4, 1, wx.ALIGN_CENTER|wx.ALL, 5 )
        
        self.m_staticText5 = wx.StaticText( self.m_scrolledWindow1, wx.ID_ANY, u"Cam IP Address", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText5.Wrap( -1 )
        self.m_staticText5.SetFont( wx.Font( 12, 70, 90, 90, False, wx.EmptyString ) )
        self.m_staticText5.SetForegroundColour(self.faintWhite)
        
        fgSizer4.Add( self.m_staticText5, 2, wx.ALIGN_CENTER|wx.ALL, 5 )
        
        self.m_staticText6 = wx.StaticText( self.m_scrolledWindow1, wx.ID_ANY, u"Password", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText6.Wrap( -1 )
        self.m_staticText6.SetFont( wx.Font( 12, 70, 90, 90, False, wx.EmptyString ) )
        self.m_staticText6.SetForegroundColour(self.faintWhite)
        
        fgSizer4.Add( self.m_staticText6, 2, wx.ALIGN_CENTER|wx.ALL, 5 )
        
        self.m_staticText8 = wx.StaticText( self.m_scrolledWindow1, wx.ID_ANY, u"", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText8.Wrap( -1 )
        self.m_staticText8.SetFont( wx.Font( 12, 70, 90, 90, False, wx.EmptyString ) )
        
        fgSizer4.Add( self.m_staticText8, 2, wx.ALIGN_CENTER|wx.ALL, 5 )
        
        self.m_staticText9 = wx.StaticText( self.m_scrolledWindow1, wx.ID_ANY, u"", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText9.Wrap( -1 )
        self.m_staticText9.SetFont( wx.Font( 12, 70, 90, 90, False, wx.EmptyString ) )
        
        fgSizer4.Add( self.m_staticText9, 2, wx.ALIGN_CENTER|wx.ALL, 5 )
        
        self.m_staticText7 = wx.StaticText( self.m_scrolledWindow1, wx.ID_ANY, u"", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText7.Wrap( -1 )
        self.m_staticText7.SetFont( wx.Font( 12, 70, 90, 90, False, wx.EmptyString ) )
        
        fgSizer4.Add( self.m_staticText7, 2, wx.ALIGN_CENTER|wx.ALL, 5 )
        
        self.m_staticText7 = wx.StaticText( self.m_scrolledWindow1, wx.ID_ANY, u"", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText7.Wrap( -1 )
        self.m_staticText7.SetFont( wx.Font( 12, 70, 90, 90, False, wx.EmptyString ) )
        
        fgSizer4.Add( self.m_staticText7, 2, wx.ALIGN_CENTER|wx.ALL, 5 )
        
        self.m_staticText10 = wx.StaticText( self.m_scrolledWindow1, wx.ID_ANY, u"", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText10.Wrap( -1 )
        self.m_staticText10.SetFont( wx.Font( 12, 70, 90, 90, False, wx.EmptyString ) )
        
        fgSizer4.Add( self.m_staticText10, 2, wx.ALIGN_CENTER|wx.ALL, 5 )
        
        #The First Input
        self.addData(fgSizer4,self.m_scrolledWindow1)
        
        self.m_scrolledWindow1.SetSizer( fgSizer4 )
        self.m_scrolledWindow1.Layout()
        fgSizer4.Fit( self.m_scrolledWindow1 )
        fgSizer31.Add( self.m_scrolledWindow1, 1, wx.ALIGN_TOP|wx.ALL|wx.EXPAND, 5 )
        
        
        self.m_panel1.SetSizer( fgSizer31 )
        self.m_panel1.Layout()
        fgSizer31.Fit( self.m_panel1 )
        bSizer3.Add( self.m_panel1, 1, wx.EXPAND |wx.ALL, 0 )
        
        self.configurationMainPanel.SetSizer(bSizer3)
        bSizer3.Fit(self.configurationMainPanel)

        self.Layout()
        #fgSizer1.Add( bSizer3, 1, wx.EXPAND, 5 )
        
        
        #self.SetSizer( fgSizer1 )
        #self.Layout()
        
        self.Centre( wx.BOTH )
    
    def __del__( self ):
        pass
    
    def stopAll(self,event,sizer):
        numberOfItems=int(len(sizer.Children)/10)
        for i in range(1,numberOfItems):
            sizer.Children[11*i+9].Window.SetBitmap(wx.Bitmap("ui_elements/play.png",wx.BITMAP_TYPE_ANY))
        
        with open('cameraDatabase.json','r') as jsonFile:
            data=json.load(jsonFile)
            for cameraData in data.values():
                cameraData["cameraStatus"]["isPaused"]=True
        with open('cameraDatabase.json','w') as jsonFile:
            json.dump(data,jsonFile,sort_keys=True, indent=4)
        
        self.sendUpdate()
        self.didUpdate=True
    
    def startAll(self,event,sizer):
        numberOfItems=int(len(sizer.Children)/10)
        for i in range(1,numberOfItems):
            sizer.Children[11*i+9].Window.SetBitmap(wx.Bitmap("ui_elements/pause.png",wx.BITMAP_TYPE_ANY))
            
        with open('cameraDatabase.json','r') as jsonFile:
            data=json.load(jsonFile)
            for cameraData in data.values():
                cameraData["cameraStatus"]["isPaused"]=False
        with open('cameraDatabase.json','w') as jsonFile:
            json.dump(data,jsonFile,sort_keys=True, indent=4)
        
        self.sendUpdate()
        self.didUpdate=True

    def makeOneRow(self,fgSizer,m_scrolledWindow1,InputData,name,canEdit,isPause,status):
        m_textCtrl0 = wx.TextCtrl( m_scrolledWindow1, wx.ID_ANY, str(self.numberOfCamera), wx.DefaultPosition, wx.Size( -1,-1 ), style=wx.BORDER_NONE | wx.TE_CENTER,name=name+"_number" )
        m_textCtrl0.SetFont( wx.Font( 12, 70, 90, 90, False, wx.EmptyString ) )
        m_textCtrl0.SetMinSize( wx.Size( 35,-1 ) )
        m_textCtrl0.SetEditable(canEdit)
        m_textCtrl0.SetBackgroundColour(self.lightGrey)
        m_textCtrl0.SetForegroundColour(self.white)
        fgSizer.Add( m_textCtrl0, 0, wx.ALL|wx.EXPAND, 5 )
        
        m_textCtrl1 = wx.TextCtrl( m_scrolledWindow1, wx.ID_ANY, InputData[0], wx.DefaultPosition, wx.Size( -1,-1 ), style= wx.BORDER_NONE | wx.TE_CENTER,name=name+"_number" )
        m_textCtrl1.SetFont( wx.Font( 12, 70, 90, 90, False, wx.EmptyString ) )
        m_textCtrl1.SetMinSize( wx.Size( 70,-1 ) )
        m_textCtrl1.SetEditable(canEdit)
        m_textCtrl1.SetBackgroundColour(self.lightGrey)
        m_textCtrl1.SetForegroundColour(self.white)
        fgSizer.Add( m_textCtrl1, 0, wx.ALL|wx.EXPAND, 5 )
        
        m_textCtrl2 = wx.TextCtrl( m_scrolledWindow1, wx.ID_ANY, InputData[1], wx.DefaultPosition, wx.DefaultSize, style=wx.BORDER_NONE | wx.TE_CENTER ,name=name+"_alias" )
        m_textCtrl2.SetFont( wx.Font( 12, 70, 90, 90, False, wx.EmptyString ) )
        m_textCtrl2.SetMinSize( wx.Size( 120,-1 ) )
        m_textCtrl2.SetMaxSize( wx.Size( 150,-1 ) )
        m_textCtrl2.SetEditable(canEdit)
        m_textCtrl2.SetBackgroundColour(self.lightGrey)
        m_textCtrl2.SetForegroundColour(self.white)
        fgSizer.Add( m_textCtrl2, 0, wx.ALL|wx.EXPAND, 5 )
        
        m_textCtrl3 = wx.TextCtrl( m_scrolledWindow1, wx.ID_ANY, InputData[2], wx.DefaultPosition, wx.Size( -1,-1 ), style=wx.BORDER_NONE | wx.TE_CENTER,name=name+"_cameraID"  )
        m_textCtrl3.SetFont( wx.Font( 12, 70, 90, 90, False, wx.EmptyString ) )
        m_textCtrl3.SetEditable(canEdit)
        m_textCtrl3.SetBackgroundColour(self.lightGrey)
        m_textCtrl3.SetForegroundColour(self.white)
        fgSizer.Add( m_textCtrl3, 0, wx.ALL|wx.EXPAND|wx.RIGHT, 5 )
        
        m_textCtrl4 = wx.TextCtrl( m_scrolledWindow1, wx.ID_ANY, InputData[3], wx.DefaultPosition, wx.DefaultSize, style=wx.BORDER_NONE | wx.TE_CENTER,name=name+"_camURL"  )
        m_textCtrl4.SetFont( wx.Font( 12, 70, 90, 90, False, wx.EmptyString ) )
        m_textCtrl4.SetMinSize( wx.Size( 150,-1 ) )
        m_textCtrl4.SetEditable(canEdit)
        m_textCtrl4.SetBackgroundColour(self.lightGrey)
        m_textCtrl4.SetForegroundColour(self.white)
        
        fgSizer.Add( m_textCtrl4, 0, wx.ALL|wx.EXPAND, 5 )
        
        m_textCtrl5 = wx.TextCtrl( m_scrolledWindow1, wx.ID_ANY, InputData[4], wx.DefaultPosition, wx.DefaultSize, style= wx.BORDER_NONE | wx.TE_CENTER,name=name+"_password"  )
        m_textCtrl5.SetFont( wx.Font( 12, 70, 90, 90, False, wx.EmptyString ) )
        m_textCtrl5.SetMinSize( wx.Size( 150,-1 ) )
        m_textCtrl5.SetEditable(canEdit)
        m_textCtrl5.SetBackgroundColour(self.lightGrey)
        m_textCtrl5.SetForegroundColour(self.white)

        fgSizer.Add( m_textCtrl5, 0, wx.ALL|wx.EXPAND, 5 )

        m_button81 = wx.Button( m_scrolledWindow1, wx.ID_ANY, InputData[5], wx.DefaultPosition, wx.Size( -1,34 ), style = wx.BORDER_NONE ,name=name+"_edit")
        m_button81.SetFont( wx.Font( 11, 70, 90, 90, False, wx.EmptyString ) )
        m_button81.name=name+"_edit"
        m_button81.Bind(wx.EVT_BUTTON,self.editButtonClick)
        m_button81.SetForegroundColour(self.faintWhite)
        m_button81.SetBackgroundColour(self.darkGrey)
        m_button81.Bind(wx.EVT_ENTER_WINDOW,lambda evt:  self.changeColor(evt, self.slightlyLightGrey))
        m_button81.Bind(wx.EVT_LEAVE_WINDOW,lambda evt:  self.changeColor(evt, self.darkGrey))
        m_button81.Bind(wx.EVT_LEFT_DOWN, lambda evt:  self.changeColor(evt, self.lightGrey))
        m_button81.Bind(wx.EVT_LEFT_UP, lambda evt:  self.changeColor(evt, self.slightlyLightGrey))
        fgSizer.Add( m_button81, 0, wx.ALL|wx.EXPAND, 5 )
        
        m_button82 = wx.Button( m_scrolledWindow1, wx.ID_ANY, u"Delete", wx.DefaultPosition, wx.Size( -1,34 ), style = wx.BORDER_NONE,name=name+"_delete")
        m_button82.SetFont( wx.Font( 11, 70, 90, 90, False, wx.EmptyString ) )
        m_button82.name=name+"_delete"
        m_button82.Bind(wx.EVT_BUTTON,lambda evt: self.deleteButtonClick(evt,fgSizer,m_scrolledWindow1))
        m_button82.SetForegroundColour(self.faintWhite)
        m_button82.SetBackgroundColour(self.darkGrey)
        m_button82.Bind(wx.EVT_ENTER_WINDOW,lambda evt:  self.changeColor(evt, self.slightlyLightGrey))
        m_button82.Bind(wx.EVT_LEAVE_WINDOW,lambda evt:  self.changeColor(evt, self.darkGrey))
        m_button82.Bind(wx.EVT_LEFT_DOWN, lambda evt:  self.changeColor(evt, self.lightGrey))
        m_button82.Bind(wx.EVT_LEFT_UP, lambda evt:  self.changeColor(evt, self.slightlyLightGrey))
        # m_button82.Bind(wx.EVT_ENTER_WINDOW, )
        fgSizer.Add( m_button82, 0, wx.ALL|wx.EXPAND, 5 )
        
        if(status==2):
            statusIcon=wx.Bitmap("ui_elements/status-green.png",wx.BITMAP_TYPE_ANY)
        elif(status==1):
            statusIcon=wx.Bitmap("ui_elements/status-yellow.png",wx.BITMAP_TYPE_ANY)
        else:
            statusIcon=wx.Bitmap("ui_elements/status-red.png",wx.BITMAP_TYPE_ANY)
        statusIcon.SetSize(wx.Size(30, 30))
        m_bpButton7 = plateButtons.PlateButton( m_scrolledWindow1, wx.ID_ANY, "", statusIcon, wx.DefaultPosition, wx.Size(43, -1), plateButtons.PB_STYLE_SQUARE,name=name+"_status" )
        m_bpButton7.SetBackgroundColour(self.lightGrey)
        m_bpButton7.SetPressColor(self.darkGrey)
        fgSizer.Add( m_bpButton7, 0, wx.ALIGN_CENTER|wx.ALL, 0 )
        
        if(isPause):
            controlIcon=wx.Bitmap("ui_elements/play.png",wx.BITMAP_TYPE_ANY)
        else:
            controlIcon=wx.Bitmap("ui_elements/pause.png",wx.BITMAP_TYPE_ANY)
        m_bpButton7 = wx.BitmapButton( m_scrolledWindow1, wx.ID_ANY, controlIcon, wx.DefaultPosition, wx.Size(43, -1) , wx.BU_AUTODRAW, name=name+"_control" )
        m_bpButton7.name=name+"_control"
        m_bpButton7.SetBackgroundColour(self.lightGrey)
        m_bpButton7.Bind(wx.EVT_BUTTON,self.controlButtonClick)
        m_bpButton7.SetForegroundColour(self.darkGrey)
        fgSizer.Add( m_bpButton7, 0, wx.ALIGN_CENTER|wx.ALL, 0 )
        
        m_button8 = wx.Button( m_scrolledWindow1, wx.ID_ANY, u"Configure", wx.DefaultPosition, wx.Size( -1,34 ), 0, name=name+"_configure" )
        m_button8.SetFont( wx.Font( 11, 70, 90, 90, False, wx.EmptyString ) )
        m_button8.Bind(wx.EVT_BUTTON, lambda evt: self.configureButtonClicked(evt, m_textCtrl2.GetValue()))
        fgSizer.Add( m_button8, 0, wx.ALL|wx.EXPAND, 5 )

    def scaleIcons(self, iconBitmap, iconSize):
        image = wx.Bitmap.ConvertToImage(iconBitmap)
        image = image.Scale(iconSize[0], iconSize[1], wx.IMAGE_QUALITY_HIGH)
        return wx.Bitmap(image)

    def configureButtonClicked(self, event, value):
        print(value)

    def controlButtonClick(self,event):
        name=event.GetEventObject().name
        cameraIndex=name[0:6]
        
        with open('cameraDatabase.json','r') as jsonFile:
            data=json.load(jsonFile)
            data[cameraIndex]["cameraStatus"]["isPaused"]=not data[cameraIndex]["cameraStatus"]["isPaused"]
        with open('cameraDatabase.json','w') as jsonFile:
            json.dump(data,jsonFile,sort_keys=True, indent=4)
        
        window= wx.FindWindowByName(name)
        if(data[cameraIndex]["cameraStatus"]["isPaused"]):
            window.SetBitmap(wx.Bitmap("ui_elements/play.png",wx.BITMAP_TYPE_ANY))
        else:
            window.SetBitmap(wx.Bitmap("ui_elements/pause.png",wx.BITMAP_TYPE_ANY))
        
        self.sendUpdate()
        self.didUpdate=True
    
    def deleteButtonClick(self,event,fgsizer,parent):
        name=event.GetEventObject().name
        cameraIndex=name[0:6]
        
        window= wx.FindWindowByName(name)
        with open('cameraDatabase.json','r') as jsonFile:
            data=json.load(jsonFile)
        
        if(window.GetLabel()=="Delete"):
            deleteIndex=int(cameraIndex[-2:])
            for i in range(0,11):
                fgsizer.Children[11*deleteIndex].Window.Destroy()
            parent.Layout()
            numberOfCamera=int(len(fgsizer.Children)/11)
            for i in range(1,numberOfCamera):
                fgsizer.Children[11*i].Window.SetValue(str(i))
            self.numberOfCamera=numberOfCamera
            self.lastCameraIndex=fgsizer.Children[11*(numberOfCamera-1)+1].Window.GetValue()
            if cameraIndex in data:
                data.pop(cameraIndex)
                with open('cameraDatabase.json','w') as jsonFile:
                    json.dump(data,jsonFile,sort_keys=True, indent=4)
            
            self.sendUpdate()
            self.didUpdate=True
        else:
            window.SetLabel("Delete")
            
            window= wx.FindWindowByName(cameraIndex+"_edit")
            window.SetLabel("Edit")

            window= wx.FindWindowByName(cameraIndex+"_alias")
            window.SetEditable(False)
            window.SetValue(data[cameraIndex]["cameraAlias"])       

            window= wx.FindWindowByName(cameraIndex+"_cameraID")
            window.SetValue(data[cameraIndex]["cameraID"])    
            window.SetEditable(False)

            window= wx.FindWindowByName(cameraIndex+"_camURL")
            window.SetValue(data[cameraIndex]["cameraIP"])    
            window.SetEditable(False)

            window= wx.FindWindowByName(cameraIndex+"_password")
            window.SetValue(data[cameraIndex]["cameraPassword"])
            window.SetEditable(False)
    
    def editButtonClick(self,event):
        name=event.GetEventObject().name
        cameraIndex=name[0:6]

        window= wx.FindWindowByName(name)
        if(window.GetLabel()=="Edit"):
            window.SetLabel("Confirm")
            
            window= wx.FindWindowByName(cameraIndex+"_delete")     
            window.SetLabel("Cancel")

            window= wx.FindWindowByName(cameraIndex+"_alias")
            window.SetEditable(True)

            window= wx.FindWindowByName(cameraIndex+"_cameraID")
            window.SetEditable(True)

            window= wx.FindWindowByName(cameraIndex+"_camURL")
            window.SetEditable(True)

            window= wx.FindWindowByName(cameraIndex+"_password")
            window.SetEditable(True)

        else:
            window.SetLabel("Edit")
            
            window= wx.FindWindowByName(cameraIndex+"_delete")     
            window.SetLabel("Delete")

            window= wx.FindWindowByName(cameraIndex+"_number")
            cameraNumber=window.GetValue()

            window= wx.FindWindowByName(cameraIndex+"_alias")
            window.SetEditable(False)
            cameraAlias=window.GetValue()

            window= wx.FindWindowByName(cameraIndex+"_cameraID")
            window.SetEditable(False)
            cameraID=window.GetValue()

            window= wx.FindWindowByName(cameraIndex+"_camURL")
            window.SetEditable(False)
            cameraIP=window.GetValue()

            window= wx.FindWindowByName(cameraIndex+"_password")
            window.SetEditable(False)
            cameraPassword=window.GetValue()
            with open('cameraDatabase.json','r') as jsonFile:
                data=json.load(jsonFile)
                data.update({
                    cameraIndex:{
                    "cameraAlias": cameraAlias,
                    "cameraID": cameraID,
                    "cameraIP": cameraIP,
                    "cameraPassword": cameraPassword,
                    "cameraStatus": {
                        "feedAvailable": False,
                        "calibAvailable": False,
                        "isPaused":True,
                    },
                    "CalibrationData": None,
                    }
                })
            with open('cameraDatabase.json','w') as jsonFile:
                json.dump(data,jsonFile,sort_keys=True, indent=4)

            self.sendUpdate()
            self.didUpdate=True
            
    def addNewCamera(self,evt,fgSizer,window):
        thisCameraIndex=self.lastCameraIndex[0:4]+str(int(self.lastCameraIndex[-2:])+1).zfill(2)
        
        self.makeOneRow(fgSizer,window,[thisCameraIndex,"","","","","Confirm"],thisCameraIndex,True,True,0)
        self.numberOfCamera=self.numberOfCamera+1
        window.Layout()
        
    def addData(self,fgSizer,window):
        with open('cameraDatabase.json','r') as jsonFile:
            data=json.load(jsonFile)
            cameras=data.items()
            for camera in cameras:
                feedAvailable=camera[1]["cameraStatus"]["feedAvailable"]
                calibAvailable=camera[1]["cameraStatus"]["calibAvailable"]
                if(feedAvailable and calibAvailable):
                    status=2
                elif(feedAvailable and not calibAvailable):
                    status=1
                else:
                    status=0
                self.makeOneRow(fgSizer,window,[camera[0],camera[1]["cameraAlias"],camera[1]["cameraID"],camera[1]["cameraIP"],camera[1]["cameraPassword"],"Edit"],camera[0],False,camera[1]["cameraStatus"]["isPaused"],status)
                self.numberOfCamera=self.numberOfCamera+1
                self.lastCameraIndex=camera[0]
    
    def changeColor(self, event, newcolor):
        event.GetEventObject().SetBackgroundColour(newcolor)

    def sendUpdate(self):
        updateFile = open("Update.txt","r")
        UpdateIndex = (updateFile.read())
        updateFile.close()
        updateFile = open("Update.txt","w")
        updateFile.write(str(UpdateIndex + 1))
        updateFile.close()

    def checkUpdate(self, event):
        if self.IsShown():
            print("checking Update")
            updateFile = open("Update.txt","r")
            self.newUpdateIndex = (updateFile.read())
            self.updateFile.close()
            if newUpdateIndex != oldUpdateIndex:
                print ("getting data")
                self.changeStatus()
            self.timer.Start(self.refreshrate)
            
    def changeStatus(self):
        with open('cameraDatabase.json','r') as jsonFile:
            data=json.load(jsonFile)
        for camera in data.items():
            feedAvailable=camera[1]["cameraStatus"]["feedAvailable"]
            calibAvailable=camera[1]["cameraStatus"]["calibAvailable"]
            if(feedAvailable and calibAvailable):
                statusIcon=wx.Bitmap("ui_elements/status-green.png",wx.BITMAP_TYPE_ANY)
            elif(feedAvailable and not calibAvailable):
                statusIcon=wx.Bitmap("ui_elements/status-yellow.png",wx.BITMAP_TYPE_ANY)
            else:
                statusIcon=wx.Bitmap("ui_elements/status-red.png",wx.BITMAP_TYPE_ANY)
            window.FindWindowByName(camera[0]+"_status")
            window.SetBitmap(statusIcon)
            

class MyApp(wx.App):
    def OnInit(self):
        self.frame=MyFrame1(None)
        # self.frame.Show()

        return True

# app=MyApp()
# app.MainLoop()
