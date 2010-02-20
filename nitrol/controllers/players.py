# vim: fileencoding=utf-8
import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to
from pylons.decorators import jsonify, validate
from pylons.decorators.rest import restrict
import nitrol.model as model
from nitrol.model import meta
import formencode

from nitrol.lib.base import BaseController, render

log = logging.getLogger(__name__)

class RankValidator(formencode.FancyValidator):
    def _to_python(self, value, state):
        if (len(value) > 3):
            raise formencode.Invalid('Podaj krótką formę', value, state)
        kyudan = value[-1]
        try:
            count = int(value[:-1])
        except ValueError:
            raise formencode.Invalid('Nieprawidłowa forma', value, state)
        if kyudan == 'k':
            if count < 1 or count > 30:
                raise formencode.Invalid('Wartość kyu poza zakresem', value, state)
        elif kyudan == 'd':
            if count < 1 or count > 8:
                raise formencode.Invalid('Wartość dan poza zakresem', value, state)
        else:
            raise formencode.Invalid('Dopuszczalne: k/d', value, state)
        return value

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

    @jsonify
    @restrict('POST')
    def add(self):
        """Add a new player"""
        try:
            form_result = PlayerSchema.to_python(request.params)
        except formencode.Invalid, e:
                return {'success': False, 'data': str(e)}
        player = model.Player()
        for k, v in form_result.items():
            setattr(player, k, v)
        meta.Session.add(player)
        meta.Session.commit()
        return {'success': True}



