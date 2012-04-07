import wx
import bid
import threadspawner
import time
import cProfile

#graph imports
import matplotlib
matplotlib.interactive( False )
matplotlib.use( 'WXAgg' )
import numpy as np
import wx
import wx.lib.scrolledpanel
import matplotlib.pyplot as plt
import math
plt.ioff()

class MyApp(wx.App):
  thread = None
#launcher bit to read in variables
class MyFrame(wx.Frame):

  def __init__(self,app):
    self.app = app
    wx.Frame.__init__(self, None, wx.ID_ANY, "Awesome Settings!!", pos=(150,150), size=(400, 300))
    self.panel = wx.Panel(self, wx.ID_ANY)
    self.advanced=False
#text boxes and and labeling
    self.label1 = wx.StaticText(self.panel, label="Port:", pos=(10,10))
    self.port = wx.TextCtrl(self.panel, pos=(10,30), value="4000")
    self.label2 = wx.StaticText(self.panel, label="Shares:", pos=(10,60))
    self.shares = wx.TextCtrl(self.panel, pos=(10,80), value="10000")
    self.label3 = wx.StaticText(self.panel, label="Min Price:", pos=(10,110))
    self.pmin = wx.TextCtrl(self.panel, pos=(10,130), value="1")
    self.label4 = wx.StaticText(self.panel, label="Max Price:", pos=(10,160))
    self.pmax = wx.TextCtrl(self.panel, pos=(10,180), value="1000")

#adv options boxes and hiding them
    self.label5 = wx.StaticText(self.panel, label="Username:", pos=(120,10))
    self.user = wx.TextCtrl(self.panel, pos=(120,30), value="dutch")
    self.label6 = wx.StaticText(self.panel, label="Password:", pos=(120,60))
    self.password = wx.TextCtrl(self.panel, pos=(120,80), value="godm0d3")
    self.label7 = wx.StaticText(self.panel, label="Database:", pos=(120,110))
    self.db = wx.TextCtrl(self.panel, pos=(120,130), value="dutchipo")
    self.advanced=False
    self.label5.Hide()
    self.user.Hide()
    self.label6.Hide()
    self.password.Hide()
    self.label7.Hide()
    self.db.Hide()

#button and event setting
    self.button1 = wx.Button(self.panel, id=wx.ID_ANY, label="Go!", pos=(10,220))
    self.button1.Bind(wx.EVT_BUTTON, self.onButton)
    self.button2 = wx.Button(self.panel, id=wx.ID_ANY, label="More...", pos=(120,220))
    self.button2.Bind(wx.EVT_BUTTON, self.advButton)
    self.port.Bind(wx.EVT_KEY_DOWN, self.onKeyPress)
    self.shares.Bind(wx.EVT_KEY_DOWN, self.onKeyPress)
    self.pmin.Bind(wx.EVT_KEY_DOWN, self.onKeyPress)
    self.pmax.Bind(wx.EVT_KEY_DOWN, self.onKeyPress)

#cursor into windows    
    self.port.SetFocus()

#start listening etc by button enter
  def onKeyPress(self, event):
    keycode = event.GetKeyCode()
    if keycode == wx.WXK_RETURN:
      self.onButton(None)
    event.Skip()

  def onButton(self, event):
    bid.Bid.shares=int(self.shares.GetValue())
    bid.Bid.pmin=int(self.pmin.GetValue())
    bid.Bid.pmax=int(self.pmax.GetValue())
    self.app.thread = threadspawner.threadspawner(int(self.port.GetValue()),self.user.GetValue(),self.password.GetValue(),self.db.GetValue())
    self.app.thread.start()
    monitor(None, "Graphomatic Command Center Plus", app).Show()
    self.Close()

#db settings
  def advButton(self, event):
    if self.advanced==False:
      self.label5.Show()
      self.user.Show()
      self.label6.Show()
      self.password.Show()
      self.label7.Show()
      self.db.Show()
      self.advanced=True
      self.button2.SetLabel("Less...")
    else:
      self.advanced=False
      self.label5.Hide()
      self.user.Hide()
      self.label6.Hide()
      self.password.Hide()
      self.label7.Hide()
      self.db.Hide()
      self.button2.SetLabel("More...")
#ugly graph to wx code

class PlotPanel (wx.Panel):
  """The PlotPanel has a Figure and a Canvas. OnSize events simply set a 
flag, and the actual resizing of the figure is triggered by an Idle event."""

  def __init__( self, parent, color=None, dpi=None, **kwargs ):
    from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg
    from matplotlib.figure import Figure

    # initialize Panel
    if 'id' not in kwargs.keys():
      kwargs['id'] = wx.ID_ANY
    if 'style' not in kwargs.keys():
      kwargs['style'] = wx.NO_FULL_REPAINT_ON_RESIZE
    wx.Panel.__init__( self, parent, **kwargs )

    # initialize matplotlib stuff
    self.figure = Figure( None, dpi )
    self.canvas = FigureCanvasWxAgg( self, 1, self.figure )
    self.SetColor( color )

    self._SetSize()
    self.draw()

    self._resizeflag = False

    self.Bind(wx.EVT_IDLE, self._onIdle)
    self.Bind(wx.EVT_SIZE, self._onSize)


  def SetColor( self, rgbtuple=None ):
    """Set figure and canvas colours to be the same."""
    if rgbtuple is None:
      rgbtuple = wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNFACE ).Get()
    clr = [c/255. for c in rgbtuple]
    self.figure.set_facecolor( clr )
    self.figure.set_edgecolor( clr )
 #   self.canvas.SetBackgroundColour( wx.Colour( *rgbtuple ) )

  def _onSize( self, event ):
    self._resizeflag = True

  def _onIdle( self, evt ):
    if self._resizeflag:
      self._resizeflag = False
      self._SetSize()

  def _SetSize( self ):
    pixels = tuple( self.parent.GetClientSize() )
    self.SetSize( pixels )
    self.canvas.SetSize( pixels )
    self.figure.set_size_inches( float( pixels[0] *1/2)/self.figure.get_dpi(),
                   float( pixels[1]*3/4 )/self.figure.get_dpi() )

  def draw(self): pass # abstract, to be overridden by child classes

#part2
class monitor(wx.Frame):
  def __init__(self, parent, title, app):
    self.app = app
    self.dirname=''
    wx.Frame.__init__(self, parent, title=title, size=(1200,600))
    self.quote = wx.StaticText(self, label="The 5 most recent bids were:\n\n\n\n\n\n\n{0}".format(self.recent()) )
    tup=self.app.thread.dataset.sumPrices()
    self.panel = DemoPlotPanel(self,len(tup[0]),tup[0],tup[1])
    self.idle = 0

#subsection layout
    self.sizer2 = wx.BoxSizer(wx.VERTICAL)
    self.sizer2.Add(self.quote, 0, wx.EXPAND)
    self.sizer2.Add(self.panel,1,wx.EXPAND)
    self.sizer3 = wx.BoxSizer(wx.VERTICAL)

#page layout
    self.sizer = wx.BoxSizer(wx.HORIZONTAL)
    self.sizer.Add(self.sizer3, 1, wx.EXPAND)
    self.sizer.Add(self.sizer2, 1, wx.EXPAND)
    self.SetSizer(self.sizer)
    self.SetAutoLayout(1)
    self.Bind(wx.EVT_IDLE, self.OnIdle)

#scrolling
    self.examine = wx.lib.scrolledpanel.ScrolledPanel(self, -1, size=(0,self.GetSize()[1]))
    self.examine.SetupScrolling()
#    self.examine.SetScrollbars(0, 1, 0, 400)
    self.sizer4 = wx.BoxSizer(wx.VERTICAL)
    self.examine.SetSizer(self.sizer4)
    self.sizer3.Add(self.examine,0,wx.EXPAND)

    self.thingies = []
    self.lists()
    self.dive = True

  def lists(self,event=""):
    self.dive = True
    a = self.app.thread.dataset.sumPrices()
    for x in self.thingies:
      x.Hide()
    self.thingies = []
    for x in range(len(a[0])):
      l = wx.StaticText(self.examine, label = "$%d | %d shares" % (a[0][x], a[1][x]), name = str(a[0][x]))
      l.Bind(wx.EVT_LEFT_DOWN, self.divedown)
      self.sizer4.Add(l,0,wx.EXPAND)
      self.thingies.append(l)
    self.sizer4.Layout()
    self.examine.SetupScrolling(scrollToTop=False)
  def OnIdle(self,event):
    if self.idle % 5 == 0:
      self.quote.Hide()
      self.quote.SetLabel("The auction is currently {0}\nThe 5 most recent bids were:\n{1}".format(("Open" if self.app.thread.dataset.closed == 0 else "Closed and the clearing price is ${0}".format(self.app.thread.dataset.clearingPrice())),self.recent()) )
      self.quote.Show()
      self.examine.SetSize((self.examine.GetSize()[0],self.GetSize()[1]))
      if self.dive:
        self.lists()
    self.idle += 1
    if self.idle == 20:
      self.idle = 0
      tup=self.app.thread.dataset.sumPrices()
      self.panel.Hide()
      self.panel.N=len(tup[0])
      self.panel.bidVals=tup[0]
      self.panel.quants=tup[1]
      self.panel.draw()
      self.panel.Show()
    event.RequestMore()
  def divedown(self,event):
    self.dive = False
    a = self.app.thread.dataset.getPrices(int(event.GetEventObject().GetName()))
    for x in self.thingies:
      x.Hide()
      x.Destroy()
    self.thingies = []
    b = wx.Button(self.examine, label= "Back")
    b.Bind(wx.EVT_BUTTON, self.lists)
    self.sizer4.Add(b,0,wx.EXPAND)
    self.thingies.append(b)
    for x in a:
      l = wx.StaticText(self.examine, label = "%s | %s, %d shares at $%d " % (time.asctime(time.localtime(float(x[0]))), x[1], x[3], x[2]))
      l.Bind(wx.EVT_LEFT_DOWN, self.lists)
      self.sizer4.Add(l,0)
      self.thingies.append(l)
    self.sizer4.Layout()
    self.examine.SetupScrolling(scrollToTop=False)     

#get string of five most recent
  def recent(self):
    return self.app.thread.dataset.fiveNewest()

#more ugly graph to wx stuff
if __name__ == '__main__':
  class DemoPlotPanel (PlotPanel):
    """Plots several lines in distinct colors."""
    def __init__( self, parent, myN, myBids, myQuants, **kwargs): # myBids and myQuants MUST BE EQUAL IN LENGTH and respective of each other
      self.parent = parent
      self.bidVals = myBids
      self.N = myN
      self.quants = myQuants

      # initiate plotter
      PlotPanel.__init__( self, parent, **kwargs )
      self.SetColor( (255,255,255) )

    def draw( self ):
      """Draw data."""
      self.subplot = self.figure.add_subplot( 111 )

      index = np.arange(self.N) # where the bars will be
      width = 0.50

      rc = self.subplot.bar(self.bidVals, self.quants, width, bottom=0, color='b', orientation='vertical', align='center')
      

app = MyApp(False)
MyFrame(app).Show(True)
app.MainLoop()

