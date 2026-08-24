# OUTH FLOW

Oauth credentials used be created on the files system.  
You can go to /app/data/oauth
and read the README for how that worked. . 

The new system is tht the user goes to
/person/oauth
And enters the mastodon domain name.

The server checks if it is a valide DottedName.
If so, it redirects to
/person/moauth/<mastodon_domain>

That checks if there is a valid credential, and if not creates it.  It
then reads the credentials and sends the user to the
Mastodon/Fediverse server which has the user login, and approve the
oauth process flow. It then sends him back with a callback to
/person/callback/<Mastodon_domain>
That then gets his details, if needed creates the account, and then
logs him in.  If he is new, it sends him to the gdpr page. 

