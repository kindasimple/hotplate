import foursquare, json, os
from bottle import route, run, template, request, response, redirect
from api import Api

##Setup

#get keys from environment
#run start.sh to set them before running this script
client_id=os.getenv("client_id")
client_secret=os.getenv("client_secret")
client = None


#we already have an access token, so set it and we can start calling
#the feed
access_token = os.getenv("access_token")
api = Api(access_token)
host = 'localhost'
port = 8080
root = 'http://{}:{}/'.format(host, port)

##Define routes

#default route to get links to api
@route('/')
def index():
    return '''
    	<p><a href="/oauth/authenticate">Authenticate</a></p>
	<p><a href="/venues">Venues</a></p>
	<p><a href="/venues/photos">Venue Photos</a></p>
	<p><a href="/user/photos">User Photos</a></p>
	'''
@route('/oauth/authenticate')
def authenticate():
	global client
	client = foursquare.Foursquare(client_id=client_id, client_secret=client_secret, redirect_uri=root + 'oauth/authorize')
	auth_uri = client.oauth.auth_url()
	redirect(auth_uri)

#oath to get access token
@route('/oauth/authorize')
def authorize():
    global client
    auth_code = request.query.code 
    access_token = client.oauth.get_token(auth_code)
    client.set_access_token(access_token)
    user = client.users()
    #print(user)
    return template('<b>Authorization Code {{auth_code}}</b>!<b>Token {{ access_token }}</b><a href="/">Continue</a>', auth_code=auth_code, access_token=access_token)

#parameters to use in the routes
params = ({'section': 'food','near': 'Portland, OR', 'radius': 400})

#output the venues near portland
@route('/venues')
def venues():
	result = api.query_venues(params)
	response.content_type = 'application/json'
	return json.dumps(result, sort_keys=True, indent=4, separators=(',', ': '))

#output the photos for portland venues
@route('/venues/photos')
def venues_photos():
	venues_with_photos = api.query_venues(params)
	print "There are {} venues with photos".format(len(venues_with_photos))
	photos = []
	for venue in venues_with_photos:
		photos.extend(api.query_photos_from_venue(venue, {'limit': 200}))
	#response.content_type = 'application/json'
	#return json.dumps(photos, sort_keys=True, indent=4, separators=(',', ': '))
	html = "<H3>Photos</h3>"
	for photo in photos:
		html = html + "<a href='" + api.get_fullsize_url_from_photo(photo) + "'><img src='"+ api.get_thumbnail_url_from_photo(photo, width=50, height=50) + "' /></a>"
	return html

#output user photos
@route('/user/photos')
def user_photos():
	user_id = 'self'
	photos = api.query_photos_from_user(user_id)
	print "There are {} photos for user {}".format(len(photos), user_id)
	#response.content_type = 'application/json'
	#return json.dumps(photos, sort_keys=True, indent=4, separators=(',', ': '))
	html = "<H3>User Photo</h3>"
	for photo in photos:
		html = html + "<a href='" + api.get_fullsize_url_from_photo(photo) + "'><img src='"+ api.get_thumbnail_url_from_photo(photo, width=50, height=50) + "' /></a>"
	return html


run(host=host, port=port)

