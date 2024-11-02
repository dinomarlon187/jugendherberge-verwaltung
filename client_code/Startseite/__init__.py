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
    
    self.hostel_id_index_relation = [] # [INDEX/ID] 
    self.user_id_index_relation = []
    self.price_id_index_relation = []
    self.room_id_index_relation = []
    self.extra_user_index = []
    self.init_components(**properties)
    self.loading_data()

    self.dropdown_user.items = anvil.server.call('get_all_users')
    # self.dropdown_preiskategorie.items = anvil.server.call('get_preiskategorien', self.dropdown_user.)
    self.dropdown_zimmer.items = anvil.server.call('get_zimmer_for_jugendherberge',self.dropdown_jugendhergerge.selected_value, self.dropdown_preiskategorie.selected_value)
    # self.dropdown_user.items = anvil.server.call('get_benutzer', 'Vorname,Nachname,Email')
    # self.dropdown_preiskategorie.items = anvil.server.call('get_preiskategorien_for_user', 'Preis')

  def dropdown_jugendherberge_change(self, **event_args):
    """This method is called when an item is selected"""
    pass

  def dropdown_user_change(self, **event_args):
    """This method is called when an item is selected"""
    pass

  def dropdown_preiskategorie_change(self, **event_args):
    """This method is called when an item is selected"""
    pass


  def data_modify(self, data):
    data_list = []
    relation = []
    count = 0
    for i in data:
      data_list.append([i[0],count]) # i[0] the Name  COUNT is the index in the dropdown
      relation.append([count, i[1]]) # i [1] the ID  COUNT is the index in the dropdown
      count +=1
    return [data_list, relation]

  def transform_index_to_id(self, data, index):
    for i in data:
      if index == i[0]:
        return i[1]
 
  def loading_data(self):
    self.load_Jugendherbergen()
    self.load_user(self.user_dropdown)
    self.load_user(self.extra_user_dropdown)
    self.load_price()
    self.load_room()
    self.display_booking()

  def load_Jugendherbergen(self):
    data_list = anvil.server.call('get_jugendherbergen')
    data_modify = self.data_modify(data_list)
    self.hostel_id_index_relation = data_modify[1]
    self.dropdown_jugendherberge.items = data_modify[0]




