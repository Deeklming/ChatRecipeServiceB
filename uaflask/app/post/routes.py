from app.post import bp
from flask import jsonify, redirect, url_for, request, render_template
from datetime import datetime, timezone, timedelta
import sqlalchemy as sa
import hashlib
from app import db, functions as f
from app.models import Users, Profiles, Posts, Comments
from sqlalchemy.exc import SQLAlchemyError, DataError
from config import r


@bp.route('/add_post', methods=['POST'])
def add_post():
    try:
        req = request.get_json()
        res = {}
        # req가 비었을 때
        if not req:
            raise Exception('empty request')
        # 로그인 확인
        if not f.login_required(req['name']):
            raise Exception('required login')
        user = db.session.scalar(sa.select(Users).where(Users.name == req["name"]))
        # 유저가 없으면
        if not user:
            raise Exception('no exists user')
        # 비활성 유저
        if user.status == False:
            raise Exception('inert user')


        # 게시글 생성
        new_post = Posts()
        # 패스워드 검증
        check, reason = new_user.validate_password(req["password"])
        if not check:
            raise Exception(reason)
        hash_pw = new_user.digest_password(req["password"])
        new_user.password=hash_pw
        new_user.password_last = {datetime.today().strftime('%Y-%m-%d'):hash_pw}
        # 프로필 생성
        profile = Profiles(nationality=req["nationality"])
        new_user.r_profile.append(profile)
        db.session.add(new_user)
        db.session.commit()
        res['status'] = 'success'
        res['data'] = 'create user'
    except Exception as err:
        print('Error<create_user>:', err)
        res['status'] = 'error'
        res['data'] = str(err).strip("'")
    print('#1###-> ', res)
    return jsonify(res)