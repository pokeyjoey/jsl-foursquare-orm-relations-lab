import src
class State:
    __table__ = 'states'
    attributes = ['id', 'name']

    def __init__(self, **kwargs):
        for key in kwargs.keys():
            if key not in self.attributes:
                raise f'{key} not in {self.attributes}' 
        for k, v in kwargs.items():
            setattr(self, k, v)

    def cities(self, cursor):
        query = f"""SELECT DISTINCT cities.* FROM cities
                    WHERE state_id = {self.id}"""
        cursor.execute(query)
        city_records = cursor.fetchall()
        cities = src.build_from_records(src.City, city_records)

        return cities
