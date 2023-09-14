

from .Model import Model
import sqlite3
DB_FILE = 'entries.db'    # file for our Database

class model(Model):
    def __init__(self):
        # Make sure our database exists
        connection = sqlite3.connect(DB_FILE)
        cursor = connection.cursor()
        try:
            cursor.execute("select count(rowid) from guestbook")
        except sqlite3.OperationalError:
            cursor.execute("Create table guestbook (ID INTEGER PRIMARY KEY NOT NULL,name text, service text, location text, operating_hours text,phone_number int, review text)")
        cursor.close()

    def select(self):
        """
        Gets all rows from the database
        Each row contains: id, name, service, location, operating_hours,phone_number, review
        :return: List of lists containing all rows of database
        """
        connection = sqlite3.connect(DB_FILE)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM guestbook")
        return cursor.fetchall()

    def insert(self,  name, service, location, operating_hours, phone_number,review):
        """
        Inserts entry into database
        
        :param name: String
        :param service: String
        :param location: String
        :param operating_hours: String
        :param phone_number: Integer
        :param review: String
        :return: True
        :raises: Database errors on connection and insertion
        """
        params = {'name':name, 'service':service, 'location':location, 'operating_hours':operating_hours,'phone_number':phone_number, 'review':review}
        connection = sqlite3.connect(DB_FILE)
        cursor = connection.cursor()
        cursor.execute("insert into guestbook (name, service, location, operating_hours, phone_number, review) VALUES (:name, :service, :location, :operating_hours, :phone_number, :review)", params)

        connection.commit()
        cursor.close()
        return True
    def fetch(self,ID):
        print("fetching id",ID)
        params = {'ID':ID}
        connection = sqlite3.connect(DB_FILE)
        cursor = connection.cursor()
        cursor.execute("Select * from guestbook where ID=:ID",params)
        print("gghhhuhuih")
        return cursor.fetchall()


    def update(self, ID, name, service, location, operating_hours, phone_number,review):
        params = {'ID':ID, 'name':name, 'service':service, 'location':location, 'operating_hours':operating_hours,'phone_number':phone_number, 'review':review}
        connection = sqlite3.connect(DB_FILE)
        cursor = connection.cursor()
        cursor.execute("update guestbook SET name=:name,service=:service, location=:location,operating_hours=:operating_hours, phone_number=:phone_number,review=:review where ID=:ID",params)

        connection.commit()
        cursor.close()
        return True
    def delete(self,ID):
        params = {'ID':ID}
        connection = sqlite3.connect(DB_FILE)
        cursor = connection.cursor()
        cursor.execute("delete from guestbook where ID=:ID",params)
        connection.commit()
        cursor.close()
        return True