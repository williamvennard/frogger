from gradientone import InstrumentDataHandler
import webapp2


class Handler(InstrumentDataHandler):
    def get(self):
        self.render('testpage_save.html')