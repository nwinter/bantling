"""
models.py

App Engine datastore models

"""


from google.appengine.ext import ndb


class ExampleModel(ndb.Model):
    """Example Model"""
    example_name = ndb.StringProperty(required=True)
    example_description = ndb.TextProperty(required=True)
    added_by = ndb.UserProperty()
    timestamp = ndb.DateTimeProperty(auto_now_add=True)


class SavedNames(ndb.Model):
    user = ndb.StringProperty(required=True)
    liked = ndb.StringProperty(repeated=True)
    hated = ndb.StringProperty(repeated=True)
    timestamp = ndb.DateTimeProperty(auto_now_add=True)

    def to_dict(self):
        return {'liked': self.liked or [],
                'hated': self.hated or []}

    #def to_dict(self):
    #    return {'liked': ['Katana', 'Jumonji'],
    #            'hated': ['Horace', 'Gertrude', 'Spittlespackle', 'Eustace', 'Euvegenia']}
