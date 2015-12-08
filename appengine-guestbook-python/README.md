# Modification

This example from the Google Python tutorial has been modified to
do a GQL query:
    qry = ndb.gql("SELECT * FROM Greeting WHERE date > DATETIME(2015,11,20)")

View results at https://{appid}.appspot.com/gql

See handler:

    class TryGQL(webapp2.RequestHandler):

Lots of logging.info messages.

The rest of this file is from Google via:

    git clone https://github.com/GoogleCloudPlatform/appengine-guestbook-python/

# Guestbook

Guestbook is an example application showing basic usage of Google App
Engine. Users can read & write text messages and optionaly log-in with
their Google account. Messages are stored in App Engine (NoSQL)
High Replication Datastore (HRD) and retrieved using a strongly consistent
(ancestor) query.

## Products
- [App Engine][1]

## Language
- [Python][2]

## APIs
- [NDB Datastore API][3]
- [Users API][4]

## Dependencies
- [webapp2][5]
- [jinja2][6]
- [Twitter Bootstrap][7]

[1]: https://developers.google.com/appengine
[2]: https://python.org
[3]: https://developers.google.com/appengine/docs/python/ndb/
[4]: https://developers.google.com/appengine/docs/python/users/
[5]: http://webapp-improved.appspot.com/
[6]: http://jinja.pocoo.org/docs/
[7]: http://twitter.github.com/bootstrap/
