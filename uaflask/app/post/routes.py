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
        new_post = Posts(
            title=req['title'],
            images=req['images'],
            content=req['content'],
            amenity=req['amenity'],
            price=req['price'],
            available_start_at = datetime.strptime(req['available_start_at'], '%Y-%m-%d %H:%M:%S'),
            available_end_at = datetime.strptime(req['available_end_at'], '%Y-%m-%d %H:%M:%S')
        )
        user.r_post.append(new_post)
        # 유저의 게시글 추가
        user.r_profile[0].accommodation = user.r_profile[0].accommodation + [new_post.id]
        db.session.add(new_post)
        db.session.commit()
        res['status'] = 'success'
        res['data'] = 'add post'
    except Exception as err:
        print('Error<add_post>:', err)
        res['status'] = 'error'
        res['data'] = str(err).strip("'")
    return jsonify(res)


@bp.route('/del_post', methods=['POST'])
def del_post():
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
        post = db.session.scalar(sa.select(Posts).where(Posts.id == req["post_id"]))
        # 유저 및 게시글이 없으면
        if not user:
            raise Exception('no exists user')
        if not post:
            raise Exception('no exists post')
        # 비활성 유저
        if user.status == False:
            raise Exception('inert user')
        # 게시글 삭제
        user.r_profile[0].accommodation = [z for z in user.r_profile[0].accommodation if z!=req["post_id"]]
        db.session.delete(post)
        db.session.commit()
        res['status'] = 'success'
        res['data'] = 'del post'
    except Exception as err:
        print(err)
        res['status'] = 'error'
        res['data'] = str(err).strip("'")
    return jsonify(res)


@bp.route('/add_comment', methods=['POST'])
def add_comment():
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
        post = db.session.scalar(sa.select(Posts).where(Posts.id == req["post_id"]))
        # 유저 및 게시글이 없으면
        if not user:
            raise Exception('no exists user')
        if not post:
            raise Exception('no exists post')
        # 비활성 유저
        if user.status == False:
            raise Exception('inert user')
        # 댓글 생성
        new_comment = Comments(content=req['content'])
        new_comment.post_id = post.id
        user.r_comment.append(new_comment)
        # 유저에 추가
        user.r_profile[0].comment = user.r_profile[0].comment + [new_comment.id]
        db.session.add(new_comment)
        db.session.commit()
        res['status'] = 'success'
        res['data'] = 'add comment'
    except Exception as err:
        print('Error<add_comment>:', err)
        res['status'] = 'error'
        res['data'] = str(err).strip("'")
    return jsonify(res)


@bp.route('/del_comment', methods=['POST'])
def del_comment():
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
        post = db.session.scalar(sa.select(Posts).where(Posts.id == req["post_id"]))
        # 유저 및 게시글이 없으면
        if not user:
            raise Exception('no exists user')
        if not post:
            raise Exception('no exists post')
        # 비활성 유저
        if user.status == False:
            raise Exception('inert user')
        # 댓글 삭제
        user.r_profile[0].comment = [z for z in user.r_profile[0].comment if z!=req["comment_id"]]
        db.session.delete(post.r_comment[0])
        db.session.commit()
        res['status'] = 'success'
        res['data'] = 'del comment'
    except Exception as err:
        print(err)
        res['status'] = 'error'
        res['data'] = str(err).strip("'")
    return jsonify(res)