from src import *
class City:
    __table__ = 'cities'
    attributes  = ['id', 'name', 'state_id']

    def __init__(self, **kwargs):
        for key in kwargs.keys():
            if key not in self.attributes:
                raise f'{key} not in {self.attributes}' 
        for k, v in kwargs.items():
            setattr(self, k, v)


    def state(self, cursor):
        query = f"SELECT * FROM states WHERE id = {self.state_id}"
        cursor.execute(query)
        state_record = cursor.fetchone()
        state = build_from_record(State, state_record)

        return state

    def zipcodes(self, cursor):
        query = f"SELECT DISTINCT zipcodes.* FROM zipcodes WHERE city_id = {self.id}"
        cursor.execute(query)
        zipcode_records = cursor.fetchall()
        zipcodes = build_from_records(Zipcode, zipcode_records)

        return zipcodes

