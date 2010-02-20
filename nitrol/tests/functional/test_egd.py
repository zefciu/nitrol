from nitrol.tests import *

class TestEgdController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='egd', action='index'))
        # Test response...
