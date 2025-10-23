# OUTH FLOW

First of all go to /app/data/oauth
and read the README for how to get credentials. 

The menu URL takes the users to 
/oauth/wiki.pythonlinks.info/mastodon.social/moauth

That looks up the secrets and sends him to Mastodon which sends him
back with a callback to /person/callback

That then logs him in.


Then do the Oauth flow.  Create the URL, and go to it.  The user logs in, 
redirects to the ..../callback and now you have the access token for that 
individual.  You can now get information about that individual.  And then 
either send the to the registration page, or log them in. 

Quite tricky because thare are two access tokens, the apps and the users. 
