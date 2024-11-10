import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.files
from anvil.files import data_files
import anvil.server
import sqlite3
from datetime import datetime

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
  conn = sqlite3.connect(data_files['buchungsdatenbank.db'])
  cursor = conn.cursor()
  res = list(cursor.execute(
      '''
      SELECT Vorname || " " || Nachname || " " || Email AS label, IDBenutzer
      FROM tblBenutzer WHERE IDBenutzer != ?;
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
      FROM tblPreiskategorie;
      '''
  ))
  return res
  
@anvil.server.callable
def get_preiskategorie_for_user(ID):
  conn = sqlite3.connect(data_files['buchungsdatenbank.db'])
  cursor = conn.cursor()
  res = list(cursor.execute(
      '''
      SELECT fkPreiskategorie
      FROM  tblBenutzer
      WHERE IDBenutzer = ?;
      ''',
    (str(ID))
    
  ))
  item = res[0][0]
  return item
  
@anvil.server.callable
def get_zimmer_for_jugendherberge(JID, PK_current):
  conn = sqlite3.connect(data_files['buchungsdatenbank.db'])
  cursor = conn.cursor()
  res = list(cursor.execute(
      '''
      SELECT "NR: " || IDZimmer || " Plätze: " || MaxBettenanzahl AS label, IDZimmer 
      FROM tblZimmer 
      WHERE fkJugendherberge = ? AND fkPreiskategorie = ?;
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
      WHERE IDBenutzer = ?;
      ''', 
      (PID, UserID)
  )
  conn.commit()
  conn.close()
@anvil.server.callable
def get_user(ID):
  conn = sqlite3.connect(data_files['buchungsdatenbank.db'])
  cursor = conn.cursor()
  res = list(cursor.execute(
    '''
    SELECT Vorname || " " || Nachname, IDBenutzer
    FROM tblBenutzer
    WHERE IDBenutzer = ?;
    ''', 
    (str(ID))
    ))

  return str(res[0][0]), str(res[0][1])


@anvil.server.callable
def add_buchung(buchung_info):
  conn = sqlite3.connect(data_files['buchungsdatenbank.db'])
  cursor = conn.cursor()
  cursor.execute(
    '''
    INSERT INTO tblBuchung
    (Startzeit, Endzeit, fkZimmer)
    VALUES (?,?,?);
    ''', 
    (buchung_info[3],buchung_info[4],buchung_info[2])
  )
  conn.commit()
  res = cursor.execute('''
  SELECT MAX(IDBuchung) AS LastID
  FROM tblBuchung;
  '''
  )
  conn.commit()
  idBuchung = cursor.fetchone()[0]
  cursor.execute(
      '''
      INSERT INTO tblBuchungBenutzer
      (IDBenutzer, IDBuchung, Benutzerrolle)
      VALUES (?,?,?);
      ''',
    (buchung_info[0], idBuchung, 'Ersteller')
  )
  conn.commit()
  for element in buchung_info[5]:
    cursor.execute(
      '''
      INSERT INTO tblBuchungBenutzer
      (IDBenutzer, IDBuchung, Benutzerrolle)
      VALUES (?,?,?);
      ''',
      (element,idBuchung,'Mitbucher')
      )
    conn.commit()
  conn.close()

@anvil.server.callable
def get_data():
  conn = sqlite3.connect(data_files['buchungsdatenbank.db'])
  cursor = conn.cursor()
  test = list(cursor.execute(
    '''
    SELECT * FROM tblBuchung;
    '''
  ))
  data = list(cursor.execute(
    '''
    SELECT * FROM view_benutzerBuchung;
    '''
  ))
  conn.commit()
  conn.close()
  return data

@anvil.server.callable
def get_maxBeds(ID):
  conn = sqlite3.connect(data_files['buchungsdatenbank.db'])
  cursor = conn.cursor()
  res = list(cursor.execute(
  '''
  SELECT MaxBettenAnzahl FROM tblZimmer WHERE IDZimmer = ?;
  ''', (str(ID))
  ))
  return res[0][0]

@anvil.server.callable
def check_dates(start_date,end_date, IDZimmer):
  conn = sqlite3.connect(data_files['buchungsdatenbank.db'])
  cursor = conn.cursor()
  res = list(cursor.execute(
    '''
    SELECT Startzeit,Endzeit FROM tblBuchung WHERE fkZimmer = ?;
    ''', str(IDZimmer)
  ))
  for item in res:
    range_start = datetime.strptime(item[0], "%Y-%m-%d").date()
    range_end = datetime.strptime(item[1],"%Y-%m-%d").date()
    is_start_in_range = range_start <= start_date <= range_end
    is_end_in_range = range_start <= end_date <= range_end
    if (is_start_in_range or is_end_in_range):
      return True
  return False
  