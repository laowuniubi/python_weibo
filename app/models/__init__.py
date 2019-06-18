from .users import User
from .posts import Posts
from app.exts import db

#添加用户与帖子的收藏中间表
collections = db.Table('collections',
    db.Column('user_id',db.Integer,db.ForeignKey('user.id')),
    db.Column('posts_id',db.Integer,db.ForeignKey('posts.id'))
)