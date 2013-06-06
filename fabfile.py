from fabric.api import *

from aeemaps import db


def create_db():
    print 'Creating database...'
    local('rm /tmp/test.db')
    db.create_all()
