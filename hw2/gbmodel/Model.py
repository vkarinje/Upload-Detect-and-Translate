class Model():
    def select(self):
        """
        Gets all entries from the database
        :return: Tuple containing all rows of database
        """
        pass

    def insert(self, name, service, location,operating_hours,phone_number,review):
        """
        Inserts entry into database
        :param name: String
        :param service: String
        :param location: String
        :param operating_hours: String
        :param phone_number: Integer
        :param review: String
        :return: none
        :raises: Database errors on connection and insertion
        """
        pass