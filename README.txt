NiTROL stands for Nice Tournament Registration Open List

This is a simple web app used for registration in Go tournaments

Installation and Setup
======================

Install ``nitrol`` using easy_install::

    easy_install nitrol

Make a config file as follows::

    paster make-config nitrol config.ini

In the config file specify:
nitrol.email.from = 'From' for the confirmation mails
nitrol.tournament.name = Tournament name for confirmation mails
nitrol.tournament.url = Tournament url for confirmation mails

Tweak the config file as appropriate and then setup the application::

    paster setup-app config.ini

Then you are ready to go.
