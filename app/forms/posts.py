from flask_wtf import FlaskForm
from wtforms import TextAreaField,SubmitField,StringField
from wtforms.validators import DataRequired,Length
class PostForm(FlaskForm):
    #如果要设置指定的属性 可以写 render_kw
    title = StringField('标题', validators=[DataRequired(), Length(6, 30, message="题目长度不符合要求6-30位")])
    content = TextAreaField('',render_kw={'placeholder':'这一刻你想说什么'},validators=[DataRequired(),Length(10,140,message="说话注意分寸在10~140之间")])
    submit = SubmitField("发表")

