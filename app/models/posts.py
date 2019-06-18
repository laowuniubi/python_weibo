from app.exts import db
from datetime import datetime
class Posts(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    title=db.Column(db.String(64))
    content=db.Column(db.Text)
    timestamp = db.Column(db.DateTime,default=datetime.utcnow())
    rid = db.Column(db.Integer,index=True,default=0)
    uid = db.Column(db.Integer,db.ForeignKey('user.id'))




