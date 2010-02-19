from nitrol.tests import *

class TestPlayersController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='players', action='index'))
        # Test response...
