import pytest
from src import State, City, Zipcode, Venue, Location, save, test_conn, test_cursor, drop_all_tables, Category, VenueCategory

location =  {'address': '141 Front St', 'crossStreet': 'Pearl St', 'lat': 40.70243624175102, 'lng': -73.98753900608666, 'labeledLatLngs': [{'label': 'display', 'lat': 40.70243624175102, 'lng': -73.98753900608666}], 'postalCode': '11201', 'cc': 'US', 'neighborhood': 'DUMBO', 'city': 'New York', 'state': 'NY', 
        'country': 'United States', 'formattedAddress': ['141 Front St (Pearl St)', 'New York, NY 11201', 'United States']}

categories = [{'id': '4bf58dd8d48988d151941735', 'name': 'Taco Place', 'pluralName': 'Taco Places', 'shortName': 'Tacos', 'icon': {'prefix': 'https://ss3.4sqi.net/img/categories_v2/food/taco_', 'suffix': '.png'}, 'primary': True}]

venue_details = {'id': '5b2932a0f5e9d70039787cf2', 'name': 'Los Tacos Al Pastor', 'categories': categories, 'location': location, 'rating': 7.9, 'price': {'tier': 1}, 'likes': {'count': 52}, 
        'delivery': {'url': 'https://www.seamless.com/menu/los-tacos-al-pastor-141a-front-st-brooklyn/857049?affiliate=1131&utm_source=foursquare-affiliate-network&utm_medium=affiliate&utm_campaign=1131&utm_content=857049'}}

@pytest.fixture()
def clean_tables():
    drop_all_tables(test_conn, test_cursor)
    yield
    drop_all_tables(test_conn, test_cursor)

@pytest.fixture()
def grimaldis():
    drop_all_tables(test_conn, test_cursor)

    new_york = save(State(name = 'New York'), test_conn, test_cursor)
    pennsylvania = save(State(name = 'Pennsylvania'), test_conn, test_cursor)

    brooklyn = save(City(name='Brooklyn', state_id = new_york.id), test_conn, test_cursor)
    manhattan = save(City(name='Manhattan', state_id = new_york.id), test_conn, test_cursor)
    philadelphia = save(City(name='Philadelphia', state_id = pennsylvania.id), test_conn, test_cursor)
    south_philly_zip = save(Zipcode(code=19019, city_id = philadelphia.id), test_conn, test_cursor)
    chelsea_zip = save(Zipcode(code=10001, city_id = manhattan.id), test_conn, test_cursor)
    dumbo_zip = save(Zipcode(code=11210, city_id = brooklyn.id), test_conn, test_cursor)

    venue = save(Venue(name='Los Tacos Al Pastor', price = 1, foursquare_id = '4bf58dd8d48988d151941735'), test_conn, test_cursor)
    grimaldis = save(Venue(name='Grimaldis', price = 2), test_conn, test_cursor)
    pizza = save(Category(name='Pizza'), test_conn, test_cursor)
    tourist_spot = save(Category(name='Tourist Spot'), test_conn, test_cursor)
    save(VenueCategory(venue_id = grimaldis.id, category_id = pizza.id), test_conn, test_cursor)
    save(VenueCategory(venue_id = grimaldis.id, category_id = tourist_spot.id), test_conn, test_cursor)

    grimaldi_location = save(Location(longitude = 40.7024 , latitude = -73.9875,
        address='1 Front Street', zipcode_id = dumbo_zip.id, venue_id = grimaldis.id), test_conn, test_cursor)
    taco_location = save(Location(longitude = 40.7024 , latitude = -73.9875,
        address='141 Front Street', zipcode_id = dumbo_zip.id, venue_id = venue.id), test_conn, test_cursor)
    yield grimaldis
    drop_all_tables(test_conn, test_cursor)

def test_venue_location(grimaldis):
    assert grimaldis.location(test_cursor).address == '1 Front Street'

def test_find_by_foursquare_id(grimaldis):
    foursquare_id = "4bf58dd8d48988d151941735"
    assert Venue.find_by_foursquare_id(foursquare_id, test_cursor).name == 'Los Tacos Al Pastor'

def test_venue_categories(grimaldis):
    categories = grimaldis.categories(test_cursor)
    category_names = [category.name for category in categories]
    assert category_names == ['Pizza', 'Tourist Spot']
