# vim: fileencoding=utf-8
import logging

from pylons import request, response, session, tmpl_context as c, config
from pylons.controllers.util import abort, redirect_to
from pylons.decorators import jsonify, validate
from pylons.decorators.rest import restrict
import nitrol.model as model
from nitrol.model import meta
import formencode
import nitrol.lib.helpers as h


from nitrol.lib.base import BaseController, render

import smtplib as smtp
from email.mime.text import MIMEText
import string
import random as rnd

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
    email = formencode.validators.Email()
    egf = formencode.validators.Int() 

class PlayersController(BaseController):
    """This controller does all the player manipulation
    Meant to be used with Ajax"""

    @jsonify
    def getindex(self):
        """Get players in JSON format"""
        players = [dict(plr) for plr in meta.Session.query(model.Player).all()]
        return {'success': True, 'data': players}

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

        player.confirmed = False
        self._sendConfirmMail(player)

        meta.Session.add(player)
        meta.Session.commit()
        return {'success': True}

    def confirm(self, id, code):
        player = meta.Session.query(model.Player).filter(model.Player.id == id).one()
        if code == player.code:
            player.confirmed = True
        meta.Session.add(player)
        meta.Session.commit()
        c.player = player
        redirect_to('/')

    def _sendConfirmMail(self, player):
        ch = string.letters + string.digits
        player.confirmation_code = ''.join(rnd.choice(ch) for i in range (32))
        email_data = {}
        for fld in ['first_name', 'last_name', 'rank', 'club']:
            email_data[fld] = getattr(player, fld)
        email_data['confirmation_link'] = h.url_for(controller = 'players', 
                action = 'confirm', id = player.id, 
                code = player.confirmation_code,
                qualified = True)
        email_data['tournament_name'] = config.get('nitrol.tournament.name')
        email_data['tournament_url'] = config.get('nitrol.tournament.url')
        for  d in email_data:
            setattr(c, d, email_data[d])

        conf_mail = MIMEText(render('conf_mail.html').encode('utf-8'), 'html', 'utf-8')
        conf_mail['from'] = config.get('nitrol.email.from')
        conf_mail['to'] = player.email
        conf_mail['Subject'] = 'Potwierdzenie uczestnictwa w turnieju'

        s = smtp.SMTP()
        s.connect()
        s.sendmail(config.get('nitrol.email.from'), [player.email], conf_mail.as_string())
        s.quit()





