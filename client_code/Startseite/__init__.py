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

  def dropdown_jugendherberge_change(self, **event_args):
    """This method is called when an item is selected"""
    print(self.dropdown_jugendherberge.selected_value)

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
    self.load_user(self.dropdown_user)
    self.load_user(self.dropdown_mitbucher)
    self.load_price()
    self.load_room()

  def load_Jugendherbergen(self):
    data_list = anvil.server.call('get_jugendherbergen')
    data_modify = self.data_modify(data_list)
    self.hostel_id_index_relation = data_modify[1]
    self.dropdown_jugendherberge.items = data_modify[0]
  def load_user(self, dropdown):
    data_list = anvil.server.call('get_all_users')
    data_modify = self.data_modify(data_list)
    self.user_id_index_relation = data_modify[1]
    self.dropdown_user.items = data_modify[0]

  def load_price(self):
    data_list = anvil.server.call('get_preiskategorien')
    data_modify = self.data_modify(data_list)
    self.price_id_index_relation = data_modify[1]
    self.dropdown_preiskategorie.items = data_modify[0]

  def load_room(self):
    print(self.dropdown_jugendherberge.selected_value)
    Jugendherberge_selected = self.transform_index_to_id(self.hostel_id_index_relation, self.dropdown_jugendherberge.selected_value)
    Preiskategorie_selected = self.transform_index_to_id(self.price_id_index_relation, self.dropdown_preiskategorie.selected_value)
    data_list = anvil.server.call('get_zimmer_for_jugendherberge',Jugendherberge_selected, Preiskategorie_selected)
    data_modify = self.data_modify(data_list)
    self.room_id_index_relation = data_modify[1]
    self.dropdown_zimmer.items = data_modify[0] 



