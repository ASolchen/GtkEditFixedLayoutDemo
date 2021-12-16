from os import X_OK
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
from widget_manager import WidgetManager

class App():
  def __init__(self) -> None:
    win = Gtk.Window()
    fixed = Gtk.Fixed(width_request=640, height_request=480)
    self.grid_settings = [8,8]
    widget_manager = WidgetManager(self, fixed)
    self.e_box = Gtk.EventBox(above_child=True)
    self.overlay = Gtk.Overlay()
    self.overlay_signals = []
    event_mask = Gdk.EventMask.BUTTON1_MOTION_MASK
    self.overlay.set_events(event_mask)
    self.overlay.add(fixed)
    win.add(self.overlay)
    win.show_all()
    win.set_decorated(False)
    Gtk.main()

  def grab_widget(self, widget):
    #called from the widget, asking for drag events until mouse is up
    self.overlay_signals.append(self.overlay.connect('motion-notify-event', widget.mouse_dragged))

  def let_go(self, widget):
    #widget notifies that the mouse came up, disconnect the drag event
    for handler in self.overlay_signals:
      self.overlay.disconnect(handler)
    self.overlay_signals = []

      

App()









