from ._anvil_designer import StartseiteTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server


class Startseite(StartseiteTemplate):
  
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    
    # Laden der Daten aus der Datebank + Korrelation der IDs herstellen
    
    self.dropdown_user.items = anvil.server.call('get_all_users')
    self.dropdown_jugendherberge.items = anvil.server.call('get_jugendherbergen')
    self.dropdown_preiskategorie.items = anvil.server.call('get_preiskategorien')
    self.dropdown_preiskategorie.selected_value = anvil.server.call('get_preiskategorie_for_user', self.dropdown_user.selected_value)
    self.dropdown_zimmer.items = anvil.server.call('get_zimmer_for_jugendherberge',self.dropdown_jugendherberge.selected_value, self.dropdown_preiskategorie.selected_value)
    self.dropdown_mitbucher.items = anvil.server.call('get_all_users',self.dropdown_user.selected_value)
    self.dropdown_jugendherberge.items = anvil.server.call('get_jugendherbergen')

  
  def dropdown_jugendherberge_change(self, **event_args):
    self.dropdown_zimmer.items = anvil.server.call('get_zimmer_for_jugendherberge', self.dropdown_jugendherberge.selected_value, self.dropdown_preiskategorie.selected_value)

  def dropdown_preiskategorie_change(self, **event_args):
    self.dropdown_zimmer.items = anvil.server.call('get_zimmer_for_jugendherberge', self.dropdown_jugendherberge.selected_value, self.dropdown_preiskategorie.selected_value)
    anvil.server.call('save_preiskategorie',self.dropdown_preiskategorie.selected_value, self.dropdown_user.selected_value)

  def dropdown_user_change(self, **event_args):
    pass

  def button_AddUser_click(self, **event_args):
    l = Link(text = anvil.server.call('get_user', self.dropdown_mitbucher.selected_value))
    l.icon="fa:times"
    l.icon_align="left"
    l.background="#eee"
    l.role="lozenge"
    l.border="1px solid #888"
    l.set_event_handler("click",self.delete)
    for item in self.flowpanel_additionalUser:
      if (l == item):
        return
    self.flowpanel_additionalUser.add_component(l)
    
  def delete(self,**k):
    print("clicked by :",k['sender'].text)
    k['sender'].remove_from_parent()
    
  

