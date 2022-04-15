from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash
from app import db,login
from flask_login import UserMixin
from hashlib import md5

followers=db.Table('followers',
                   db.Column('follower_id',db.Integer,db.ForeignKey('user.id')),
                   db.Column('followed_id',db.Integer,db.ForeignKey('user.id')))

class User(UserMixin,db.Model): # tutorial 5 -usermixin
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(64),index=True,unique=True)
    email=db.Column(db.String(120),index=True,unique=True)
    password_hash=db.Column(db.String(128))
    posts=db.relationship('Post',backref='author',lazy='dynamic') # User 생성시에 posts는 입력하지 않음,걍 relationship임(line45와 비교)
    about_me=db.Column(db.String(140))
    last_seen=db.Column(db.DateTime,default=datetime.utcnow)
    followed=db.relationship(
        'User',secondary=followers,
        primaryjoin=(followers.c.follower_id==id), # 팬(follower)
        secondaryjoin=(followers.c.followed_id==id), # 연예인(followed)
        backref=db.backref('followers',lazy='dynamic'),lazy='dynamic'#
    )
    def __repr__(self):
        return '<User {}>'.format(self.username)
    
    def set_password(self,password):
        self.password_hash=generate_password_hash(password)
    
    def check_password(self,password):
        return check_password_hash(self.password_hash,password)
    
    def avatar(self,size):
        digest=md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest,size)
    
    def follow(self,user):
        if not self.is_following(user):
            self.followed.append(user)
            
    def unfollow(self,user):
        if self.is_following(user):
           self.followed.remove(user) 
    
    def is_following(self,user):
        return self.followed.filter(
            followers.c.followed_id==user.id).count()>0
    
    def followed_posts(self):
        followed= Post.query.join( # after join: 전체 post 테이블에 follower id가 추가됨.
            followers,(followers.c.followed_id==Post.user_id)).filter( 
                followers.c.follower_id==self.id)
        own=Post.query.filter_by(user_id=self.id)
        return followed.union(own).order_by(Post.timestamp.desc()) # after filter: 이 함수를 쓸 follower user가 follow한 포스트 테이블만 추려짐
                    # after order_by:timestamp별로 sorted
        

@login.user_loader # tutorial 5 - every time when logged in user navigates to new page, flask-login retrieves id of him from the session and load it into memory
def load_user(id):# bc flask-login know nothing about db, so user_loader helps the extention to load a user
    return User.query.get(int(id)) 
   
class Post(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    body=db.Column(db.String(140))
    timestamp=db.Column(db.DateTime,index=True,default=datetime.utcnow)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id')) # user_id는 Post를 생성할 때 필수로 입력해야 함.
    
    def __repr__(self):
        return '<Post {}>'.format(self.body)

# flask db init 을 터미널에서 실행함으로서 현재 빈 db schema가 생성됨 
# migration repository가 생겼다