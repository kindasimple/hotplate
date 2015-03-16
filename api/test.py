from api import Api
import json

## Now create an api instance and give it an established access token
access_token = os.getenv("access_token")
api = Api(access_token)

def venues():
	params = ({'section': 'food','near': 'Portland, OR', 'radius': 200})
	result = api.query_venues(params)
	return json.dumps(result, sort_keys=True, indent=4, separators=(',', ': '))

def venues_photos(params):
	#params = ({'section': 'food','near': 'Vancouver, WA', 'radius': 200})
	venues_with_photos = api.query_venues(params)
	params = {'limit': 200}
	print "There are {} venues with photos".format(len(venues_with_photos))
	photos = []
	for venue in venues_with_photos:
		photos.extend(api.query_photos_from_venue(venue, params))
	return photos

def user_photos():
	user_id = 'self'
	photos = api.query_photos_from_user(user_id)
	print "There are {} photos for user {}".format(len(photos), user_id)
	return photos
