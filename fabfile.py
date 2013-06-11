from fabric.api import *

from app import db


def create_db():
    print 'Creating database...'
    with settings(warn_only=True):
        local('rm /tmp/test.db')
    db.create_all()
