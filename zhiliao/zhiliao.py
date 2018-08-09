from flask import (
    Flask,
    render_template,
    redirect,
    request,
    url_for,
    session,
    escape,
    flash,
)
from werkzeug.security import generate_password_hash,check_password_hash
import config
from exts import db
from models import *
from decorators import login_requird

app = Flask(__name__)
app.config.from_object(config)
app.config["SESSION_PERMANENT"] = True
db.init_app(app)

#主页面,用户发布问答文章显示的区域
@app.route("/")
def index():
    #将查询的所有的文章,作者id查询结果渲染到模板中
    question = Question.query.order_by('-create_time').all()
    print(request.script_root)
    return render_template("index.html",question=question,request=request)

#登录页面处理函数
@app.route("/login/",methods=["GET","POST"])
def login():
    '''
    get访问时,将登录模板渲染回页面
    post访问时,将表单数据和数据里面的值进行比对
    '''
    if request.method == "GET":
        return render_template("login.html")
    else:
        username= request.form.get("username","")
        print(username)
        password = request.form.get("password","")
        #如果输入为空,则返回错误信息,msg可以换为flash
        if username == "" or password == "":
            msg = "输入不能为空"
            return render_template("login.html",msg = msg)
        else:
            #输入不为空,将用户输入的用户名和密码放到数据库进行查询
            result = User.query.filter(User.username==username).first()
            if result:
                if check_password_hash(result.password,password):
                    #成功登录,则将用户的id存在session中,然后用钩子函数,传到base模板中
                    session["user_id"] = result.id
                    return redirect(url_for("index"))
                else:
                    msg = "用户名或密码错误"
                    return render_template("login.html",msg=msg)
            else:
                msg = "用户名或密码错误"
                return render_template("login.html", msg=msg)

@app.route("/register/",methods=["GET","POST"])
def register():
    msg = ""
    if request.method == "GET":
        return render_template("register.html", msg=msg)
    else:
        user_name = request.form.get("userName", "")
        password = request.form.get("pwd", "")
        cpwd = request.form.get("cpwd", "")
        phone_num = request.form.get("phoneNum", "")

        if not (user_name and password and cpwd and phone_num):
            msg = "输入不能为空"
            return render_template("register.html", msg=msg)
        elif password != cpwd:
            msg = "密码输入不一致"
            return render_template("register.html", msg=msg)
        else:
            userinfo = User.query.filter(User.username == user_name).first()
            p_num =  User.query.filter( User.phonenum == phone_num).first()
            if not (userinfo or p_num):
                add_user =  User(username=user_name, password=generate_password_hash(password),phonenum=phone_num)
                db.session.add(add_user)
                db.session.commit()

                return redirect(url_for('login'))
            else:
                if userinfo:
                    msg = "用户名已被注册"
                    return render_template("register.html", msg=msg)
                elif p_num:
                    msg = "手机号已被注册"
                    return render_template("register.html", msg=msg)
@app.route("/logout/")
def logout():
    #----删除session会话的方法-------!
    #session.pop("user_id")
    session.clear()
    # del session["user_id"]
    return redirect(url_for("login"))

@app.context_processor
def handler_session():
    if session.get("user_id"):
        username = User.query.filter(User.id==session.get("user_id")).first()
        return {"user":username}
    else:
        return {"user":None}

@app.route("/question/",methods=["GET","POST"])
@login_requird
def question():
    if request.method =="GET":
        return render_template("question.html")
    else:
        title = request.form.get("title")
        content= request.form.get("content")
        if title == "" or content =="":
            flash("输入内容不能为空")
            return render_template("question.html")
        question = Question(title=title,content=content)
        user = User.query.filter(User.id==session["user_id"]).first().id
        question.author_id=user
        db.session.add(question)
        db.session.commit()
        return redirect(url_for("index"))

@app.route("/detail/<question_id>",methods=["GET","POST"])
@login_requird
def detail(question_id):
    msg = ""
    question = Question.query.filter(Question.id == question_id).first()
    comment = Comment.query.order_by("-create_time").filter(Comment.question_id == question_id,Comment.is_ban==1).all()
    if request.method == "GET":
        return render_template("detail.html",question=question,comment=comment,msg=msg)
    else:

        comment = request.form.get("comment")
        if comment:
            add_data = Comment(content=comment,user_id=session.get("user_id"),question_id=question_id)
            db.session.add(add_data)
            db.session.commit()
            return redirect(url_for("detail",question_id=question_id))
        else:
            flash("输入不能为空")
            return redirect(url_for("detail",question_id=question_id))


@app.route("/delete_comment/<comment_id>/<question_id>",methods=["GET","POST"])
def delete_comment(comment_id,question_id):
    comment = Comment.query.filter(Comment.id==comment_id).first()
    comment.is_ban = False
    db.session.add(comment)
    db.session.commit()
    question = Question.query.filter(Question.id == question_id).first()
    comment = Comment.query.order_by("-create_time").filter(Comment.question_id == question_id,
                                                            Comment.is_ban == 1).all()
    return redirect(url_for("detail",question_id=question_id,question=question,comment=comment))

@app.route("/form-test/",methods=["GET","POST"])
def form_test():
    if request.method =="GET":
        return render_template("test_.html")
    else:
        return "数据提交成功"

#之前密码没有加密,现在全部遍历一遍,然后全部修改加密后,重新存入数据库
@app.route("/add_secret/")
def add_secret():
    user = User.query.all()
    for i in user:
        i.password = generate_password_hash(i.password)
        db.session.add(i)
        db.session.commit()
    return "测试"

#注册时,将前端ajax传送回来的json数据进行查询
@app.route("/ajaxHandler/",methods=["GET","POST"])
def ajaxHandler():
    username = request.get_json()
    if User.query.filter(User.username==username).first():
        return "no"
    status = True
    return "ok"

if __name__ == "__main__":
    app.run(host='176.130.2.168',port=8000)

