from flask import *
from form import *
from werkzeug.security import generate_password_hash, check_password_hash
import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
from flask_socketio import SocketIO
import time
import datetime


from json import JSONEncoder

# config

app = Flask(__name__)
app.secret_key = 'you will never guess'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///' + os.path.join(app.root_path, 'dataRecord.db'))
db = SQLAlchemy(app)
socketio = SocketIO(app)

from model import Users,Admin,MsgHistory,ChangeFormat

# user pages
@app.route('/index')
def index():
    form = indexSearchForm()
    return render_template("index.html", form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    phone = form.phoneNumber.data

    # if the form can be submit
    if form.validate_on_submit():
        user_in_db = Users.query.filter(Users.phoneNumber == phone).first()
        if not user_in_db:
            redirect(url_for('login'))
        if not check_password_hash(user_in_db.password, form.password.data):
            redirect(url_for('login'))
        session["PHONE"] = phone
        session["USER"] = user_in_db.realName
        return redirect(url_for('index'))
    flash(form.errors)
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        password_hash = generate_password_hash(form.password.data)
        user = Users(phoneNumber=form.phoneNumber.data, nickName=form.fullName.data, realName="", Sex="", Profile="", password=password_hash)
        try:
            db.session.add(user)
            db.session.commit()
            session["PHONE"] = form.phoneNumber.data
            session["USER"] = form.fullName.data
            return redirect('/index')
        except Exception:
            flash("You should change another email")
            return redirect('/register')
    else:
        redirect('/register')
    return render_template("register.html", form=form)

@app.route('/search/<int:id>')
def item_search(id):
    returnMessage = '<h1>search result of %s</h1>' % id
    return render_template("search.html", returnMessage=returnMessage)

@app.route('/', defaults={'id':"000"})
@app.route('/<int:id>')
def item_intro(id):
    returnMessage = '<h1>item intro %s</h1>' % id
    return render_template("item_intro.html", returnMessage=returnMessage)


@app.route('/user_center')
def user_center():
    returnMessage = '<h1>user center</h1>'
    return render_template("user_center.html", returnMessage=returnMessage)


@app.route('/shopping_cart')
def shopping_cart():
    return render_template('shopping_cart.html')


@app.route('/user_sendMessage')
def user_sendMessage():
    if session.get("USER") is None:
        return redirect('/login')
    else:
        getUserName = session.get("USER") 
        chatUser = Users.query.filter(Users.realName == getUserName).first()
        chatMessage = MsgHistory.query.filter(or_(MsgHistory.Sender == chatUser.realName,MsgHistory.Receiver == chatUser.realName)).order_by(MsgHistory.sendTime).all()
    # user_messages = {}
    # timelist=[]
    # for chatmsg in chatMessage:
    #     timelist.append(chatmsg.SendTime)
    # timelist=sorted(timelist,key=lambda date:get_list(date))
    # print(timelist)
    # adminChatMessage = MsgHistoryStaff.query.filter(MsgHistoryStaff.Receiver == chatUser.realName).order_by(MsgHistoryStaff.staffSendTime).all()
    # combine_messages = chatMessage+adminChatMessage
    # sort 一下子
    # for c in chatMessage:
    #     user_messages[c.Sender]=c.Message
    # print('===============')
    # print(type(chatMessage))
    # print(len(chatMessage))
    # user_messages = [{'sender': 'user', 'text': 'lalala', 'ts': ''}]
    # admin_messages = [{'sender': 'admin', 'text': 'lalala', 'ts': ''}]
    # combined_messages = user_messages + admin_messages

    # json = {
    #     messages: [{'sender': 'user', 'text': 'lalala'}]
    # }
    # return render_template('user_sendMessage.html', data=json)
    return render_template('user_sendMessage.html',chatMessage = chatMessage)

judgeAdmin = 0
session_ids = {}
admin_session_id = ''
@socketio.on('connect')
def handle_connect():
    global onlineUser
    global admin_session_id
    d = request.args.to_dict()
    if 'source' not in d:
        print(request.args.to_dict())
        print('=================')
    else:
        source = d['source']
        # print('###########')
        # print(source)
    session_id = request.sid
    if source == 'user' and session.get("USER")!= None:
        session_ids[session_id] = session.get("USER")
        # print(session_ids)
        # for ids in session_ids:
        #     onlineUser.append(str(session_ids[ids]))
        # print(onlineUser)
        print("=========userSessionId==========")
        print(session_id)
        socketio.emit('sendback_session_id',session_id,to=session_id)
        socketio.emit('sendback_session_name',session_ids[session_id],to=session_id)
    else:
        admin_session_id = request.sid
        # print("adminSession" + admin_session_id)
        # print()
        # session_ids[admin_session_id] = session.get("Admin")
        socketio.emit('refresh_users',list(session_ids.values()),to=admin_session_id)
        socketio.emit('refresh_usersids',list(session_ids.keys()),to=admin_session_id)
    

@socketio.on('disconnect')
def handle_disconnect():
    global session_ids
    global admin_session_id
    session_id=request.sid
    index=0
    del session_ids[session_id]
    # if(session_id in session_ids.keys()):
    #     while len(onlineUser)!=0 and index < len(onlineUser):
    #         if onlineUser[index] == session_ids[session_id]:
    #             onlineUser.remove(session_ids[session_id])
    #         index=index+1
    #         print(index)
    #         print(len(onlineUser))

    #     print(session_ids)
    #     print(onlineUser)
    
    socketio.emit('refresh_users',session_ids,to=admin_session_id)    


# admin pages
@app.route('/admin')
def admin():
    returnMessage = '<h1>This is the admin page</h1>'
    return render_template("admin.html", returnMessage=returnMessage)


@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    form = AdminLoginForm()
    if form.validate_on_submit():
        adminNumber = form.userName.data
        user_in_db = Admin.query.filter(Admin.adminNumber == adminNumber).first()
        if not user_in_db:
            redirect(url_for('admin_login'))
        if not check_password_hash(user_in_db.adminPassword, form.password.data):
            redirect(url_for("admin_login"))
        session["Admin"] = adminNumber
        return redirect(url_for("admin"))
        judgeAdmin = 1
    flash("Welcome back ", session.get("Admin"))
    return render_template("admin_login.html", form=form)


@app.route('/admin/item_management')
def admin_item_management():
    navState = 1 
    returnMessage = '<h1>This is the management page</h1>'
    return render_template("admin_item_management.html", returnMessage=returnMessage,navState=navState)


@app.route('/admin/message',methods=['GET', 'POST'])
def admin_message():
    navState = 0
    #python 从js获取用户名。读取button按钮上的字直接就是chatUser.realName
    # global chatToUser
    # chatToUser = "a"
    getUserName = session.get("USER")
    chatUser = Users.query.filter(Users.realName == getUserName).first()
    chatMessage = MsgHistory.query.filter(or_(MsgHistory.Sender == chatUser.realName,MsgHistory.Receiver == chatUser.realName)).order_by(MsgHistory.sendTime).all()
    return render_template("admin_message.html", chatMessage = chatMessage,navState=navState)


@app.route('/admin/change_category')
def admin_change_category():
    navState = 0
    returnMessage = '<h1>change category</h1>'
    return render_template('admin_change_category.html', returnMessage=returnMessage,navState=navState)

@app.route('/admin/change_format')
def admin_change_format():
    navState = 0
    returnMessage = '<h1>change format</h1>'
    return render_template('admin_change_format.html', returnMessage=returnMessage,navState=navState)

@app.route('/admin/order_info')
def admin_order_info():
    navState = 1
    returnMessage = '<h1>order info</h1>'
    return render_template("admin_order_info.html", returnMessage=returnMessage,navState=navState)


#jquery check phone number
@app.route('/registerCheckPhoneNumber', methods=['POST'])
def registerCheckEmail():
    time.sleep(1)
    chosen_name = request.form['email']
    user_in_db = Users.query.filter(Users.nickName == chosen_name).first()
    if not user_in_db:
        return jsonify({'text': 'Cool!', 'returnvalue': 0})
    else:
        return jsonify(({'text': 'Please check your phone number.', 'returnvalue': 1}))


@app.route('/loginCheckPhoneNumber', methods=['POST'])
def loginCheckEmail():
    time.sleep(1)
    chosen_name = request.form['email']
    user_in_db = Users.query.filter(Users.phoneNumber == chosen_name).first()
    if not user_in_db:
        return jsonify({'text': 'Please check your phone number.', 'returnvalue': 1})
    else:
        return jsonify(({'text': 'Cool!', 'returnvalue': 0}))

def messageReceived(methods=['GET','POST']):
	print('message was reveived!!!')

@socketio.on('my event')
def handle_my_custom_event(json,methods=['GET','POST']):
    print('here')
    localtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    # myMessage = (str(json))[13:-2]
    # 判断是不是管理员，filter那个表。如果结果不存在，就存在MsgHistory里，else存在MsgHistoryAdmin里
    print(json['message'])
    print(json)
    session_id = json['sid']
    print("++++++++++++=admin_session_id+++++++++++")
    print(admin_session_id)
    if admin_session_id != '':
        socketio.emit('my response',json,callback=messageReceived, to=admin_session_id)
    message = MsgHistory(Sender = json['name'],Message = json['message'], sendTime = localtime, Receiver='admin')
    db.session.add(message)
    db.session.commit()
    # emit()函数是用来reply message

@socketio.on('admin event')
def handle_my_custom_event(json,methods=['GET','POST']):
    print('here')
    localtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    # print(json['name'])
    # myMessage = (str(json))[13:-2]
    # 判断是不是管理员，filter那个表。如果结果不存在，就存在MsgHistory里，else存在MsgHistoryAdmin里
    message = MsgHistory(Sender = 'admin',Message = json['message'], sendTime = localtime, Receiver=json['name'])
    db.session.add(message)
    db.session.commit()
    # print(json)
    # print('reveived my event:' + json['message'])
    # print('received my session id' + json['sid'])
    session_id = json['session_id']
    socketio.emit('my response',json,callback=messageReceived, to=session_id)

# @socketio.on('user history')
# def user_history(username,methods=['GET','POST']):
#     print("==============userHistory Name+++++++++++++")
#     print(username)
#     user = username
#     redirect(url_for('showUserHistory',key=user))

# @app.route('/admin/message/?<key>',methods=['GET', 'POST'])
# def showUserHistory(key):
#     navState = 0
#     print("=============key============")
#     print(key)
#     chatUser = Users.query.filter(Users.realName == key).first()
#     chatMessage = MsgHistory.query.filter(or_(MsgHistory.Sender == chatUser.realName,MsgHistory.Receiver == chatUser.realName)).order_by(MsgHistory.sendTime).all()
#     return render_template("admin_message.html", chatMessage = chatMessage,navState=navState)

@socketio.on('user history')
def user_history(json2):
    print("==============userHistory Name+++++++++++++")
    print(json2)
    print(json2['username'])
    print(json2['session_id'])
    username = json2['username']
    navState = 0
    chatUser = Users.query.filter(Users.realName == username).first()
    chatMessage = MsgHistory.query.filter(or_(MsgHistory.Sender == chatUser.realName,MsgHistory.Receiver == chatUser.realName)).order_by(MsgHistory.sendTime).all()
    print(chatMessage)

    j = []
    for m in chatMessage:
        j.append(m.as_dict())
    session_id = json2['session_id']
    socketio.emit('refresh message',j,callback=messageReceived, to=admin_session_id)




if __name__ =='__main__':
	socketio.run(app,debug=True)