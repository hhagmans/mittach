# encoding: utf-8
import os, sys, unittest

os.environ["MITTACH_CONFIG_MODE"] = "testing"
sys.path.append("/Users/hendrik11/Documents/innoq_mittach")
from mittach.web import app, database
from flask import Flask, g

class TestCase(unittest.TestCase):

    def setUp(self):
        assert app.config["MODE"] == "testing"
        # reset database
        self.db = database.connect(app.config)
        self.db.flushall()
        self.app = app.test_client()


#    def tearDown(self):
#        os.close(self.db)
#        os.unlink(mittach.DATABASE)

    def test_creation(self):
        data = { "title": "FooBar", "details": "", "date": "2012:03:10",
                "slots": 3, "vegetarian": True }

        assert database.create_event(self.db, data) == 1

    def test_event_list(self):
        defaults = { "details": "", "date": 0, "vegetarian": False }
        for i, data in enumerate([{ "title": "Foo", "slots": 1 },
                { "title": "Bar", "slots": 2, "vegetarian": True },
                { "title": "Baz", "slots": 3 }]):
            _data = {}
            _data.update(defaults)
            _data.update(data)
            database.create_event(self.db, _data)

        events = database.list_events(self.db)
        assert len(events) == 3
        assert ["Baz", "Bar", "Foo"] == [event["title"] for event in events]

    def test_admin(self):

        with app.test_request_context():
            rv = self.app.get('/events/1')
            print rv.data
            assert u'Admin' in rv.data

if __name__ == '__main__':
    unittest.main()

#class Test(object):
#
#    def setup_method(self, method):
#        assert app.config["MODE"] == "testing"
#        # reset database
#        self.db = database.connect(app.config)
#        self.db.flushall()
#
#    def test_creation(self):
#        data = { "title": "FooBar", "details": "", "date": "2012:03:10",
#                "slots": 3, "vegetarian": True }
#        try:
#            assert database.create_event(self.db, data) == 1
#            print "Test 1 success"
#        except AssertionError:
#            print "Test 1 failed"
#
#    def test_event_list(self):
#        defaults = { "details": "", "date": 0, "vegetarian": False }
#        for i, data in enumerate([{ "title": "Foo", "slots": 1 },
#                { "title": "Bar", "slots": 2, "vegetarian": True },
#                { "title": "Baz", "slots": 3 }]):
#            _data = {}
#            _data.update(defaults)
#            _data.update(data)
#            database.create_event(self.db, _data)
#
#        events = database.list_events(self.db)
#        assert len(events) == 3
#        assert ["Baz", "Bar", "Foo"] == [event["title"] for event in events]
#
#    def test_admin(self):
#        rv = self.app.get('/admin/1')
#        assert u'Du besitzt nicht die benötigten Rechte für diese Seite.' in rv.data
