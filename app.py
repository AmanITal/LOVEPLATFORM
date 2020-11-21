from flask import Flask, render_template, request, redirect, url_for, session
from models import User, Life, Comments, Hobby, Characters, Friend, Admin
from exts import db
from sqlalchemy import or_
import config
import os
import random
import Mangement
from decorators import login_required, back_login_required
from emotion import compute_model, get_emotion

basedir     =   os.path.abspath(os.path.dirname(__file__))#定义根目录
path        =   basedir+'\\static\\user_img\\'#设置图片保存路径
app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)

#产生随机数列
def randoms():
    count = 0
    ran = ''
    while(count<10):
        i = random.randint(0,9)
        ran = ran + str(i)
        count = count + 1
    return ran

'''
---------------------------------------------------------------------------------------------------
-----------------------------------------------前台------------------------------------------------
---------------------------------------------------------------------------------------------------
'''
#首页
@app.route('/')
def index():
    if 'user_id' in session.keys():
        user    =   User.query.filter(User.id == session.get('user_id')).first()
        gender  =   User.query.filter(User.sex != user.sex).all()
        gender_id = []
        for id in gender:
            gender_id.append(id.id)
        gender_id.append(user.id)
        print(gender_id)
        context = {'life':Life.query.filter(Life.author_id.in_(gender_id)).order_by(db.desc('creat_time')).all()}
        return render_template("index.html", **context)
    else:
        context = {'life':Life.query.order_by(db.desc('creat_time')).all()}
        return render_template("index.html", **context)

#登陆页面
@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':

        return render_template('login.html')
    else:
        phone       =   request.form.get('phone')
        password    =   request.form.get('password')

        user = User.query.filter(User.phone==phone, User.password==password).first()
        if user:
            session['user_id'] = user.id
            return redirect(url_for('index'))
        else:
            return '用户名或密码有误！'

#注册页面
@app.route('/regist/', methods=['GET', 'POST'])
def regist():
    if request.method == 'GET':
        return render_template('regist.html')
    else:
        phone       =   request.form.get('phone')
        username    =   request.form.get('username')
        password1   =   request.form.get('password1')
        password2   =   request.form.get('password2')
        sex         =   request.form.get('sex')

        figure      =   request.files.get('figure')#获取图片

        ran = randoms()
        imgName     =   ran+str(figure.filename)
        img_path    =   path+imgName#合并保存路径和图片名称
        figure.save(img_path)#保存图片
        url         =   '/static/user_img/'+imgName#图片相对路径

        user = User.query.filter(User.phone==phone).first()
        if user:
            return '该手机号已被注册'
        else:
            if (password1 != password2):
                return '密码不一致'
            else:
                if (sex=='男') or (sex=='女'):
                    user = User(phone=phone, username=username, password=password1, sex=sex, img=url)
                    db.session.add(user)
                    db.session.commit()
                    user1 = User.query.filter(User.phone == phone).first()
                    session['user_id'] = user1.id
                    return redirect(url_for('character'))
                else:
                    return '请输入男/女'

#性格测试页面
@app.route('/character/', methods=['GET', 'POST'])
def character():
    if request.method == 'GET':
        return render_template('character.html')
    else:
        #################################
        #爱好
        hobby_model = ''
        content         =   request.values.getlist('hobby')
        if len(content) == 0:
            return '请填写您的兴趣爱好'
        for con in content:
            hobby_model = hobby_model+con+';'
        hobby           =   Hobby(hobby=hobby_model)
        hobby.user_id   =   session.get('user_id')
        db.session.add(hobby)
        db.session.commit()

        ##################################
        #性格
        count = 1
        character_model = dict()
        cha_model = list()
        while(count<=30):
            character_model['name'+str(count)]  =   request.form.get(str(count))
            if character_model['name'+str(count)] == '':
                return '请填写第%s测试题'%str(count)
            count = count+1
        Tiger   =   int(character_model['name5']) + int(character_model['name10']) + int(character_model['name14']) + int(character_model['name18']) + int(character_model['name24']) + int(character_model['name30'])
        Peacock =   int(character_model['name3']) + int(character_model['name6']) + int(character_model['name13']) + int(character_model['name20']) + int(character_model['name22']) + int(character_model['name29'])
        Panda   =   int(character_model['name2']) + int(character_model['name8']) + int(character_model['name15']) + int(character_model['name17']) + int(character_model['name25']) + int(character_model['name28'])
        Owl     =   int(character_model['name1']) + int(character_model['name7']) + int(character_model['name11']) + int(character_model['name16']) + int(character_model['name21']) + int(character_model['name26'])
        Anole   =   int(character_model['name4']) + int(character_model['name9']) + int(character_model['name12']) + int(character_model['name19']) + int(character_model['name23']) + int(character_model['name27'])
        total   =   (Tiger + Peacock + Owl + Anole + Panda)
        aver    =   int(total/5)
        #数据分析
        cha_dict    =   {'Tiger':Tiger, 'Peacock':Peacock, 'Panda':Panda, 'Owl':Owl, 'Anole':Anole}
        cha_sort    =   sorted(cha_dict.items(), key=lambda x: x[1], reverse = True)
        print(cha_sort)
        #cha_model   =   [cha_sort[0][0],cha_sort[1][0],cha_sort[2][0],cha_sort[3][0],cha_sort[4][0]]
        if (int(cha_sort[0][1]) - int(cha_sort[4][1]))<3:
            characters          =   Characters(character='Perfect')
            characters.user_id  =   session.get('user_id')
            db.session.add(characters)
            db.session.commit()
        elif (int(cha_sort[0][1]) - int(cha_sort[1][1])) >= (int(cha_sort[1][1]) - int(cha_sort[2][1])):
            characters          =   Characters(character=str(cha_sort[0][0]))
            characters.user_id  = session.get('user_id')
            db.session.add(characters)
            db.session.commit()
        else:
            characters          =   Characters(character=str(cha_sort[0][0])+'-'+str(cha_sort[1][0]))
            characters.user_id  = session.get('user_id')
            db.session.add(characters)
            db.session.commit()

        return redirect(url_for('index'))

#注销
@app.route('/layout/')
def layout():
    session.pop('user_id')
    return redirect(url_for("index"))

#发布朋友圈
@app.route('/life/', methods=['GET', 'POST'])
@login_required
def life():
    if request.method == 'GET':
        return render_template('life.html')
    else:
        content     =   request.form.get('content')
        img         =   request.files.get('img')
        ran = randoms()
        imgname     =   ran+str(img.filename)
        img_path    =   path+imgname
        img.save(img_path)
        url         =   '/static/user_img/'+imgname
        life        =   Life(content=content, img=url)
        user_id     =   session.get('user_id')
        user        =   User.query.filter(User.id==user_id).first()
        life.author =   user
        db.session.add(life)
        db.session.commit()
        return redirect(url_for('index'))

#回复页面
@app.route('/details/<life_id>', methods=['POST', 'GET'])
def details(life_id):
    if request.method == 'GET':
        life_model = Life.query.filter(Life.id == life_id).first()
        count_model = len(life_model.comments)
        return render_template('details.html', life=life_model, count=count_model)
    else:
        return 'post'

#添加评论
@app.route('/add_comment/', methods=['POST'])
@login_required
def add_comment():
    comment     =    request.form.get('comment')
    life_id     =    request.form.get('life_id')
    '''算法开始'''
    index_now   =   compute_model(comment)
    print(str(index_now))
    life        =   Life.query.filter(Life.id==life_id).first()
    author      =   User.query.filter(User.id==life.author_id).first()
    character   =   Characters.query.filter(Characters.user_id==author.id).first()
    if character.rank:
        string          =   float(character.rank)
        string          +=  index_now
        character.rank  =   str(string)
        db.session.commit()
    else:
        character.rank = str(index_now)
        db.session.commit()
    '''算法结束'''
    comments    =    Comments(content=comment)
    comments.life_id = life_id
    user_id = session.get('user_id')
    comments.user_id = user_id
    db.session.add(comments)
    db.session.commit()
    return redirect(url_for('details', life_id=life_id))

#个人信息
@app.route('/personal/')
@login_required
def personal():
    user_id     =   session.get('user_id')
    user_model  =   User.query.filter(User.id==user_id).first()
    return render_template('personal.html', user=user_model)

#修改个人信息
@app.route('/infoupdate/', methods=['GET', 'POST'])
@login_required
def infoupdate():
    user_id     =   session.get('user_id')
    user_model  =   User.query.filter(User.id == user_id).first()
    life_model  =   Life.query.filter(Life.author_id == user_model.id).all()
    if request.method == 'GET':
        return render_template('infoupudate.html', user=user_model)
    else:
        ###############################################
        #更改用户信息
        avatar                  =   request.files.get('img')
        username                =   request.form.get('username')
        autograph               =   request.form.get('autograph')
        password                =   request.form.get('password')
        user_model.username     =   username
        user_model.autograph     =   autograph
        user_model.password     =   password

        ran = randoms()
        imgname = ran + str(avatar.filename)
        img_path = path + imgname
        avatar.save(img_path)
        url = '/static/user_img/' + imgname
        url_model = user_model.img
        if len(url)==27:
            url = url_model
        else:
            pass
        user_model.img = url
        db.session.commit()
        ##################################################
        #更改兴趣爱好
        hobby_model = ''
        content = request.values.getlist('hobby')
        if len(content) == 0:
            pass
        else:
            hobby   =   Hobby.query.filter(Hobby.user_id==user_id).first()
            db.session.delete(hobby)
            db.session.commit()

            for con in content:
                hobby_model = hobby_model + con + ';'
            hobby = Hobby(hobby=hobby_model)
            hobby.user_id = user_id
            db.session.add(hobby)
            db.session.commit()
        ####################################################
        #删除朋友圈
        for foo in life_model:
            f = request.form.get('删除'+str(foo.id))
            if f:
                life = Life.query.filter(Life.id==foo.id).first()
                db.session.delete(life)
                db.session.commit()
        return render_template('personal.html')

#搜索好友
@app.route('/search/',methods=['POST'])
@login_required
def search():
    phone   =   request.form.get('mphone')
    friend_model  =   User.query.filter(User.phone == phone).first()
    if friend_model:
        return redirect(url_for('add_friend', phone=phone))
    else:
        return '没有此用户'
#添加好友
@app.route('/add_friend?phone=<phone>', methods=['GET','POST'])
@login_required
def add_friend(phone):
    user_id = session.get('user_id')
    user_model = User.query.filter(User.id == user_id).first()
    friend_model = User.query.filter(User.phone == phone).first()
    if request.method == 'GET':
        return render_template('search.html', user=user_model, friend=friend_model)
    else:
        test    =   Friend.query.filter(Friend.friend_id == friend_model.id, Friend.user_id == user_id).first()
        if test:
            print('1')
            return render_template('search.html', user=user_model, friend=friend_model)
        else:
            print('2')
            friend          =   Friend(friend_id=friend_model.id)
            friend.user_id  =   session.get('user_id')
            db.session.add(friend)
            db.session.commit()
            print('3')
            return render_template('search.html', user=user_model, friend=friend_model)

#朋友圈
@app.route('/friend_life/')
@login_required
def friend_life():
    user_id     =   session.get('user_id')
    filter_list =   list()
    friends     =   Friend.query.filter(Friend.user_id == user_id).all()
    for foo in friends:
        filter_list.append(Life.author_id == foo.friend_id)
        print(foo.friend_id)
    context = {
        'life': Life.query.filter(or_(*filter_list)).order_by(db.desc('creat_time')).all(),
        'user': User.query.filter(User.id==user_id).first()
    }
    print(friends)
    print(filter_list)
    print(context['life'])
    for foo in context['life']:
        print(foo.id)
    return render_template("friend_life.html", **context)

'''
=========================================================================================
=========================================后台============================================
=========================================================================================
'''
@app.route('/backstage_index/')
@back_login_required
def backstage_index():
    user_model    =   User.query.all()
    return render_template('backstage_index.html', user=user_model)

@app.route('/backstage_login/', methods=['GET', 'POST'])
def backstage_login():
    if request.method == 'GET':
        return  render_template('backstage_login.html')
    else:
        username    =   request.form.get('u')
        password    =   request.form.get('p')
        admin       =   Admin.query.filter(Admin.username==username, Admin.password==password).first()
        if admin:
            session['admin_id'] = admin.id
            return redirect(url_for('backstage_index'))
        else:
            return render_template('backstage_login.html')

@app.route('/backstage_layout/')
def backstage_layout():
    session.pop('admin_id')
    return redirect(url_for('backstage_login'))

@app.route('/backstage_search/', methods=['POST'])
def backstage_search():
    con_search  =   request.form.get('con_query')
    user_model  =   User.query.filter(User.phone==con_search).first()
    if user_model:
        userid = user_model.id
        return redirect(url_for('backstage_query', userid=userid))
    else:
        return '请输入正确查询信息'
@app.route('/backstage_query?userid=<userid>', methods=['GET', 'POST'])
@back_login_required
def backstage_query(userid):
    user_model = User.query.filter(User.id==userid).first()
    if request.method == 'GET':
        return render_template('backstage_query.html', user=user_model)
    else:
        return
@app.route('/backstage_deluser/<user_id>')
@back_login_required
def backstage_deluser(user_id):
    life        =   Life.query.filter(Life.author_id==user_id).all()
    for i in life:
        db.session.delete(i)
        db.session.commit()
    comment     =   Comments.query.filter(Comments.user_id==user_id).all()
    for i in comment:
        db.session.delete(i)
        db.session.commit()
    character   =   Characters.query.filter(Characters.user_id==user_id).first()
    try:
        db.session.delete(character)
        db.session.commit()
    except :
        print("1")
    hobby       =   Hobby.query.filter(Hobby.user_id==user_id).first()
    try:
        db.session.delete(hobby)
        db.session.commit()
    except:
        print('2')
    friend      =   Friend.query.filter(Friend.user_id==user_id).first()
    try:
        db.session.delete(friend)
        db.session.commit()
    except:
        print('3')
    user = User.query.filter(User.id == user_id).first()
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('backstage_index'))
@app.route('/backstage_update/<user_id>', methods=['POST'])
@back_login_required
def backstage_update(user_id):
    user_model = User.query.filter(User.id == user_id).first()
    life_model = Life.query.filter(Life.author_id == user_model.id).all()
    ###############################################
    # 更改用户信息
    username = request.form.get('username')
    autograph = request.form.get('autograph')
    password = request.form.get('password')
    user_model.username = username
    user_model.autograph = autograph
    user_model.password = password

    db.session.commit()
    ##################################################
    # 更改兴趣爱好
    hobby_model = ''
    content = request.values.getlist('hobby')
    if len(content) == 0:
        pass
    else:
        hobby = Hobby.query.filter(Hobby.user_id == user_id).first()
        db.session.delete(hobby)
        db.session.commit()

        for con in content:
            hobby_model = hobby_model + con + ';'
        hobby = Hobby(hobby=hobby_model)
        hobby.user_id = user_id
        db.session.add(hobby)
        db.session.commit()
    ####################################################
    # 删除朋友圈
    for foo in life_model:
        f = request.form.get('删除' + str(foo.id))
        if f:
            life = Life.query.filter(Life.id == foo.id).first()
            db.session.delete(life)
            db.session.commit()
    return render_template('backstage_query.html', user=user_model)
@app.route('/backstage_content/')
@back_login_required
def backstage_content():
    context = {'life': Life.query.order_by(db.desc('creat_time')).all()}
    return render_template("backstage_content.html", **context)
@app.route('/backstage_update_content/<life_id>', methods=['GET', 'POST'])
@back_login_required
def backstage_update_content(life_id):
    life_model = Life.query.filter(Life.id == life_id).first()
    count_model = len(life_model.comments)
    if request.method == 'GET':
        return render_template('backstage_update_content.html', life=life_model, count=count_model)
    else:
        comment_id_list     =   request.form.getlist('删除')
        print(comment_id_list)
        for comment_id in comment_id_list:
            if comment_id:
                comment = Comments.query.filter(Comments.id==comment_id).first()
                db.session.delete(comment)
                db.session.commit()
        return render_template('backstage_update_content.html', life=life_model, count=count_model)

#上下文钩子函数
@app.context_processor
def if_user():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id==user_id).first()
        if user:
            return {'user': user}
    return {}

if __name__ == '__main__':
    app.run()
