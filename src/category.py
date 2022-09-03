import src
class Category:
    __table__ = 'categories'
    attributes = ['id', 'name']

    def __init__(self, **kwargs):
        for key in kwargs.keys():
            if key not in self.attributes:
                raise f'{key} not in {self.attributes}' 
        for k, v in kwargs.items():
            setattr(self, k, v)

    @classmethod
    def find_by_name(self, name, cursor):
        category_query = """SELECT * FROM categories WHERE name = %s """
        cursor.execute(category_query, (name,))
        category_record =  cursor.fetchone()
        category = src.build_from_record(self, category_record)
        return category

    @classmethod
    def find_or_create_by_name(self, name, conn, cursor):
        category = self.find_by_name(name, cursor)
        if not category:
            new_category = Category()
            new_category.name = name
            src.save(new_category, conn, cursor)
            category = self.find_by_name(name, cursor)
        return category


    def venues(self, cursor):
        query = f"""SELECT DISTINCT v.*
                    FROM venue_categories vc
                    JOIN venues v
                    ON  vc.venue_id = v.id
                    WHERE vc.category_id = {self.id}"""
        cursor.execute(query)
        venue_records = cursor.fetchall()
        venues = src.build_from_records(src.Venue, venue_records)

        return venues

