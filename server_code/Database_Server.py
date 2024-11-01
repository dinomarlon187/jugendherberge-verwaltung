import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.files
from anvil.files import data_files
import anvil.server
import sqlite3

# This is a server module. It runs on the Anvil server,
# rather than in the user's browser.
#
# To allow anvil.server.call() to call functions here, we mark
# them with @anvil.server.callable.
# Here is an example - you can replace it with your own:
#
@anvil.server.callable
def say_hello(name):
  print("Hello, " + name + "!")
  return 42

@anvil.server.callable
def get_jugendherbergen(rows='*'):

  conn = sqlite3.connect(data_files['buchungsdatenbank.db'])
  cursor = conn.cursor()
  res = list(cursor.execute(f'SELECT {rows} FROM tblJugendherberge'))
  print(res)
  return res

@anvil.server.callable
def get_zimmer_for_jugendherberge(id, columns="MaxBettenanzahl,fkPreiskategorie"):
  conn = sqlite3.connect(data_files['buchungsdatenbank.db'])
  cursor = conn.cursor()
  res = list(cursor.execute(f'SELECT {columns} FROM tblZimmer WHERE fkJugendherberge = {id}'))

  item_list = []
  tmp_idx = 1
  for item in res:
    preis = list(cursor.execute(f'SELECT Preis FROM tblPreiskategorie WHERE IDPreiskategorie = {item[1]}'))
    label = f"Zimmer mit {item[0]} Betten, Preis: {preis[0][0]}€"
    tmp_tuple = (label,tmp_idx)
    item_list.append(tmp_tuple)
    tmp_idx += 1
  
  return item_list

@anvil.server.callable
def get_benutzer(columns="Vorname,Nachname,Email"):
  conn = sqlite3.connect(data_files['buchungsdatenbank.db'])
  cursor = conn.cursor()
  res = list(cursor.execute(f'SELECT {columns} FROM tblBenutzer'))
  item_list = []
  tmp_idx = 1
  for item in res:
    label = f"{item[0]} {item[1]} {item[2]}"
    tmp_tuple = (label,tmp_idx)
    item_list.append(tmp_tuple)
    tmp_idx += 1
  return item_list

@anvil.server.callable
def get_preiskategorien(id, columns="Preis"):
  conn = sqlite3.connect(data_files['buchungsdatenbank.db'])
  cursor = conn.cursor()
  res = list(cursor.execute(f'SELECT {columns} FROM tblPreiskategorie'))
  item_list = []
  tmp_idx = 1
  for item in res:
    label = f"{item[0]}€"
    tmp_tuple = (label,tmp_idx)
    item_list.append(tmp_tuple)
    tmp_idx += 1
  return item_list


