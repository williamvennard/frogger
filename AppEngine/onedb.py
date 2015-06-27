from google.appengine.ext import db

class DictModel(db.Model):


    def to_dict(self):
       return dict([(p, unicode(getattr(self, p))) for p in self.properties()])

def OscopeDB_key(name = 'default'):
    return db.Key.from_path('oscope', name)


class OscopeDB(DictModel):


    name = db.StringProperty(required = True)
    config = db.StringProperty(required = True)
    slicename = db.StringProperty(required = True)
    TIME = db.FloatProperty(required = True)
    CH1 = db.FloatProperty(required = True)
    CH2 = db.FloatProperty(required = True)
    CH3 = db.FloatProperty(required = True)
    CH4 = db.FloatProperty(required = True)
    DTE = db.IntegerProperty(required = True)