This directory holds the software which lets people add themselves to a map.
The basic data structure is a tree of ZODB objects.
/root/world/<countryCode_postalCode>/person
ccpc = countryCode_postalCode

This started out as just a map of US Green Party voters. It included
zip code Latitude and Longitude data.  But the US greens were not
interested, so I tossed out all of the US specific stuff, and am
making it based on ccpc.  That way each one will have a unique
name. But it also requires the mapbox api to convert country code and
postal code into latitude and longitude information. The first version
will not have that api.

Every ccpc holds a list of persons.  The ccpc pages show a list of
people, links to their fediverse account and their interests.
Interests are initially a list of 7 options.

- Climate Crisis
- @TaxBillionairesNow
- Mastodon/Fediverse
- Gaming
- Dating
- LGBTQ
- Green/Socialist parties. 

The @TaxBillionairesNow will have a link to that user.  Not initially
but in the custom template later. Climate Crisis will have a link to https://UncensoredNews.us later.   

So when the person signs up with oauth, it creates a principal object,
and they are redirected to /gdpr. The code is in file ./gdpr.py.  The
gdpr form asks for their interests, their country name, postal code
and gdpr permission to link to their fediverse account. If they only
provide one of country name, postal code, the request is rejected as a
bad request.  In the next release, updating the data on the client,
will call autocomplete.  Sucess will call the mapbox api with their
country name and postal code to generate the country code, latitude
and longitude needed for the ccpc lookup or creation and for
displaying pins on the map.  ccpc names are canonical, meaning unique,
the root keeps an index of them.

If the person object does not exist, and the valid country name and
postal code are provided, the person object is created.  If its ccpc
object does not exist, it is created and added to the map object.

If the person object already exists, maybe the user is editing their
values.  If the country and postal code are the same, nothing needs to
change.  If the person exists, but the ccpc object is different, the
person is removed from the existing ccpc object, and added to the new
one.  When the last person is removed from a ccpc object, that ccpc
object is deleted.

After the data is updated, countryCode, latitude and longitude are
deleted from the principal object.

On success the user is redirected to their ccpc object where they can
see the other people in that region.  The submit form should tell them
where clicking the button will take them, so that they can spot if there is a problem. 


The gdpr form needs to say, to delete yourself from the map, go to the gdpr form, and delete your country name and postal code.  URL needs to be provided. 

You could get an error if two people are accessing the same ccpc at
the same time, one deleting it the other adding to it.

Eventually the country form field will be replaced with the mapbox
autocomplete api which will populate the hidden country code,
latitude, longitude and some other not needed fields, using some
javascript I have to write.


