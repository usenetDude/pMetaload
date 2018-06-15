import os

class Config(object):
    DEBUG = False
    TESTING = False
    SELENIUMURL = os.getenv("SELENIUMURL", 'http://selenium:4444/wd/hub')
    BROWSEROOT = os.getenv("BROWSEROOT", '/video')