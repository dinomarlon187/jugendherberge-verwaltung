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
  return res

@anvil.server.callable
def get_all_users(ID=0):
  print(ID, "Hallo")
  conn = sqlite3.connect(data_files['buchungsdatenbank.db'])
  cursor = conn.cursor()
  res = list(cursor.execute(
      '''
      SELECT Vorname || " " || Nachname || " " || Email AS label, IDBenutzer
      FROM tblBenutzer WHERE IDBenutzer != ?
      ''',
      (str(ID))
  )) 
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
def get_preiskategorie_for_user(ID):
  conn = sqlite3.connect(data_files['buchungsdatenbank.db'])
  cursor = conn.cursor()
  res = list(cursor.execute(
      '''
      SELECT fkPreiskategorie
      FROM  tblBenutzer
      WHERE IDBenutzer = ?
      ''',
    (str(ID))
    
  ))
  item = res[0][0]
  print(item)
  return item
  
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
      (str(JID), str(PK_current))
  ))
  return res

@anvil.server.callable
def save_preiskategorie(PID,UserID):
  # theoretisch speichert er die neue Preiskategorie hier als Standart ab, aber shit not working
  conn = sqlite3.connect(data_files['buchungsdatenbank.db'])
  cursor = conn.cursor()
  cursor.execute(
      '''
      UPDATE tblBenutzer
      SET fkPreiskategorie = ?
      WHERE IDBenutzer = ?
      ''', 
      (PID, UserID)
  )
@anvil.server.callable
def get_user(ID):
  conn = sqlite3.connect(data_files['buchungsdatenbank.db'])
  cursor = conn.cursor()
  res = list(cursor.execute(
    '''
    SELECT Vorname || " " || Nachname, IDBenutzer
    FROM tblBenutzer
    WHERE IDBenutzer = ?
    ''', 
    (str(ID))
    ))
  print(res[0][0])
  return str(res[0][0]), str(res[0][1])


@anvil.server.callable
def add_buchung(buchung_info):
  conn = sqlite3.connect(data_files['buchungsdatenbank.db'])
  cursor = conn.cursor()
  cursor.execute(
    '''
    INSERT INTO tblBuchung
    (Startzeit, Endzeit, fkZimmer)
    VALUES (?,?,?)
    ''', 
    (buchung_info[3],buchung_info[4],buchung_info[2])
    )
  res = cursor.execute('''
  SELECT MAX(IDBuchung) AS LastID
  FROM tblBuchung
  '''
    )
  idBuchung = cursor.fetchone()[0]
  cursor.execute(
      '''
      INSERT INTO tblBuchungBenutzer
      (IDBenutzer, IDBuchung, Benutzerrolle)
      VALUES (?,?,?)
      ''',
    (buchung_info[0], idBuchung, 'Ersteller')
      )
  for element in buchung_info[5]:
    cursor.execute(
      '''
      INSERT INTO tblBuchungBenutzer
      (IDBenutzer, IDBuchung, Benutzerrolle)
      VALUES (?,?,?)
      ''',
      (element,idBuchung,'Mitbucher')
      )
  conn.close()