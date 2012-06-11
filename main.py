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
from scraper import make_scraper #, str_to_image, image_to_str, prepare_image

class MainHandler(webapp2.RequestHandler):
    def get(self):
        if self.request.get("url", ''):
            h = make_scraper(self.request.get("url", ''))
            img = h.largest_image_url()
            
            self.response.out.write(img)
        else:
            # Not much
            self.response.out.write('This is an image extractor application built by <a href="http://superfeedr.com/">Superfeedr</a> for <a href="http://msgboy.com">Msgboy</a>. Check the <a href="">source code</a>, and run your own instance on Google App Engine.')
            

app = webapp2.WSGIApplication([('/', MainHandler)],
                              debug=True)
