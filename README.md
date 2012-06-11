image-extrator
==============

This is a simple web application that is able to extract images from urls and caches them. It's using [Reddit's scrapper code](https://github.com/reddit/reddit/blob/master/r2/r2/lib/scraper.py), with a couple small tweaks, mostly to allow it to run on [Google App Engine](https://developers.google.com/appengine/).

The app provides a single call: <code>/?url=<url></code>, which will return a URL corresponding to the location of that image. Your app should cache that url.
Please note that the URL returned may also be a redirect url, which should 'soon' redirect to the actual image when it's been extracted.
