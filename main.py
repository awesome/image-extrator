#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import logging

from google.appengine.api import memcache # Cache!
from google.appengine.api import taskqueue # Queue Worker to extract the images...

from scraper import make_scraper
import base64

class MainHandler(webapp2.RequestHandler):
    def get(self):
        if self.request.get("url", ''):
            b64 = base64.b64encode(self.request.get("url", ''));
            img = memcache.get(b64)
            if img is not None:
                self.response.out.write(img)
            else :
                taskqueue.add(url='/worker', params={'url': self.request.get("url", '')})
                self.response.out.write('http://' + self.request.host  + '/r/' + b64)
        else:
            self.response.out.write('This is an image extractor application built by <a href="http://superfeedr.com/">Superfeedr</a> for <a href="http://msgboy.com">Msgboy</a>. Check the <a href="">source code</a>, and run your own instance on Google App Engine.')


class ExtractWorker(webapp2.RequestHandler):
    def post(self): # should run at most 1/s
        url = self.request.get('url')
        b64 = base64.b64encode(url);
        h = make_scraper(url)
        img = h.largest_image_url()
        logging.info('Image for %s found: %s', url, img)
        if img is None:
            # We want to set a value anyway... to avoid people asking for that url again over and over.
            memcache.set(b64, "", 86400)        
        else:
            memcache.set(b64, img, 86400)        


class RedirectHandler(webapp2.RequestHandler):
    def get(self, b64):
        img = memcache.get(b64)
        if img is not None:
            self.redirect(img.encode('ascii','ignore'))
        else :
            self.response.out.write("Wait a bit plz!")        


app = webapp2.WSGIApplication([ ('/', MainHandler), 
                                ('/r/(.*)', RedirectHandler),
                                ('/worker', ExtractWorker),
                              ], debug=True)
