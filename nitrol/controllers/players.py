import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to
from pylons.decorators import jsonify

from nitrol.lib.base import BaseController, render

log = logging.getLogger(__name__)

class PlayersController(BaseController):

    @jsonify
    def getindex(self):
        """Get players in JSON format"""
        return []

    def add(self):
        """Add a new player"""
        pass

