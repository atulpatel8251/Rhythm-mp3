# from sqlite3 import DatabaseError, connect
from cx_Oracle import DatabaseError,connect
from traceback import*
from cx_Oracle import *
class Model:
    def __init__(self):
      self.song_dict={}
      self.db_status=True
      self.conn=None
      self.cur=None
      try:
          self.conn=connect("mouzikka/music@127.0.0.1/xe")
          print("connected to successfully to the DB")
          self.cur=self.conn.cursor()
      except DatabaseError:
          self.db_status=False
          print("DB error:",format_exc())
      
    def get_db_status(self):
          return self.db_status 
      
    def close_db_connection(self):
          if self.cur is not None:
              self.cur.close()
              print("cursor closed succesfully")
          if self.conn is not None:
              self.conn.close()
              print("disconnected successfully from the DB") 
      
    def add_song(self,song_name,song_path):
          self.song_dict[song_name]=song_path
          print("song added:",self.song_dict[song_name])
      
    def get_song_path(self,song_name):
          return self.song_dict[song_name]
      
    def remove_song(self,song_name):
          self.song_dict.pop(song_name)
          print("after deletion:",self.song_dict)
      
    def search_song_in_favourites(self,song_name):
          self.cur.excute("select song_name from myfavourite where song_name=:1",(song_name))
          song_tuple=self.cur.fetchone()
          if song_tuple is None:
              return False
          else:    
              return True
      
    def add_song_to_favourites(self,song_name,song_path):
          is_song_present=self.search_song_in_favorites(song_name)
          if is_song_present==True:
              return "song already present in favourites"
          self.cur.excute("select max(song_id) from myfavourites")
          last_song_id=self.cur.fetchone()[0]
          next_song_id=1
          if last_song_id is not None:
                next_song_id=last_song_id+1
          self.cur.execute("insert into myfavourites values(:1,:2,:3)",(next_song_id,song_name,song_path))
          self.conn.commit()
          return "song sucessfully added to your favourites"
      
    def load_song_from_favourites(self):
           self.cur.execute("select song_name,song_path from myfavourites")
           for song_name,song_path in self.cur:
               self.song_dict[song_name]=song_path
               song_present=True
           if song_present:
               return "list populated from favourites"
           else:
               return "no songs present in your favourite"
      
    def remove_song_from_favourites(self,song_name):
          self.cur.execute("delete from myfavourites where song_name=:1",(song_name,))
          count=self.cur.rowcount
          if count==0:
              return "song not present in your favourites"
          else:
              self.song_dict.pop(song_name)
              self.conn.commit()
              return "song deleted from your favourites"
      
    def get_song_count(self):
          return len(self.song_dict)         



                   







