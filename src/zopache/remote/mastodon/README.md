# OUTH FLOW

First of all go to your favorite Mastodon server, and create an application. 
That gives you a clienKey/ID, clientSecret and accessToken. That access token
is your applicaitons access token.  

Then do the Oauth flow.  Create the URL, and go to it.  The user logs in, 
redirects to the ..../callback and now you have the access token for that 
individual.  You can now get information about that individual.  And then 
either send the to the registration page, or log them in. 

Quite tricky because thare are two access tokens, the apps and the users. 
