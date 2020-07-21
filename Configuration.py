# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Jun 17 2015)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class MyFrame1
###########################################################################

class MyFrame1 ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 1082,785 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		self.SetFont( wx.Font( 10, 70, 90, 90, False, wx.EmptyString ) )
		self.SetForegroundColour( wx.Colour( 255, 255, 255 ) )
		self.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_HIGHLIGHT ) )
		
		fgSizer1 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer1.AddGrowableCol( 1 )
		fgSizer1.AddGrowableRow( 1 )
		fgSizer1.SetFlexibleDirection( wx.BOTH )
		fgSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_bpButton61 = wx.BitmapButton( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.Size( -1,-1 ), wx.BU_AUTODRAW )
		fgSizer1.Add( self.m_bpButton61, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
		
		self.m_staticText1 = wx.StaticText( self, wx.ID_ANY, u"Configuration", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1.Wrap( -1 )
		self.m_staticText1.SetFont( wx.Font( 20, 70, 90, 90, False, wx.EmptyString ) )
		self.m_staticText1.SetForegroundColour( wx.Colour( 255, 255, 255 ) )
		
		fgSizer1.Add( self.m_staticText1, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
		
		fgSizer3 = wx.FlexGridSizer( 0, 1, 0, 0 )
		fgSizer3.AddGrowableRow( 0 )
		fgSizer3.SetFlexibleDirection( wx.BOTH )
		fgSizer3.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		bSizer4 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_bpButton5 = wx.BitmapButton( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		bSizer4.Add( self.m_bpButton5, 0, wx.ALL, 5 )
		
		self.m_bpButton6 = wx.BitmapButton( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		bSizer4.Add( self.m_bpButton6, 0, wx.ALL, 5 )
		
		self.m_bpButton7 = wx.BitmapButton( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		
		# self.m_bpButton7.SetBitmapSelected( wx.Bitmap( u"C:\\Users\\Capture2.PNG", wx.BITMAP_TYPE_ANY ) )
		bSizer4.Add( self.m_bpButton7, 0, wx.ALL, 5 )
		
		
		fgSizer3.Add( bSizer4, 1, wx.EXPAND, 5 )
		
		bSizer5 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_bpButton8 = wx.BitmapButton( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
		bSizer5.Add( self.m_bpButton8, 0, wx.ALL, 5 )
		
		
		fgSizer3.Add( bSizer5, 1, wx.EXPAND, 5 )
		
		
		fgSizer1.Add( fgSizer3, 1, wx.EXPAND, 5 )
		
		bSizer3 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_panel1 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.m_panel1.SetBackgroundColour( wx.Colour( 255, 255, 255 ) )
		
		fgSizer31 = wx.FlexGridSizer( 0, 1, 0, 0 )
		fgSizer31.AddGrowableCol( 0 )
		fgSizer31.AddGrowableRow( 1 )
		fgSizer31.SetFlexibleDirection( wx.BOTH )
		fgSizer31.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		bSizer41 = wx.BoxSizer( wx.HORIZONTAL )
		
		fgSizer6 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer6.AddGrowableCol( 0 )
		fgSizer6.SetFlexibleDirection( wx.BOTH )
		fgSizer6.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		bSizer6 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_button1 = wx.Button( self.m_panel1, wx.ID_ANY, u"+ Add New Camera", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_button1.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 90, False, wx.EmptyString ) )
		
		bSizer6.Add( self.m_button1, 0, wx.ALL, 5 )
		
		
		fgSizer6.Add( bSizer6, 1, wx.EXPAND, 5 )
		
		bSizer7 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_button2 = wx.Button( self.m_panel1, wx.ID_ANY, u"Stop All", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_button2.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 90, False, wx.EmptyString ) )
		
		bSizer7.Add( self.m_button2, 0, wx.ALL, 5 )
		
		self.m_button3 = wx.Button( self.m_panel1, wx.ID_ANY, u"Start All", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_button3.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 90, False, wx.EmptyString ) )
		
		bSizer7.Add( self.m_button3, 0, wx.ALL, 5 )
		
		self.m_button4 = wx.Button( self.m_panel1, wx.ID_ANY, u"Save", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_button4.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 90, False, wx.EmptyString ) )
		
		bSizer7.Add( self.m_button4, 0, wx.ALL, 5 )
		
		self.m_button5 = wx.Button( self.m_panel1, wx.ID_ANY, u"Cancel", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_button5.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 90, False, wx.EmptyString ) )
		
		bSizer7.Add( self.m_button5, 0, wx.ALL, 5 )
		
		
		fgSizer6.Add( bSizer7, 1, wx.EXPAND, 5 )
		
		
		bSizer41.Add( fgSizer6, 1, wx.EXPAND, 5 )
		
		
		fgSizer31.Add( bSizer41, 1, wx.EXPAND, 5 )
		
		self.m_scrolledWindow1 = wx.ScrolledWindow( self.m_panel1, wx.ID_ANY, wx.DefaultPosition, wx.Size( -1,-1 ), wx.HSCROLL|wx.VSCROLL )
		self.m_scrolledWindow1.SetScrollRate( 5, 5 )
		self.m_scrolledWindow1.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 90, False, wx.EmptyString ) )
		
		fgSizer4 = wx.FlexGridSizer( 0, 9, 0, 0 )
		fgSizer4.AddGrowableCol( 0 )
		fgSizer4.AddGrowableCol( 1 )
		fgSizer4.AddGrowableCol( 2 )
		fgSizer4.AddGrowableCol( 3 )
		fgSizer4.AddGrowableCol( 4 )
		fgSizer4.AddGrowableCol( 5 )
		fgSizer4.AddGrowableCol( 6 )
		fgSizer4.AddGrowableCol( 7 )
		fgSizer4.AddGrowableCol( 8 )
		fgSizer4.SetFlexibleDirection( wx.BOTH )
		fgSizer4.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticText2 = wx.StaticText( self.m_scrolledWindow1, wx.ID_ANY, u"#", wx.DefaultPosition, wx.Size( -1,-1 ), 0 )
		self.m_staticText2.Wrap( -1 )
		self.m_staticText2.SetFont( wx.Font( 12, 70, 90, 90, False, wx.EmptyString ) )
		
		fgSizer4.Add( self.m_staticText2, 1, wx.ALIGN_CENTER|wx.ALL, 5 )
		
		self.m_staticText3 = wx.StaticText( self.m_scrolledWindow1, wx.ID_ANY, u"Alias", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText3.Wrap( -1 )
		self.m_staticText3.SetFont( wx.Font( 12, 70, 90, 90, False, wx.EmptyString ) )
		
		fgSizer4.Add( self.m_staticText3, 1, wx.ALIGN_CENTER|wx.ALL, 5 )
		
		self.m_staticText4 = wx.StaticText( self.m_scrolledWindow1, wx.ID_ANY, u"User-ID", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText4.Wrap( -1 )
		self.m_staticText4.SetFont( wx.Font( 12, 70, 90, 90, False, wx.EmptyString ) )
		
		fgSizer4.Add( self.m_staticText4, 1, wx.ALIGN_CENTER|wx.ALL, 5 )
		
		self.m_staticText5 = wx.StaticText( self.m_scrolledWindow1, wx.ID_ANY, u"Cam IP Address", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText5.Wrap( -1 )
		self.m_staticText5.SetFont( wx.Font( 12, 70, 90, 90, False, wx.EmptyString ) )
		
		fgSizer4.Add( self.m_staticText5, 2, wx.ALIGN_CENTER|wx.ALL, 5 )
		
		self.m_staticText6 = wx.StaticText( self.m_scrolledWindow1, wx.ID_ANY, u"Password", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText6.Wrap( -1 )
		self.m_staticText6.SetFont( wx.Font( 12, 70, 90, 90, False, wx.EmptyString ) )
		
		fgSizer4.Add( self.m_staticText6, 2, wx.ALIGN_CENTER|wx.ALL, 5 )
		
		self.m_staticText7 = wx.StaticText( self.m_scrolledWindow1, wx.ID_ANY, u"Edit", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText7.Wrap( -1 )
		self.m_staticText7.SetFont( wx.Font( 12, 70, 90, 90, False, wx.EmptyString ) )
		
		fgSizer4.Add( self.m_staticText7, 2, wx.ALIGN_CENTER|wx.ALL, 5 )
		
		self.m_staticText8 = wx.StaticText( self.m_scrolledWindow1, wx.ID_ANY, u"Status", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText8.Wrap( -1 )
		self.m_staticText8.SetFont( wx.Font( 12, 70, 90, 90, False, wx.EmptyString ) )
		
		fgSizer4.Add( self.m_staticText8, 2, wx.ALIGN_CENTER|wx.ALL, 5 )
		
		self.m_staticText9 = wx.StaticText( self.m_scrolledWindow1, wx.ID_ANY, u"Control", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText9.Wrap( -1 )
		self.m_staticText9.SetFont( wx.Font( 12, 70, 90, 90, False, wx.EmptyString ) )
		
		fgSizer4.Add( self.m_staticText9, 2, wx.ALIGN_CENTER|wx.ALL, 5 )
		
		self.m_staticText10 = wx.StaticText( self.m_scrolledWindow1, wx.ID_ANY, u"Configure", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText10.Wrap( -1 )
		self.m_staticText10.SetFont( wx.Font( 12, 70, 90, 90, False, wx.EmptyString ) )
		
		fgSizer4.Add( self.m_staticText10, 2, wx.ALIGN_CENTER|wx.ALL, 5 )
		
		self.m_textCtrl1 = wx.TextCtrl( self.m_scrolledWindow1, wx.ID_ANY, u"10", wx.DefaultPosition, wx.Size( -1,-1 ), 0 )
		self.m_textCtrl1.SetFont( wx.Font( 12, 70, 90, 90, False, wx.EmptyString ) )
		self.m_textCtrl1.SetMinSize( wx.Size( 35,-1 ) )
		
		fgSizer4.Add( self.m_textCtrl1, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_textCtrl2 = wx.TextCtrl( self.m_scrolledWindow1, wx.ID_ANY, u"Main Gate", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_textCtrl2.SetFont( wx.Font( 12, 70, 90, 90, False, wx.EmptyString ) )
		self.m_textCtrl2.SetMinSize( wx.Size( 120,-1 ) )
		self.m_textCtrl2.SetMaxSize( wx.Size( 150,-1 ) )
		
		fgSizer4.Add( self.m_textCtrl2, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_textCtrl3 = wx.TextCtrl( self.m_scrolledWindow1, wx.ID_ANY, u"admin", wx.DefaultPosition, wx.Size( -1,-1 ), 0 )
		self.m_textCtrl3.SetFont( wx.Font( 12, 70, 90, 90, False, wx.EmptyString ) )
		
		fgSizer4.Add( self.m_textCtrl3, 0, wx.ALL|wx.EXPAND|wx.RIGHT, 5 )
		
		self.m_textCtrl4 = wx.TextCtrl( self.m_scrolledWindow1, wx.ID_ANY, u"192.168.0.100", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_textCtrl4.SetFont( wx.Font( 12, 70, 90, 90, False, wx.EmptyString ) )
		self.m_textCtrl4.SetMinSize( wx.Size( 150,-1 ) )
		
		fgSizer4.Add( self.m_textCtrl4, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_textCtrl5 = wx.TextCtrl( self.m_scrolledWindow1, wx.ID_ANY, u"Shrinivas", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_textCtrl5.SetFont( wx.Font( 12, 70, 90, 90, False, wx.EmptyString ) )
		self.m_textCtrl5.SetMinSize( wx.Size( 150,-1 ) )
		
		fgSizer4.Add( self.m_textCtrl5, 0, wx.ALL|wx.EXPAND, 5 )
		
		bSizer51 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_button81 = wx.Button( self.m_scrolledWindow1, wx.ID_ANY, u"Edit", wx.DefaultPosition, wx.Size( -1,34 ), 0 )
		bSizer51.Add( self.m_button81, 0, wx.ALL|wx.EXPAND, 5 )
		
		
		fgSizer4.Add( bSizer51, 1, wx.EXPAND, 0 )
		
		self.m_radioBtn1 = wx.RadioButton( self.m_scrolledWindow1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer4.Add( self.m_radioBtn1, 0, wx.ALIGN_CENTER|wx.ALL, 0 )
		
		self.m_textCtrl8 = wx.TextCtrl( self.m_scrolledWindow1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( -1,40 ), 0 )
		self.m_textCtrl8.SetMinSize( wx.Size( 80,-1 ) )
		
		fgSizer4.Add( self.m_textCtrl8, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_button8 = wx.Button( self.m_scrolledWindow1, wx.ID_ANY, u"Configure", wx.DefaultPosition, wx.Size( -1,34 ), 0 )
		fgSizer4.Add( self.m_button8, 0, wx.ALL|wx.EXPAND, 5 )
		
		
		self.m_scrolledWindow1.SetSizer( fgSizer4 )
		self.m_scrolledWindow1.Layout()
		fgSizer4.Fit( self.m_scrolledWindow1 )
		fgSizer31.Add( self.m_scrolledWindow1, 1, wx.ALIGN_TOP|wx.ALL|wx.EXPAND, 5 )
		
		
		self.m_panel1.SetSizer( fgSizer31 )
		self.m_panel1.Layout()
		fgSizer31.Fit( self.m_panel1 )
		bSizer3.Add( self.m_panel1, 1, wx.EXPAND |wx.ALL, 0 )
		
		
		fgSizer1.Add( bSizer3, 1, wx.EXPAND, 5 )
		
		
		self.SetSizer( fgSizer1 )
		self.Layout()
		
		self.Centre( wx.BOTH )
	
	def __del__( self ):
		pass
	
class MyApp(wx.App):
    def OnInit(self):
        self.frame=MyFrame1(None)
        self.frame.Show()

        return True

app=MyApp()
app.MainLoop()
