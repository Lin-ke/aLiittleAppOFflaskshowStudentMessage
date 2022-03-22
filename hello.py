from ast import parse
from flask_bootstrap import Bootstrap
from flask import Flask, redirect, render_template, request, session, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField,SelectField 
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine

app = Flask(__name__)#程序运行在哪个模块中
bootstrap = Bootstrap(app)
#print(__name__)#运行时他显示hello
app.config['SECRET_KEY'] = 'hard to guess string' #初始化wtf
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db = SQLAlchemy(app)
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'],
    echo=False)

# Student 表
class Student(db.Model):
    num = db.Column(db.String(20), primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    age = db.Column(db.Integer, unique=False, nullable=False)
    ssex = db.Column(db.String(10),nullable = False)
    cls = db.Column(db.String(30),nullable = False)
    depart = db.Column(db.String(30),nullable = False)
    addr = db.Column(db.String(80),nullable = False)
contribs = ["学号","姓名","年龄","性别","班","系","地址"]
#建立一个格式，适用于固定的模式
class InputForm(FlaskForm):
    num = StringField("学号")
    name = StringField('姓名')
    age1 = StringField('年龄起始(包括)')#IntegerField需要这个数非空
    age2 = StringField("到(包括)")
    sex = SelectField(choices=("空","男","女"),label = "性别")
    cls = StringField('班') #TODO: 这个也可以整成联动的 比如省市区这样
    dpt = StringField('系')
    addr = StringField("地址")
    submit = SubmitField("查询")
    dlt = SubmitField("删除")
#todo: 根据读入的数据修改提交类。或者每个读入后面跟一个框！

def readData(str):
    new_list = []
    with engine.connect() as conn:
        res = conn.execute(str)
        list = res.all()
    for tuple in list:
        new_tuple = []
        for ele in tuple:
            new_tuple.append(ele)
        new_list.append(new_tuple)
    print(new_list)
    #TODO:优化此处逻辑
    return new_list 
#对于一般的字符串适用
@app.route('/',methods = ['GET','POST'])
def index():
    typeList = ["num","name","age1","age2","ssex","cls","depart","addr","submit","delete"]
    result = []
    form = InputForm()
    if request.method == "POST" and form.validate():
        paraList = [form.num.data,form.name.data,form.age1.data,
        form.age2.data,form.sex.data,
        form.cls.data,form.dpt.data,form.addr.data,
        form.submit.data,form.dlt.data]
        #开始写入
        str = changeSth(typeList,paraList)
        result = readData(str)
        session["sql_sentense"] = str
        session["sql_result"] = result
        return redirect(url_for('index')) # 用视图函数的名字,重定向后用get方法
    return render_template("user.html",str = session.get("sql_sentense"),form = form,results = session.get("sql_result"),paraList = contribs)
def changeSth(types,paras):
    str = " * from student where "
    fst = True
    for i in range(len(types)-2):
        if types[i] == "ssex":
            if paras[i] == "空":
                paras[i] = ""
        if paras[i] != "":
            if(fst == False):
                str+="and "
            else: fst = False

            if types[i] == "age1":
                str+="age>="+paras[i]+" "
            elif types[i] == "age2":
                str+="age<="+paras[i]+" "
                
            else: str +=types[i]+"="+"\""+paras[i]+"\" "
    if(paras[len(types)-2] == True):
        str = "select"+str
    else : str = "delete"+str
    str = str.strip()
    str+=";"
    if fst == True:
        return "select * from student;"
    return str
@app.route('/all/')
def viewall():
    return