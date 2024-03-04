from app.auth import bp
from flask import jsonify, redirect, url_for, request, render_template
from datetime import datetime, timezone, timedelta
import sqlalchemy as sa
import hashlib
from app import db, functions as f
from app.models import Users
from sqlalchemy.exc import SQLAlchemyError, DataError
from config import r


@bp.post('/login')
def login():
    try:
        req = request.get_json()
        res = {}
        # req가 비었을 때
        if not req:
            raise Exception('empty request')
        if req.get('email'):
            user = db.session.scalar(sa.select(Users).where(Users.email == req["email"]))
        else:
            user = db.session.scalar(sa.select(Users).where(Users.name == req["name"]))
        # 유저 없음
        if not user:
            raise Exception('user not exists')
        # 패스워드 확인
        check = Users.check_password(req["password"])
        if not check:
            if r.get(user.name) == 'stop': # 로그인 멈춤
                raise Exception('stop login')
            raise Exception('password error')
        # 세션 및 로그인
        session_key = hashlib.sha256(f'{user.name}{datetime.now(timezone(timedelta(hours=9)))}'.encode()).hexdigest()
        r.set(user.name, session_key, ex=3600*24)
        res['status'] = 'success'
        res['data'] = 'login'
    except Exception as err:
        print(err)
        if err.__str__() == 'password error':
            val = r.get(user.name)
            if val:
                if int(val)>=5: # 5회 실패시 5분 멈춤
                    r.set(user.name, 'stop', ex=300)
                r.incr(user.name)
            else:
                r.set(user.name, 1, ex=600) # 로그인 실패 횟수 설정
        res['status'] = 'error'
        res['data'] = err
    return jsonify(res)


@bp.route('/create_user', methods=['POST'])
def create_user():
    try:
        req = request.get_json()
        res = {}
        # req가 비었을 때
        if not req:
            raise Exception('empty request')
        # 아이디, 패스워드 검증
        check, reason = Users.validate_id(req["name"], req["email"])
        if not check:
            raise Exception(reason)
        check, reason = Users.validate_password(req["password"])
        if not check:
            raise Exception(reason)
        user = db.session.scalar(sa.select(Users).where(Users.email == req["email"] or Users.name == req["name"]))
        # 유저 이미 있음
        if user:
            raise Exception('user already exists')
        hash_pw = Users.digest_password(req["password"])
        new_user = Users(email=req["email"], name=req["name"], password=hash_pw)
        new_user.password_last = {datetime.today().strftime('%Y-%m-%d'):hash_pw}
        db.session.add(new_user)
        db.session.commit()
        res['status'] = 'success'
        res['data'] = 'create user'
    except Exception as err:
        print(err)
        res['status'] = 'error'
        res['data'] = err
    return jsonify(res)


# @bp.route('/update_user', methods=['GET', 'POST'])
# def update_user():
    # if not current_user.is_authenticated:
    #     return funcs.result_redirect('로그인해주세요', 'auth.login')
    
    # form = UpdateUserForm()
    # if request.method == 'GET':
    #     return render_template('auth/update_user.html', form=form)
    
    # if form.password.data != form.password_check.data:
    #     return funcs.result_redirect('패스워드가 다름', 'auth.update_user')
    
    # if form.validate_on_submit(): #post submit 했을 경우
    #     try:
    #         user = db.session.scalar(sa.select(Users).where(Users.name == current_user.name))
    #         if user is None:
    #             return funcs.result_redirect('해당 유저가 없음', 'auth.update_user')
            
    #         if user.name == 'root':
    #             return funcs.result_redirect('수정 불가 유저', 'auth.update_user')
            
    #         is_valid, msg = user.validate_password(form.password.data) #패스워드 검증
    #         if not is_valid:
    #             return funcs.result_redirect(msg, 'auth.update_user')
            
    #         user.digest_password(form.password.data)
    #         user.login_fail_count = 0
    #         used_pw = UsedPassword(used_password=user.password, user=user)
    #         db.session.add(used_pw)
    #         db.session.commit()

    #         return funcs.result_redirect(f'{user.name} 패스워드 변경 성공', 'main.index')
    #     except DataError as e:
    #         print(e) #log
    #         return funcs.result_redirect('계정 업데이트 실패', 'auth.update_user')
    # return funcs.result_redirect('업데이트 기타 이상 감지', 'auth.update_user')


# @bp.route('/delete_user', methods=['GET', 'POST'])
# def delete_user():
#     if not current_user.is_authenticated:
#         return funcs.result_redirect('로그인해주세요', 'auth.login')
    
#     form = DeleteUserForm()
#     if request.method == 'GET':
#         return render_template('auth/delete_user.html', form=form)
    
#     if form.validate_on_submit():
#         try:
#             user = db.session.scalar(sa.select(Users).where(Users.name == form.username.data))
#             if user is None:
#                 return funcs.result_redirect('해당 유저가 없음', 'auth.delete_user')

#             if user.name == 'root':
#                 return funcs.result_redirect('삭제 불가 유저', 'auth.delete_user')

#             db.session.delete(user)
#             db.session.commit()
#             flash(f'{form.username.data} 유저 삭제 성공')
#             if current_user.name == form.username.data: #본인이면 여기
#                 return redirect(url_for('auth.logout'))
#             return redirect(url_for('main.index'))
#         except DataError as e:
#             print(e) #log
#             return funcs.result_redirect('계정 삭제 실패', 'auth.delete_user')
#     return funcs.result_redirect('딜리트 기타 이상 감지', 'auth.delete_user')


# @bp.get('/show_users')
# def show_users():
#     if not current_user.is_authenticated:
#         return funcs.result_redirect('로그인해주세요', 'auth.login')
    
#     try:
#         query = Users.query.all()
#         users = [u.name for u in query]
#         return render_template('auth/show_users.html', users=users)
#     except Exception as e:
#         return funcs.result_redirect('목록 로딩 실패', 'main.index')


@bp.get('/logout')
def logout():
    try:
        req = request.get_json()
        res = {}
        # req가 비었을 때
        if not req:
            raise Exception('empty request')
        # 로그인 되어있는지 확인 후 세션 제거
        if f.login_required(req['name']):
            r.delete(req['name'])
        else:
            raise Exception('logout failure')
        res['status'] = 'success'
        res['data'] = 'logout'
    except Exception as err:
        print(err)
        res['status'] = 'error'
        res['data'] = err
    return jsonify(res)
