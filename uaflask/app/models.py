import sqlalchemy as sa
import sqlalchemy.orm as sao
import hashlib
import re
import uuid
from flask_login import UserMixin
from email_validator import validate_email, EmailNotValidError, caching_resolver
from datetime import datetime, timezone
from decimal import Decimal
from app import db, login


class Users(UserMixin, db.Model):
    id: sao.Mapped[uuid.UUID] = sao.mapped_column(sa.Uuid, primary_key=True, index=True)
    email: sao.Mapped[str] = sao.mapped_column(sa.VARCHAR(128), unique=True)
    name: sao.Mapped[str] = sao.mapped_column(sa.VARCHAR(30), unique=True)
    password: sao.Mapped[str] = sao.mapped_column(sa.CHAR(128))
    password_last: sao.Mapped[dict] = sao.mapped_column(sa.JSON)
    business: sao.Mapped[bool] = sao.mapped_column(sa.BOOLEAN, default=False)
    updated_at: sao.Mapped[datetime] = sao.mapped_column(sa.DateTime, default=lambda: datetime.now(timezone.utc))
    created_at: sao.Mapped[datetime] = sao.mapped_column(sa.DateTime, default=lambda: datetime.now(timezone.utc))
    deleted_at: sao.Mapped[datetime] = sao.mapped_column(sa.DateTime, nullable=True, default=None)
    status: sao.Mapped[bool] = sao.mapped_column(sa.BOOLEAN, default=True)
    r_profile = sao.relationship('Profiles', back_populates='r_user', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<User {self.name}>'
    
    def digest_password(self, pw: str):
        return hashlib.sha3_256(pw.encode()).hexdigest()
    
    def check_password(self, pw: str):
        return self.password == self.digest_password(pw)
    
    def validate_signup_email(self, e: str):
        try:
            emailinfo = validate_email(e, check_deliverability=True, dns_resolver=caching_resolver(timeout=5))
            email = emailinfo.normalized
            print(emailinfo)
            print(email)
        except EmailNotValidError as err:
            print(err)
            print(str(err))

    def validate_signin_email(self, e: str):
        try:
            emailinfo = validate_email(e, check_deliverability=False)
            email = emailinfo.normalized
            print(emailinfo)
            print(emailinfo.ascii_email)
            print(email)
        except EmailNotValidError as err:
            print(err)
            print(str(err))
    
    def validate_password(self, pw: str):
        # 현재 및 과거 중복된 PW
        hash_pw = self.digest_password(pw)
        for x in self.password_last.values():
            if self.password == hash_pw:
                return (False, 'overlapping password')
        # 영문자, 숫자, 특수문자 최소 하나씩 8~32자 검증
        r = re.compile('^(?=.*[\\d])(?=.*[a-zA-Z])(?=.*[\\W])[\\S]{8,32}$').fullmatch(pw)
        if not r:
            return (False, 'condition check failed')
        # 특정 패턴 검증
        ptrn = [
            re.compile('(\\w)\\1\\1').findall(pw), #3자 이상 연속된 동일 문자
            re.compile(f'(?i){self.name}|{self.email.split("@")[0]}').search(pw) #유저 이름, 이메일 아이디 포함
        ]
        for x in ptrn:
            if x:
                return (False, 'easy pattern')
        return (True, 'success')


class Profiles(db.Model):
    id: sao.Mapped[int] = sao.mapped_column(primary_key=True, index=True)
    user_id: sao.Mapped[uuid.UUID] = sao.mapped_column(sa.Uuid, sa.ForeignKey(Users.id, ondelete='CASCADE'))
    image: sao.Mapped[bytes] = sao.mapped_column(sa.LargeBinary)
    nationality: sao.Mapped[str] = sao.mapped_column(sa.CHAR(2))
    like: sao.Mapped[dict] = sao.mapped_column(sa.JSON)
    accommodation: sao.Mapped[list] = sao.mapped_column(sa.ARRAY(sa.Integer))
    clip: sao.Mapped[list] = sao.mapped_column(sa.ARRAY(sa.Integer))
    follow: sao.Mapped[list] = sao.mapped_column(sa.ARRAY(sa.Uuid))
    comment: sao.Mapped[list] = sao.mapped_column(sa.ARRAY(sa.Integer))
    r_user = sao.relationship('Users', back_populates='r_profile', uselist=False)

    def __repr__(self):
        return f'<Profile {self.user_id}>'


class Posts(db.Model):
    id: sao.Mapped[int] = sao.mapped_column(primary_key=True, index=True)
    author: sao.Mapped[uuid.UUID] = sao.mapped_column(sa.Uuid, sa.ForeignKey(Users.id))
    title: sao.Mapped[str] = sao.mapped_column(sa.VARCHAR(64))
    images: sao.Mapped[dict] = sao.mapped_column(sa.JSON, nullable=True)
    content: sao.Mapped[str] = sao.mapped_column(sa.TEXT)
    amenity: sao.Mapped[list] = sao.mapped_column(sa.ARRAY(sa.String), nullable=True)
    price: sao.Mapped[Decimal] = sao.mapped_column(sa.DECIMAL)
    like_vag_score: sao.Mapped[float] = sao.mapped_column(sa.FLOAT)
    like_count: sao.Mapped[int] = sao.mapped_column(sa.INTEGER)
    clip_count: sao.Mapped[int] = sao.mapped_column(sa.INTEGER)
    start_at: sao.Mapped[datetime] = sao.mapped_column(sa.DateTime)
    end_at: sao.Mapped[datetime] = sao.mapped_column(sa.DateTime)
    checkin: sao.Mapped[datetime] = sao.mapped_column(sa.DateTime)
    checkout: sao.Mapped[datetime] = sao.mapped_column(sa.DateTime)
    position: sao.Mapped[str] = sao.mapped_column(sa.VARCHAR, nullable=True, default=None)
    hashtag: sao.Mapped[list] = sao.mapped_column(sa.ARRAY(sa.String), nullable=True, default=None)
    public: sao.Mapped[bool] = sao.mapped_column(sa.BOOLEAN, default=True)
    r_user = sao.relationship('Users', backref='r_post')

    def __repr__(self):
        return f'<Post {self.title[:9]}>'


class Comments(db.Model):
    id: sao.Mapped[int] = sao.mapped_column(primary_key=True, index=True)
    post_id: sao.Mapped[int] = sao.mapped_column(sa.INTEGER, sa.ForeignKey(Posts.id))
    author: sao.Mapped[uuid.UUID] = sao.mapped_column(sa.Uuid, sa.ForeignKey(Users.id))
    content: sao.Mapped[str] = sao.mapped_column(sa.VARCHAR(300))
    created_at: sao.Mapped[datetime] = sao.mapped_column(sa.DateTime, default=lambda: datetime.now(timezone.utc))
    public: sao.Mapped[bool] = sao.mapped_column(sa.BOOLEAN, default=True)
    r_user = sao.relationship('Users', backref='r_comment')
    r_post = sao.relationship('Posts', backref='r_comment')
    
    def __repr__(self):
        return f'<Comment {self.id}>'


class Reservations(db.Model):
    id: sao.Mapped[int] = sao.mapped_column(primary_key=True, index=True)
    user_id: sao.Mapped[uuid.UUID] = sao.mapped_column(sa.Uuid, sa.ForeignKey(Users.id))
    created_at: sao.Mapped[datetime] = sao.mapped_column(sa.DateTime, default=lambda: datetime.now(timezone.utc))
    head_count: sao.Mapped[int] = sao.mapped_column(sa.INTEGER)
    checkin: sao.Mapped[datetime] = sao.mapped_column(sa.DateTime)
    checkout: sao.Mapped[datetime] = sao.mapped_column(sa.DateTime)
    payment_price: sao.Mapped[Decimal] = sao.mapped_column(sa.DECIMAL)
    r_user = sao.relationship('Users', backref='r_reservation')
    
    def __repr__(self):
        return f'<Reservation {self.id}>'


class Hashtags(db.Model):
    id: sao.Mapped[int] = sao.mapped_column(primary_key=True, index=True)
    theme: sao.Mapped[str] = sao.mapped_column(sa.VARCHAR(18))
    tag: sao.Mapped[str] = sao.mapped_column(sa.VARCHAR(30))
    note: sao.Mapped[str] = sao.mapped_column(sa.VARCHAR(100))
    
    def __repr__(self):
        return f'<Hashtag {self.tag}>'

@login.user_loader
def load_user(id):
    return db.session.get(Users, id)
