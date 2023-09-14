"""
Python list model
"""
from datetime import date
from .Model import Model

class model(Model):
    def __init__(self):
        self.guestentries = []

    def select(self):
        """
        Returns guestentries list of lists
        Each list in guestentries contains: id, name, service, location, operating_hours,phone_number, review
        :return: List of lists
        """
        return self.guestentries

    def insert(self, name, service, location, operating_hours, phone_number,review):
        """
        Appends a new list of values representing new message into entries
        :param id: Integer
        :param name: String
        :param service: String
        :param location: String
        :param operating_hours: String
        :param phone_number: Integer
        :param review: String
        :return: True
        """
        params = [name, service, location, operating_hours, phone_number, review]
        self.guestentries.append(params)
        return True