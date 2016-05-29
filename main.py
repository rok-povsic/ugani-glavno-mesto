#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import jinja2
import webapp2
import datetime

from drzava import Drzava

template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)

drzave = [
    Drzava(u"Francija", u"Pariz", "http://www.roomsuggestion.com/userfiles/images/paris.jpg"),
    Drzava(u"Nemčija", u"Berlin", "http://www.berlin49.com/images/edit_image/Ferienwohnung_Berlin_Charlottenburg.jpg"),
    Drzava(u"Združeni arabski emirati", u"Dubaj", "http://7606-presscdn-0-74.pagely.netdna-cdn.com/wp-content/uploads/2016/03/Dubai-Photos-Images-Dubai-UAE-Pictures-800x600.jpg"),
    Drzava(u"Jemen", u"Sana", "https://www.agencija-oskar.si/images/yems/jemen-sarmantni-taiz.jpg"),
    Drzava(u"Kambodža", u"Phnom Penh", "http://www.rupp.edu.kh/erasmus/sat/images/ind.jpg"),
    Drzava(u"Angola", u"Luanda", "http://www.latitude-platform.eu/wp-content/uploads/2013/06/Banco_BPC_Luanda.jpg"),
    Drzava(u"Paragvaj", u"Asuncion", "http://k12.kn3.net/C4064A665.jpg"),
]


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if not params:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        return self.render_template("home.html")


class QuizHandler(BaseHandler):
    def get(self):
        self.vpisi_piskotek(0, 0)

        view_vars = {
            'drzava': drzave[0]
        }

        return self.render_template("kviz.html", view_vars)

    def post(self):
        st_drzave, tocke = self.preberi_piskotek()

        odgovor = self.request.get("answer")

        if odgovor.lower() == drzave[st_drzave].glavno_mesto.lower():
            tocke += 1

        st_drzave += 1

        if st_drzave < len(drzave):
            self.vpisi_piskotek(st_drzave, tocke)

            view_vars = {
                'drzava': drzave[st_drzave]
            }

            return self.render_template("kviz.html", view_vars)
        else:
            view_vars = {
                'tocke': tocke,
                'vse_tocke': len(drzave),
            }

            return self.render_template("rezultat.html", view_vars)


    def vpisi_piskotek(self, st_drzave, tocke):
        value = "%s:%s" % (st_drzave, tocke)
        expires = datetime.datetime.utcnow() + datetime.timedelta(minutes=60)

        self.response.set_cookie("st_drzave_in_tocke", value=value, expires=expires)

    def preberi_piskotek(self):
        st_drzave, tocke = self.request.cookies.get("st_drzave_in_tocke").split(":")
        st_drzave = int(st_drzave)
        tocke = int(tocke)
        return st_drzave, tocke



app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/kviz', QuizHandler),
], debug=True)
