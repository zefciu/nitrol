import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to
from pylons.decorators import jsonify
import unicodedata
import re
import httplib
import urllib

from nitrol.lib.base import BaseController, render

log = logging.getLogger(__name__)

class EgdController(BaseController):
    """Improved Ajax proxy for European Go Database. Solves the cross-site issue
    and also manipulates the data a little"""

    def __init__(self, *args, **kwargs):
        super(EgdController, self).__init__(*args, **kwargs)
        self.reCombining = re.compile(u'[\u0300-\u036f\u1dc0-\u1dff\u20d0-\u20ff\ufe20-\ufe2f]',re.U)

    def fetchJsonData(self):
        last_name = request.params['query']
        stripped = self.__remove_diacritics(last_name)
        conn = httplib.HTTPConnection('www.europeangodatabase.eu')
        params = urllib.urlencode({'lastname': stripped})
        conn.request('GET', '/EGD/GetPlayerDataByData.php?' + params)
        resp = conn.getresponse()
        return resp.read()

    def __remove_diacritics(self, s):
        """Decomposes string, then removes combining characters"""
        return self.reCombining.sub('',unicodedata.normalize('NFD',unicode(s)))
