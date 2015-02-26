import foursquare
import json

class Api:
	"""A class that initializes the foursquare module
	https://github.com/mLewisLogic/foursquare/blob/master/foursquare/__init__.py"""
	def __init__(self, access_token):
		self.client = foursquare.Foursquare(access_token=access_token)
	
	def __get_venues_from_response(self, response):
		results = []
		for group in response["groups"]:
			for item in group["items"]:
				#print json.dumps(item, indent=4, separators=(',',': '))
				if item["venue"]["photos"]["count"] > 0:
					results.append(item["venue"])
		return results
	
	def query_venues(self, params):
		"""queries the foursquare api venues endpoint, writes the output to venues.json
		for inspection, and returns an array of group item venues that have photos"""
		payload = self.client.venues.explore(params=params)
		
		#with open('venues.json', 'w') as f:
		#	output = json.dumps(payload, sort_keys=True, indent=4, separators=(',', ': '))
		#	f.write(output)
		
		results = self.__get_venues_from_response(payload)
		return results

	def query_photos_from_venue(self, venue, params):
		payload = self.client.venues.photos(VENUE_ID=venue["id"], params=params)
		
		#with open('photos_' + venue["id"], 'w') as f:
		#	output = json.dumps(payload, sort_keys=True, indent=4, separators=(',', ': '))
		#	f.write(output)
		
		return payload["photos"]["items"]

	def query_photos_from_user(self, user_id):
		payload = self.client.users.photos(USER_ID=user_id)

		#with open('user_photos', 'w') as f:
		#	output = json.dumps(payload, sort_keys=True, indent=4, separators=(',', ': '))
		#	f.write(output)
		
		return payload["photos"]["items"]
	
	def get_fullsize_url_from_photo(self, photo):
		"""Generate a url using the dimensions from the feed"""
		return "{}{}x{}{}".format(photo["prefix"], photo["height"], photo["width"], photo["suffix"])
	
	def get_thumbnail_url_from_photo(self, photo, **kwargs):
		"""generate a thumbnail, expecting the width and height to be present in the args dictionary"""
		return "{}{}x{}{}".format(photo["prefix"], kwargs["height"], kwargs["width"], photo["suffix"])

