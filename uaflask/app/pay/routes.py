from app.pay import bp
from flask import jsonify, redirect, url_for, request, render_template
from datetime import datetime, timezone, timedelta
import sqlalchemy as sa
import hashlib
from app import db, functions as f
from app.models import Users, Profiles, Posts, Comments, Reservations
from sqlalchemy.exc import SQLAlchemyError, DataError
from config import r


@bp.route('/do_reservation', methods=['POST'])
def do_reservation():
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
        # 예약
        new_reservation = Reservations(
            head_count = req['head_count'],
            check_in = datetime.strptime(req['check_in'], '%Y-%m-%d %H:%M:%S'),
            check_out = datetime.strptime(req['check_out'], '%Y-%m-%d %H:%M:%S'),
            payment_price = req['payment_price']
        )
        new_reservation.post_id = post.id
        user.r_reservation.append(new_reservation)
        db.session.add(new_reservation)
        db.session.commit()
        res['status'] = 'success'
        res['data'] = 'do reservation'
    except Exception as err:
        print('Error<do_reservation>:', err)
        res['status'] = 'error'
        res['data'] = str(err).strip("'")
    return jsonify(res)


@bp.route('/cancle_reservation', methods=['POST'])
def cancle_reservation():
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
        reservation = db.session.scalar(sa.select(Reservations).where(Reservations.id == req["reservation_id"]))
        # 유저 및 게시글 및 예약이 없으면
        if not user:
            raise Exception('no exists user')
        if not post:
            raise Exception('no exists post')
        if not reservation:
            raise Exception('no exists reservation')
        # 비활성 유저
        if user.status == False:
            raise Exception('inert user')
        # 예약 취소
        db.session.delete(reservation)
        db.session.commit()
        res['status'] = 'success'
        res['data'] = 'cancle reservation'
    except Exception as err:
        print(err)
        res['status'] = 'error'
        res['data'] = str(err).strip("'")
    return jsonify(res)