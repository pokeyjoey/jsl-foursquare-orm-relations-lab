from src import *
class Location:
    __table__ = 'locations'
    attributes = ['id', 'longitude', 'latitude', 'address', 
            'zipcode_id', 'venue_id', 'created_at']

    def __init__(self, **kwargs):
        for key in kwargs.keys():
            if key not in self.attributes:
                raise f'{key} not in {self.attributes}' 
        for k, v in kwargs.items():
            setattr(self, k, v)

    def venue(self, cursor):
        query = f"SELECT * FROM venues WHERE id = {self.venue_id}"
        cursor.execute(query)
        venue_record = cursor.fetchone()
        venue = build_from_record(Venue, venue_record)

        return venue

    def zipcode(self, cursor):
        query = f"SELECT * FROM zipcodes WHERE id = {self.zipcode_id}"
        cursor.execute(query)
        zipcode_record = cursor.fetchone()
        zipcode = build_from_record(Zipcode, zipcode_record)

        return zipcode

