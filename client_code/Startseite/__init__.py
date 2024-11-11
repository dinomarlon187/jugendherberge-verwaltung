from ._anvil_designer import StartseiteTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import datetime


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
    self.display_booking()
    self.dropdown_preiskategorie.selected_value = anvil.server.call('get_preiskategorie_for_user', self.dropdown_user.selected_value)
    self.date_picker_start.min_date = datetime.date.today()
    self.date_picker_end.min_date = datetime.date.today()
    
    

  
  def dropdown_jugendherberge_change(self, **event_args):
    self.dropdown_zimmer.items = anvil.server.call('get_zimmer_for_jugendherberge', self.dropdown_jugendherberge.selected_value, self.dropdown_preiskategorie.selected_value)

  def dropdown_preiskategorie_change(self, **event_args):
    self.dropdown_zimmer.items = anvil.server.call('get_zimmer_for_jugendherberge', self.dropdown_jugendherberge.selected_value, self.dropdown_preiskategorie.selected_value)
    anvil.server.call('save_preiskategorie',self.dropdown_preiskategorie.selected_value, self.dropdown_user.selected_value)

  def dropdown_user_change(self, **event_args):
    self.dropdown_preiskategorie.selected_value = anvil.server.call('get_preiskategorie_for_user', self.dropdown_user.selected_value)

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
    if text not in [component.text for component in self.flowpanel_additionalUser.get_components()] and len(self.flowpanel_additionalUser.get_components()) < anvil.server.call('get_maxBeds', int(self.dropdown_zimmer.selected_value))-1:
      self.flowpanel_additionalUser.add_component(name)
    else:
      print("Nope, geht nicht.")  
    
  def delete(self,**k):
    print("clicked by :",k['sender'].text)
    k['sender'].remove_from_parent()

  def button_buchung_click(self, **event_args):
    if (self.date_picker_end.date == None or self.date_picker_start.date == None or self.dropdown_zimmer.selected_value == None):
      print("Nicht alle Felder ausgefüllt")
    elif (anvil.server.call('check_dates',self.date_picker_start.date, self.date_picker_end.date,self.dropdown_zimmer.selected_value)):
      print("Dieses Zimmer ist zu diesem Datum schon besetzt. Bitte wähle einen anderen Zeitraum aus.")
    elif (self.date_picker_end.date == self.date_picker_start.date ):
      print("Netter Versuch!")
    else:
      buchungsinfo = self.get_buchung_info()
      anvil.server.call('add_buchung',buchungsinfo)
      self.resetAll()
      self.display_booking()

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
    
  def resetAll(self):
    for component in self.flowpanel_additionalUser.get_components():
      component.remove_from_parent()
    self.date_picker_end.date = None
    self.date_picker_start.date = None
  
  def display_booking(self):
    self.repeating_panel_1.items = None
    data = anvil.server.call('get_data')
    add_list = []
    for i in data:
      add_list.append({'column_1': i[0],'column_2': i[1], 'column_3': i[2], 'column_4': i[3], 'column_5': i[4], 'column_6': i[5],})
    self.repeating_panel_1.items = add_list
    
      
    
  
  
  

