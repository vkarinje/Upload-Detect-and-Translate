from .Model import Model
from datetime import date
from google.cloud import datastore

def from_datastore(entity):
    if not entity:
        return None
    if isinstance(entity, list):
        entity = entity.pop()
    return [entity['name'], entity['service'], entity['location'], entity['operating_hours'], entity['phone_number'], entity['review']]

class model(Model):
    def __init__(self):
        self.client = datastore.Client('cloud-cs-530-karinje-vkarinje')

    def select(self):
        query = self.client.query(kind = 'Review')
        entities = list(map(from_datastore,query.fetch()))
        return entities

    def insert(self,  name, service, location, operating_hours, phone_number,review):
        key = self.client.key('Review')
        rev = datastore.Entity(key)
        rev.update( {'name':name, 'service':service, 'location':location, 'operating_hours':operating_hours,'phone_number':phone_number, 'review':review})
        self.client.put(rev)
        return True
