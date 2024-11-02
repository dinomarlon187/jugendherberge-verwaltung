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
    text, id = anvil.server.call('get_user', self.dropdown_mitbucher.selected_value)
    name = Link(text = str(text))
    name.icon="fa:times"
    name.icon_align="left"
    name.background="#eee"
    name.role="lozenge"
    name.border="1px solid #888"
    name.set_event_handler("click",self.delete)
    name.tag = id
    
    if text not in [component.text for component in self.flowpanel_additionalUser.get_components()]:
      self.flowpanel_additionalUser.add_component(name)
    else:
      print(f"{text} is already added.")  # Optionally, notify that the item is already added
    
  def delete(self,**k):
    print("clicked by :",k['sender'].text)
    k['sender'].remove_from_parent()

  def button_buchung_click(self, **event_args):
    if (self.date_picker_end.date == None or self.date_picker_start.date == None):
      print("Nicht alle Felder ausgefüllt")
    elif (self.date_picker_end.date == self.date_picker_start.date):
      print("Netter Versuch!")
    else:
      buchungsinfo = self.get_buchung_info()
      anvil.server.call('add_buchung',buchungsinfo)

  def date_picker_start_change(self, **event_args):
    self.date_picker_end.min_date = self.date_picker_start.date

  def get_buchung_info(self):
    userID = self.dropdown_user.selected_value
    jugendherbergeID = self.dropdown_jugendherberge.selected_value
    zimmerID = self.dropdown_zimmer.selected_value
    start_date = self.date_picker_start.date
    end_date = self.date_picker_end.date
    additional_UserID = []
    for component in self.flowpanel_additionalUser.get_components():
      additional_UserID.append(component.tag)
    return [userID,jugendherbergeID,zimmerID,start_date,end_date,additional_UserID]
    
      
      
    
  
  
  

