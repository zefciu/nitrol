import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from nitrol.lib.base import BaseController, render

log = logging.getLogger(__name__)

class PlayersController(BaseController):

    def get_index(self):
        """Get players in JSON format"""
        pass

    def add(self):
        """Add a new player"""
        pass

