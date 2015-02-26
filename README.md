HOTPLATE
==============

Tinder for food

###Overview

A tool for foodies to explore local food venues

###Installation

The api is powered by foursquare and written in python

####Dependencies

* bottle


```
pip install bottle
./run.sh
#open browser to localhost:8080
```	

####Configuration

edit run.sh with updated client_id and client_secret and open http://localhost:8080/oauth/authenticate in a browser

```
export client_id=<<foursquare client id>>
export client_secret=<<foursquare client secret>>

##after visiting /oauth/authenticate

export access_token=<<foursquare access token>>
```

###Roadmap

* Obtain food Images from foursquare, yelp, instagram, and user submissions
* Create simple interface to judge local food
* Connect users to food and people based on their location and interaction

