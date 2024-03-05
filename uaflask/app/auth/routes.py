from app.auth import bp
from flask import jsonify, redirect, url_for, request, render_template
from datetime import datetime, timezone, timedelta
import sqlalchemy as sa
import hashlib
from app import db, functions as f
from app.models import Users, Profiles
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
        # 비활성 유저
        if user.status == False:
            raise Exception('inert user')
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
        # 유저 생성
        hash_pw = Users.digest_password(req["password"])
        new_user = Users(email=req["email"], name=req["name"], password=hash_pw)
        new_user.password_last = {datetime.today().strftime('%Y-%m-%d'):hash_pw}
        db.session.add(new_user)
        nationality = req["nationality"] if req["nationality"] else "ko"
        profile = Profiles(r_user=user, nationality=nationality)
        db.session.add(profile)
        db.session.commit()
        res['status'] = 'success'
        res['data'] = 'create user'
    except Exception as err:
        print(err)
        res['status'] = 'error'
        res['data'] = err
    return jsonify(res)


@bp.route('/update_user', methods=['POST'])
def update_user():
    try:
        req = request.get_json()
        res = {}
        # req가 비었을 때
        if not req:
            raise Exception('empty request')
        # 로그인 확인
        if not f.login_required(req['name']):
            raise Exception('required login')
        user = db.session.scalar(sa.select(Users).where(Users.email == req["email"] or Users.name == req["name"]))
        # 유저가 없으면
        if not user:
            raise Exception('no exists user')
        # 비활성 유저
        if user.status == False:
            raise Exception('inert user')
        # 아이디, 패스워드 검증
        check, reason = Users.validate_id(req["name"], req["email"])
        if not check:
            raise Exception(reason)
        check, reason = Users.validate_password(req["password"])
        if not check:
            raise Exception(reason)
        # 유저 수정
        last_user = user.name
        hash_pw = Users.digest_password(req["password"])
        user.email = req["email"]
        user.name = req["name"]
        user.password = hash_pw
        user.password_last[f"{datetime.today().strftime('%Y-%m-%d')}"] = hash_pw
        user.business = req["business"]
        user.updated_at = datetime.now(timezone.utc)
        db.session.commit()
        # 세션 업데이트
        r.delete(last_user)
        session = hashlib.sha256(f'{user.name}{datetime.now(timezone(timedelta(hours=9)))}'.encode()).hexdigest()
        r.set(user.name, session, ex=3600*24)
        res['status'] = 'success'
        res['data'] = 'update user'
    except Exception as err:
        print(err)
        res['status'] = 'error'
        res['data'] = err
    return jsonify(res)


@bp.route('/delete_user', methods=['POST'])
def delete_user():
    try:
        req = request.get_json()
        res = {}
        # req가 비었을 때
        if not req:
            raise Exception('empty request')
        # 로그인 확인
        if not f.login_required(req['name']):
            raise Exception('required login')
        user = db.session.scalar(sa.select(Users).where(Users.email == req["email"] or Users.name == req["name"]))
        # 유저가 없으면
        if not user:
            raise Exception('no exists user')
        # 비활성 유저
        if user.status == False:
            raise Exception('inert user')
        # 유저 삭제
        last_user = user.name
        db.session.delete(user)
        db.session.commit()
        # 세션 삭제
        r.delete(last_user)
        res['status'] = 'success'
        res['data'] = 'delete user'
    except Exception as err:
        print(err)
        res['status'] = 'error'
        res['data'] = err
    return jsonify(res)


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


@bp.route('/update_profile', methods=['POST'])
def update_profile():
    try:
        req = request.get_json()
        res = {}
        # req가 비었을 때
        if not req:
            raise Exception('empty request')
        # 로그인 확인
        if not f.login_required(req['name']):
            raise Exception('required login')
        user = db.session.scalar(sa.select(Users).where(Users.email == req["email"] or Users.name == req["name"]))
        # 유저가 없으면
        if not user:
            raise Exception('no exists user')
        # 비활성 유저
        if user.status == False:
            raise Exception('inert user')
        # 프로필 수정
        user.r_profile.image = req['image']
        user.r_profile.nationality = req["nationality"]
        # user.r_profile.like = 
        user.r_profile.accommodation.append(req["accommodation"])
        user.r_profile.clip.append(req["clip"])
        user.r_profile.follow.append(req["follow"])
        user.r_profile.comment.append(req["comment"])
        db.session.commit()
        res['status'] = 'success'
        res['data'] = 'update profile'
    except Exception as err:
        print(err)
        res['status'] = 'error'
        res['data'] = err
    return jsonify(res)


@bp.route('/get_user_info', methods=['GET'])
def get_user_info():
    try:
        req = request.get_json()
        res = {}
        # req가 비었을 때
        if not req:
            raise Exception('empty request')
        # 로그인 확인
        if not f.login_required(req['name']):
            raise Exception('required login')
        user = db.session.scalar(sa.select(Users).where(Users.email == req["email"] or Users.name == req["name"]))
        # 유저가 없으면
        if not user:
            raise Exception('no exists user')
        # 비활성 유저
        if user.status == False:
            raise Exception('inert user')
        # 유저 정보
        info = {}
        for x in req['user']:
            match x:
                case 'email':
                    info["email"] = user.email
                case 'name':
                    info["name"] = user.name
                case 'business':
                    info["business"] = user.business
                case 'updated_at':
                    info["updated_at"] = user.updated_at
                case 'created_at':
                    info["created_at"] = user.created_at
                case 'deleted_at':
                    info["deleted_at"] = user.deleted_at
                case 'status':
                    info["status"] = user.status
        for x in req['profile']:
            match x:
                case 'image':
                    info["image"] = user.r_profile.image
                case 'nationality':
                    info["nationality"] = user.r_profile.nationality
                case 'like':
                    info["like"] = user.r_profile.like
                case 'accommodation':
                    info["accommodation"] = user.r_profile.accommodation
                case 'clip':
                    info["clip"] = user.r_profile.clip
                case 'follow':
                    info["follow"] = user.r_profile.follow
                case 'comment':
                    info["comment"] = user.r_profile.comment
        res['status'] = 'success'
        res['data'] = 'get user info'
        res['info'] = info
    except Exception as err:
        print(err)
        res['status'] = 'error'
        res['data'] = err
    return jsonify(res)
