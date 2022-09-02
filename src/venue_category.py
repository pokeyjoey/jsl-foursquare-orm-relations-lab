class VenueCategory:
    __table__ = 'venue_categories'
    attributes = ['venue_id', 'category_id']

    def __init__(self, **kwargs):
        for key in kwargs.keys():
            if key not in self.attributes:
                raise f'{key} not in {self.attributes}' 
        for k, v in kwargs.items():
            setattr(self, k, v)
