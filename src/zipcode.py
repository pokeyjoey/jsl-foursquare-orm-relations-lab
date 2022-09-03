import src
class Zipcode:
    __table__ = 'zipcodes'
    attributes = ['id', 'code', 'city_id']

    def __init__(self, **kwargs):
        for key in kwargs.keys():
            if key not in self.attributes:
                raise f'{key} not in {self.attributes}' 
        for k, v in kwargs.items():
            setattr(self, k, v)

    def city(self, cursor):
        query= f"SELECT * FROM cities WHERE id = {self.city_id}"
        cursor.execute(query)
        city_record = cursor.fetchone()
        city = src.build_from_record(src.City, city_record)

        return city

    def locations(self, cursor):
        query = f"""SELECT DISTINCT l.* FROM locations l
                    JOIN zipcodes z
                    ON  l.zipcode_id = {self.id}"""
        cursor.execute(query)
        location_records = cursor.fetchall()
        locations = src.build_from_records(src.Location, location_records)

        return locations
