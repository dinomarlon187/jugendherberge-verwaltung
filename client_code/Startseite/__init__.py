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

    # Any code you write here will run before the form opens.

    self.drop_down_1.items = anvil.server.call('get_jugendherbergen', 'name,IDJugendherberge')
    self.drop_down_2.items = anvil.server.call('get_zimmer_for_jugendherberge', 1)
    self.dropdown_User.items = anvil.server.call('get_benutzer', 'Vorname,Nachname,Email')
    self.dropdown_Preiskategorie.items = anvil.server.call('get_preiskategorien', 'Preis')
    

  def drop_down_1_change(self, **event_args):
    """This method is called when an item is selected"""
    jid = self.drop_down_1.items\
    [self.drop_down_1.selected_value - 1][1]
    self.drop_down_2.items = anvil.server.call('get_zimmer_for_jugendherberge', jid)

  def dropdown_User_change(self, **event_args):
    """This method is called when an item is selected"""
    anvil.server.call(get_Preiskategorie_User())
     
    
    
