# vim: fileencoding=utf-8
import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to
from pylons.decorators import jsonify
import formencode

from nitrol.lib.base import BaseController, render

log = logging.getLogger(__name__)

class RankValidator(formencode.FancyValidator):
    def _to_python(self, value, state):
        if (len(value) > 3):
            self.invalid(value, state)
        kyudan = value[-1]
        try:
            count = int(value[:-1])
        except ValueError:
            self.invalid(value, state)
        if kyudan is 'k':
            if count < 1 or count > 30:
                self.invalid(value, state)
        elif kyudan is 'd':
            if count < 1 or count > 8:
                self.invalid()
        else:
            self.invalid(value, state)
        return value

    def invalid(self, value, state):
        raise formencode.Invalid('Nieprawidłowy rank', value, state)

class PlayerSchema(formencode.Schema):
    pin = formencode.validators.Int()
    first_name = formencode.validators.String(notEmpty = True)
    last_name = formencode.validators.String(notEmpty = True)
    club = formencode.validators.String(notEmpty = True)
    rank = RankValidator()
    egf = formencode.validators.Int() 

class PlayersController(BaseController):
    """This controller does all the player manipulation
    Meant to be used with Ajax"""

    @jsonify
    def getindex(self):
        """Get players in JSON format"""
        return []

    def add(self):
        """Add a new player"""



