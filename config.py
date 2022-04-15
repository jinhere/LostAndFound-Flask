import os
basedir=os.path.abspath(os.path.dirname(__file__))
class Config(object):
    SECRET_KEY=os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI=os.environ.get('DATABASE_URL') or \
        'sqlite:///'+os.path.join(basedir,'app.db')
    SQLALCHEMY_TRACK_NOTIFICATIONS=False #true로 하면 db에 변경사항있을때마다 알림옴
    POSTS_PER_PAGE=10