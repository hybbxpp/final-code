from __future__ import unicode_literals
from flask import jsonify, flash, session
from flask_cors import CORS
from xwtools.neo4j_op import Neo4jOp
import re, datetime, math
from dateutil import tz
from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
import os

from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.config['SECRET_KEY'] = '123456'
app.config['JSON_AS_ASCII'] = False
app.jinja_env.auto_reload = True
CORS(app, supports_credentials=True)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,'app.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    username = db.Column(db.String(64), unique=True)
    _password = db.Column(db.String(128))

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = generate_password_hash(value)

    def check_password(self, user_pad):
        return check_password_hash(self._password, user_pad)

class Name(db.Model):
    __tablename__ = 'name'
    name = db.Column(db.String(64), primary_key=True, index=True)

class Daily(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    drug = db.Column(db.String(64), index=True)
    question = db.Column(db.String(64), index=True)
    way = db.Column(db.String(64), index=True)
    time = db.Column(db.DateTime, index=True)

#db.drop_all()
db.create_all()



with open('./build_graph/data/regexp_name.txt', 'r', encoding='utf-8') as fp:
    data = fp.read().strip().replace('(', '').replace(')', '')

entity_regexp = re.compile(data)

relation_map = {
    '成分': '主要成份', '包含': '主要成份', '含什么成份': '主要成份', '元素': '主要成份', '内含': '主要成份', '包括': '主要成份', '东西': '主要成份', '玩意': '主要成份',
    '什么样': '性状', '啥样': '性状', '特征': '性状', '特点': '性状', '味': '性状', '表征': '性状', '形式': '性状', '液体': '性状', '液态': '性状', '固体': '性状', '固态': '性状', '气体': '性状', '气态': '性状',
    '功能': '主治功能', '功效': '主治功能', '效果': '主治功能', '作用': '主治功能', '什么用': '主治功能', '啥用': '主治功能', '干嘛用': '主治功能',
    '怎么': '用法用量', '如何': '用法用量', '吃多少': '用法用量', '量': '用法用量',
    '副': '不良反应', '不好': '不良反应', '坏': '不良反应', '反': '不良反应', '不适': '不良反应', '不舒服': '不良反应',
    '久': '有效期', '时间': '有效期', '天': '有效期', '月': '有效期', '年': '有效期', '期限': '有效期',
    '产': '生产商', '来': '生产商',
    '存': '贮藏方式', '放': '贮藏方式', '搁': '贮藏方式',
    '心': '注意',
    '治': '适应症',
    '孕': '孕妇用药', '怀': '孕妇用药', '有孩子': '孕妇用药', '有宝宝': '孕妇用药',
    '儿童': '儿童用药', '孩子': '儿童用药', '小孩': '儿童用药',
    '老': '老人用法', '年纪大': '老人用法', '年龄大': '老人用法',
    '过激': '药物过量', '过敏': '药物过量'
}

relation_regexp = re.compile('主要成份|性状|主治功能|用法用量|不良反应|有效期|生产商|贮藏方式|注意|规格|批准文号|适应症|孕妇用药|儿童用药|老人用法|药物过量|警告|临床研究' + '|' + '|'.join(relation_map.keys()))

def get_question_entity(question):
    entity_list = entity_regexp.findall(question)
    if entity_list:
        return entity_list[0]

def get_question_relation(question):
    rel_list = relation_regexp.findall(question)
    if rel_list:
        rel = rel_list[0]
        if relation_map.get(rel):
            rel = relation_map[rel]
        return rel

op_neo4j = Neo4jOp(label='neo4j')
default_answer = "抱歉，没有该问题的相关数据"
def get_answer(question, question_entity, num):
    entity = get_question_entity(question_entity)
    if not entity:
        return default_answer
    relation = get_question_relation(question)
    if not relation:
        return default_answer
    if num:
        tz_sh = tz.gettz('Asia/Shanghai')
        daily = Daily(name=session.get('name'), drug=entity, question=relation, way='问答系统', time=datetime.datetime.now(tz=tz_sh))
        db.session.add(daily)
        db.session.commit()
    r = op_neo4j.run_cql(f"MATCH p=(a:`通用名称`)-[r:`{relation}`]->(b) where a.name='{entity}' RETURN b LIMIT 1")
    _list_graphs = r.data()
    if not _list_graphs: return default_answer
    print(_list_graphs[0]['b']["name"])
    return  _list_graphs[0]['b']["name"]

def is_number(password):
    """判断一个unicode是否是数字"""
    pattern = re.compile('[0-9]+')
    match = pattern.findall(password)
    if match:
        return True
    else:
        return False

def is_lowercase(password):
    """判断一个unicode是否包含小写字母"""
    flag = 0
    for i in password:
        if i.islower() == True:
            flag += 1
    if(flag > 0):
        return True
    else:
        return False


def is_uppercase(password):
    """判断一个unicode是否包含大写字母"""
    flag = 0
    for i in password:
        if i.isupper() == True:
            flag += 1
    if (flag > 0):
        return True
    else:
        return False

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    flash('登出成功', 'success')
    print('Logout successfully')
    return redirect('/')

@app.route('/post', methods=["GET", "POST"])
def get_response():
    if(session.get('name')):
        question = request.values.get('text', '').strip()
        if not question:
            return jsonify({"msg": '问题为空'})
        a = []
        with open('./build_graph/data/trans.txt', 'r', encoding='utf-8-sig') as fp:
            data_list = fp.readlines()
        for i in data_list:
            i = i.rstrip("\n")
            a.append(i)
        for entity in a:
            if entity in question:
                question_entity = question[question.index(entity):]
        answer_str = get_answer(question, question_entity, 1)
        return jsonify({"response": answer_str})
    else:
        flash('清先登录！', 'danger')
        return redirect('/')


@app.route('/robot', methods=["GET"])
def robot():
    if(session.get('name')):
        return render_template('chatrobot.html')
    else:
        flash('清先登录！', 'danger')
        return redirect('/')

@app.route('/register/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        un = request.form['username']
        pd = request.form['password']
        if(len(un)<=64):
            if(len(un)<=64):
                if(User.query.filter(User.username == un).count()==0):
                    if(is_lowercase(pd) == 0):
                        if (is_number(pd) == 0):
                            flash('密码中需要包含数字和小写字母，请重新输入！', 'danger')
                            print('Need number and no lowercase')
                            return redirect('/register/')
                        elif (is_uppercase(pd) == 0):
                            flash('密码中需要包含大写字母和小写字母，请重新输入！', 'danger')
                            print('No uppercase and no lowercase')
                            return redirect('/register/')
                        else:
                            flash('密码中需要包含小写字母，请重新输入！', 'danger')
                            print('No lowercase')
                            return redirect('/register/')
                    elif(is_uppercase(pd) == 0):
                        if (is_number(pd) == 0):
                            flash('密码中需要包含大写字母和数字，请重新输入！', 'danger')
                            print('Need number and no uppercase ')
                            return redirect('/register/')
                        else:
                            flash('密码中需要包含大写字母，请重新输入！', 'danger')
                            print('No uppercase ')
                            return redirect('/register/')
                    elif(is_number(pd) == 0):
                        flash('密码中需要包含数字，请重新输入！', 'danger')
                        print('Need number')
                        return redirect('/register/')
                    else:
                         user = User(name=un, username=un, password=pd)
                         db.session.add(user)
                         db.session.commit()
                         flash('注册成功!请登录', 'success')
                         return redirect('/')
                flash('用户名已存在，请重新输入！', 'danger')
                print('Username already exist')
                print(un)
                print(User.query.filter(User.username == un).count())
                return redirect('/register/')
            else:
                flash('姓名过长，请重新输入！', 'danger')
                print('name is too long')
                return redirect('/register/')
        else:
            flash('用户名过长，请重新输入！', 'danger')
            print('username is too long')
            return redirect('/register/')
    return render_template('register.html')



@app.route('/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        name = request.form['username']
        pawd = request.form['password']
        user = User.query.filter_by(username=name).first()
        if user:
            if user.check_password(pawd):
                session['name'] = name
                return redirect('/user')
            else:
                flash('密码错误', 'danger')
                return render_template("index.html")
        flash('用户不存在！请点击注册按钮注册', 'info')
        return render_template("index.html")

    return render_template("index.html")

@app.route('/transit', methods=['POST', 'GET'])
def transit():
    if(session.get('name')):
        welcome = "欢迎回来, " + session.get('name')
        flash(welcome, 'success')
        return render_template('transit.html')
    else:
        flash('清先登录！', 'danger')
        return redirect('/')

@app.route('/search', methods=['GET', 'POST'])
def web():
    if(session.get('name')):
        if request.method == 'POST':
            line1 = []
            line2 = []
            line3 = []
            hybb = '%'+request.form['drug']+'%'
            list = request.form['drug']
            name = Name.query.filter(Name.name.ilike(hybb)).order_by(Name.name).all()
            number = Name.query.filter(Name.name.ilike(hybb)).count()
            count = math.ceil(number/2)
            count_biggest = math.ceil(number/3)
            count_middle = math.ceil((number-count_biggest)/2)
            count_small = count_biggest + count_middle
            if number == 0:
                flash("没有相关药品！", 'danger')
                return redirect('/search')
            elif number>=0 and number<17:
                for i in range(number):
                    line1.append(name[i])
            elif number>=17 and number<33:
                for i in range(count):
                    line1.append(name[i])
                for j in range(count,number):
                    line2.append(name[j])
            else:
                for i in range(count_biggest):
                    line1.append(name[i])
                for j in range(count_biggest, count_small):
                    line2.append(name[j])
                for k in range(count_small, number):
                    line3.append(name[k])

            return render_template('list.html', name=name, list=list, number=number, line1=line1, line2=line2, line3=line3
                                   )
        return render_template('result.html')
    else:
        flash('清先登录！', 'danger')
        return redirect('/')

@app.route('/drugs/<name>', methods=['GET', 'POST'])
def drugs(name):
    if (session.get('name')):
        element = '主要成份'
        character = '性状'
        function = '功能主治'
        usage = '用法用量'
        untoward = '不良反应'
        indate = '有效期'
        package = '包装规格'
        store = '贮藏'
        disease = '适应症'
        certificate = '批准文号'
        tz_sh = tz.gettz('Asia/Shanghai')
        daily = Daily(name=session.get('name'), drug=name, question='None', way='搜索系统',time=datetime.datetime.now(tz=tz_sh))
        db.session.add(daily)
        db.session.commit()
        return render_template('drugs.html',
            drug = name, element = get_answer(name+element, name+element, 0),
                         character = get_answer(name+character, name+element, 0),
                         function = get_answer(name+function, name+element, 0),
                         usage = get_answer(name+usage, name+element, 0),
                         untoward = get_answer(name+untoward, name+element, 0),
                         indate = get_answer(name+indate, name+element, 0),
                         package = get_answer(name+package, name+element, 0),
                         store = get_answer(name+store, name+element, 0),
                         disease = get_answer(name+disease, name+element, 0),
                         certificate = get_answer(name+certificate, name+element, 0)
                               )
    else:
        flash('清先登录！', 'danger')
        return redirect('/')

@app.route('/user', methods=['GET', 'POST'])
def user():
    if (session.get('name')):
        name = User.query.filter(User.name == session.get('name'))
        return render_template('user.html', user=session.get('name'))
    else:
        flash('清先登录！', 'danger')
        return redirect('/')

@app.route('/daily', methods=['GET', 'POST'])
def daily():
    if (session.get('name')):
        daily = Daily.query.filter(Daily.name == session.get('name')).all()
        return render_template('daily.html', user=session.get('name'), daily=daily)
    else:
        flash('清先登录！', 'danger')
        return redirect('/')

if __name__ == '__main__':
    app.run(debug=True, threaded=True)
