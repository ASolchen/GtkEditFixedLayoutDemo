import gi
import random
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject

class HMI_ALIGNMENT():
  CENTER = 0
  LEFT = 1
  RIGHT = 2
  MIDDLE = 3
  TOP = 4
  BOTTOM = 5
  CENTER_MIDDLE = 6




class HMIWidget(Gtk.Box):
  """base box widget that all widgets are derived from"""
  def __init__(self, app, parent_layout) -> None:
    super().__init__()
    self.app = app
    self.parent_layout = parent_layout
    self.x = 0
    self.y = 0
    self.focused = False
    self.parent_layout.put(self, 0,0)
    self.grab_offset = [0,0]
    self.e_box = Gtk.EventBox(above_child=True)
    self.e_box.connect("button-release-event", self.mouse_up)
    self.e_box.connect("button-press-event", self.mouse_down)
    self.add(self.e_box)
    self.build()


  def move_widget(self, x ,y):
    self.parent_layout.move(self,x,y)
    self.x = x
    self.y = y

  def mouse_dragged(self, overlay, event):
    
    x = event.x_root - self.grab_offset[0]
    y = event.y_root - self.grab_offset[1]
    x = int(round(x) /self.app.grid_settings[0]) * self.app.grid_settings[0]
    y = int(round(y) /self.app.grid_settings[1]) * self.app.grid_settings[1]
    self.move_widget(x,y)
  
  def grab(self, event):
    self.grab_offset = [event.x_root - self.x, event.y_root- self.y] # where on the widget the mouse grabbed it
    self.app.grab_widget(self)

  def mouse_down(self, e_box, event):
    if event.button == 1:
      self.grab(event)
    if event.button == 3:
      print("right-click")    

  def mouse_up(self, e_box, event):
    self.app.let_go(self)

  def build(self):
    pass


class HMIButton(HMIWidget):

  def build(self):
    self.base_widget = Gtk.Button(label="HMI Button",
                                  width_request=64,
                                  height_request=48)
    self.e_box.add(self.base_widget)




class WidgetManager(object):
  def __init__(self, app, layout) -> None:
    super().__init__()
    self.app = app
    self.layout = layout
    self.btns = []
    for x in range(10):
      btn = HMIButton(app, layout)
      self.btns.append(btn)
    btn_box = Gtk.Box()
    layout.put(btn_box,0,0)
    for idx, label in enumerate(["Center", "Left", "Right", "Middle", "Top", "Bottom", "Center-Middle"]):
      btn = Gtk.Button(label=label)
      btn.connect("clicked", self.align_test, idx)
      btn_box.pack_start(btn,0,0,1)
    self.btns[0].move_widget(300,300)
    self.btns[0].base_widget.set_property("label", "Master")



  def align_test(self, btn, alignment):
    self.align(self.btns, alignment)

  def align(self, widgets, align_by=HMI_ALIGNMENT.CENTER):
    """list of widgets to align. the first is the master template"""
    if not len(widgets) > 1:
      return
    master = widgets[0].get_allocation() # only need the master's rectangle
    widgets = [(w, w.get_allocation()) for w in widgets[1:]] # generat a list of widgets and their rectangle
    if align_by == HMI_ALIGNMENT.CENTER:
      center = master.x + (master.width / 2)
      for w, rect in widgets:
        w.move_widget(center - (rect.width / 2), w.y)
    if align_by == HMI_ALIGNMENT.LEFT:
      for w, rect in widgets:
        w.move_widget(master.x, w.y)
    if align_by == HMI_ALIGNMENT.RIGHT:
      right = master.x+master.width
      for w, rect in widgets:
        w.move_widget(right-rect.width, w.y)
    if align_by == HMI_ALIGNMENT.MIDDLE:
      center = master.y+(master.height / 2)
      for w, rect in widgets:
        w.move_widget(w.x, center - (rect.height / 2))
    if align_by == HMI_ALIGNMENT.TOP:
      for w, rect in widgets:
        w.move_widget(w.x, master.y)
    if align_by == HMI_ALIGNMENT.BOTTOM:
      bottom = master.y+master.height
      for w, rect in widgets:
        w.move_widget(w.x, bottom-rect.height)
    if align_by == HMI_ALIGNMENT.CENTER_MIDDLE:
      center_x = master.x + (master.width / 2)
      center_y = master.y + (master.height / 2)
      for w, rect in widgets:
        w.move_widget(center_x - (rect.width / 2), center_y - (rect.height / 2))

