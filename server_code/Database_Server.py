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
def get_jugendherbergen():

  conn = sqlite3.connect(data_files['buchungsdatenbank.db'])
  cursor = conn.cursor()
  res = list(cursor.execute('SELECT Name,IDJugendherberge FROM tblJugendherberge'))
  print(res)
  return res

@anvil.server.callable
def get_all_users():
  conn = sqlite3.connect(data_files['buchungsdatenbank.db'])
  cursor = conn.cursor()
  res = list(cursor.execute(
      '''
      SELECT Vorname || " " || Nachname || " " || Email AS label, IDBenutzer
      FROM tblBenutzer
      '''
  ))
  print(res)
  return res

@anvil.server.callable
def get_preiskategorien():
  conn = sqlite3.connect(data_files['buchungsdatenbank.db'])
  cursor = conn.cursor()
  res = list(cursor.execute(
      '''
      SELECT Preis || "€" AS label, IDPreiskategorie
      FROM tblPreiskategorie 
      '''
  ))
  print(res)
  return res
  
@anvil.server.callable
def get_zimmer_for_jugendherberge(JID, PK_current):
  conn = sqlite3.connect(data_files['buchungsdatenbank.db'])
  cursor = conn.cursor()
  res = list(cursor.execute(
      '''
      SELECT "NR: " || IDZimmer || " Plätze: " || MaxBettenanzahl AS label, IDZimmer 
      FROM tblZimmer 
      WHERE fkJugendherberge = ? AND fkPreiskategorie = ?
      ''', 
      (JID, PK_current)
  ))
  print(res)
  return res