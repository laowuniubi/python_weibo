from app.exts import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask import current_app,flash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_login import UserMixin
from app.exts import login_manager
from .posts import Posts
#UserMixin 查看该用户是否登录 以及 是否是匿名用户

class User(UserMixin,db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True,nullable=False)
    username = db.Column(db.String(50),nullable=False,unique=True)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(128),nullable=False)
    confirmed = db.Column(db.Boolean,default=False)
    icon = db.Column(db.String(64),default='default.jpg')
    #lazy 在这里是懒加载 dynamic表示不加载数据但是提供查询
    #如果一对一的关系 需要加上 uselist=Flase
    posts = db.relationship("Posts",backref="user",lazy="dynamic")
    favorites = db.relationship('Posts', secondary='collections', backref=db.backref('useres', lazy='dynamic'),lazy='dynamic')

    # 添加收藏功能
    # 判断用户是否收藏了
    def is_favorite(self, pid):
        # 先获取所有收藏的博客
        favorites = self.favorites.all()
        post = list(filter(lambda p: p.id == pid, favorites))
        if len(post) > 0:
            return True
        return False

    # 添加收藏功能
    def add_favorite(self, pid):
        p = Posts.query.get(pid)  # 先根据id 查询出来
        self.favorites.append(p)  # 然后追加到 第三张表中

    # 取消收藏功能
    def del_favorite(self, pid):
        p = Posts.query.get(pid)  # 先根据id 查询出来
        self.favorites.remove(p)  # 从第三张表中 移除
    #当前用户通过 user 访问 posts 表中的字段
    #密码不能读 而且永不返回
    @property
    def password(self):
        raise AttributeError("密码不可读的帅哥")

    #设置密码的时候  保存的是加密后的hash值
    @password.setter
    def password(self,password):
        self.password_hash = generate_password_hash(password)

    #校验密码是否正确 正确 true 错误 false
    #先加密 再跟数据库比较
    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)

    #生成token   通过邮箱发送给用户
    def generate_active_token(self,expires_in=3600):
        s = Serializer(current_app.config['SECRET_KEY'],expires_in=expires_in)
        return s.dumps({'id':self.id})

    # 验证token 方法
    @staticmethod
    def check_active_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        #这个id是从 token中解析出来的  然后根据id 到数据库中查找  对应的数据进行更新
        u = User.query.get(data.get('id'))
        if not u:
            flash("该用户不存在")
            return False
        if not u.confirmed:
            u.confirmed = True
            db.session.add(u)
        return True

#登录成功以后 执行以下方法 回调函数 获取登录用户的相关信息
@login_manager.user_loader
def load_user(uid):
    return User.query.get(int(uid))




