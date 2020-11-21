from functools import wraps
from flask import session, redirect, url_for

#登录限制装饰器
def login_required(func):
    @wraps(func)
    def wapper(*args, **kwargs):
        if session.get('user_id'):
            return func(*args, **kwargs)
        else:
            return redirect(url_for('login'))
    return wapper

#后台登录限制修饰器
def back_login_required(func):
    @wraps(func)
    def wapper(*args, **kwargs):
        if session.get('admin_id'):
            return func(*args, **kwargs)
        else:
            return redirect(url_for('backstage_login'))
    return wapper