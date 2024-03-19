import sqlalchemy as sa
import sqlalchemy.orm as sao
import hashlib
import re
import uuid
from email_validator import validate_email, EmailNotValidError, caching_resolver
from datetime import datetime, timezone, timedelta
from decimal import Decimal
from app import db


class Users(db.Model):
    id: sao.Mapped[uuid.UUID] = sao.mapped_column(sa.Uuid, primary_key=True, index=True)
    email: sao.Mapped[str] = sao.mapped_column(sa.VARCHAR(128), unique=True)
    name: sao.Mapped[str] = sao.mapped_column(sa.VARCHAR(20), unique=True)
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
    
    def create_uuid():
        return uuid.uuid4()
    
    def digest_password(self, pw: str):
        return hashlib.sha3_512(pw.encode()).hexdigest()
    
    def check_password(self, pw: str):
        return self.password == self.digest_password(pw)
    
    def validate_id(n: str, e: str):
        # 유저 이름 검증
        if not re.compile('^(?=.*[\\w])[\\w]{2,20}$').search(n):
            return (False, 'name validate failed')
        # 이메일 검증
        try:
            emailinfo = validate_email(e, check_deliverability=True, dns_resolver=caching_resolver(timeout=5))
            email = emailinfo.normalized
            return (True, 'id success')
        except EmailNotValidError as err:
            print(err)
            return (False, 'email validate failed')
    
    def validate_password(self, pw: str):
        # 현재 및 과거 중복된 PW
        hash_pw = self.digest_password(pw)
        if self.password_last:
            for x in self.password_last.values():
                if self.password == hash_pw:
                    return (False, 'overlapping password')
        # 영문자, 숫자, 특수문자 최소 하나씩 8~32자 검증
        r = re.compile('^(?=.*[\\d])(?=.*[a-zA-Z])(?=.*[\\W])[\\S]{8,32}$').fullmatch(pw)
        if not r:
            return (False, 'password condition check failed')
        # 특정 패턴 검증
        ptrn = [
            re.compile('(\\w)\\1\\1').findall(pw), #3자 이상 연속된 동일 문자
            re.compile(f'(?i){self.name}|{self.email.split("@")[0]}').search(pw) #유저 이름, 이메일 아이디 포함
        ]
        for x in ptrn:
            if x:
                return (False, 'password easy pattern')
        return (True, 'password success')


class Profiles(db.Model):
    id: sao.Mapped[int] = sao.mapped_column(primary_key=True, index=True)
    user_id: sao.Mapped[uuid.UUID] = sao.mapped_column(sa.Uuid, sa.ForeignKey(Users.id, ondelete='CASCADE'))
    image: sao.Mapped[str] = sao.mapped_column(sa.VARCHAR(30), nullable=True, default=None)
    nationality: sao.Mapped[str] = sao.mapped_column(sa.CHAR(2))
    like: sao.Mapped[dict] = sao.mapped_column(sa.JSON, default={})
    accommodation: sao.Mapped[list] = sao.mapped_column(sa.ARRAY(sa.Integer), default=[])
    clip: sao.Mapped[list] = sao.mapped_column(sa.ARRAY(sa.Integer), default=[])
    follow: sao.Mapped[list] = sao.mapped_column(sa.ARRAY(sa.Uuid), default=[])
    comment: sao.Mapped[list] = sao.mapped_column(sa.ARRAY(sa.Integer), default=[])
    r_user = sao.relationship('Users', back_populates='r_profile', uselist=False)

    def __repr__(self):
        return f'<Profile {self.user_id}>'


class Posts(db.Model):
    id: sao.Mapped[int] = sao.mapped_column(primary_key=True, index=True)
    author: sao.Mapped[uuid.UUID] = sao.mapped_column(sa.Uuid, sa.ForeignKey(Users.id))
    title: sao.Mapped[str] = sao.mapped_column(sa.VARCHAR(64), unique=True)
    images: sao.Mapped[dict] = sao.mapped_column(sa.JSON, nullable=True)
    content: sao.Mapped[str] = sao.mapped_column(sa.TEXT)
    amenity: sao.Mapped[list] = sao.mapped_column(sa.ARRAY(sa.String), nullable=True)
    price: sao.Mapped[Decimal] = sao.mapped_column(sa.DECIMAL)
    like_avg_score: sao.Mapped[float] = sao.mapped_column(sa.FLOAT, default=0.0)
    like_count: sao.Mapped[int] = sao.mapped_column(sa.INTEGER, default=0)
    clip_count: sao.Mapped[int] = sao.mapped_column(sa.INTEGER, default=0)
    available_start_at: sao.Mapped[datetime] = sao.mapped_column(sa.DateTime)
    available_end_at: sao.Mapped[datetime] = sao.mapped_column(sa.DateTime)
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
    post_id: sao.Mapped[int] = sao.mapped_column(sa.INTEGER, sa.ForeignKey(Posts.id))
    created_at: sao.Mapped[datetime] = sao.mapped_column(sa.DateTime, default=lambda: datetime.now(timezone.utc))
    head_count: sao.Mapped[int] = sao.mapped_column(sa.INTEGER)
    check_in: sao.Mapped[datetime] = sao.mapped_column(sa.DateTime)
    check_out: sao.Mapped[datetime] = sao.mapped_column(sa.DateTime)
    payment_price: sao.Mapped[Decimal] = sao.mapped_column(sa.DECIMAL)
    r_user = sao.relationship('Users', backref='r_reservation')
    
    def __repr__(self):
        return f'<Reservation {self.id}>'


class Hashtags(db.Model):
    id: sao.Mapped[int] = sao.mapped_column(primary_key=True, index=True)
    theme: sao.Mapped[str] = sao.mapped_column(sa.VARCHAR(18))
    tag: sao.Mapped[str] = sao.mapped_column(sa.VARCHAR(30))
    note: sao.Mapped[str] = sao.mapped_column(sa.VARCHAR(100), nullable=True, default=None)
    
    def __repr__(self):
        return f'<Hashtag {self.tag}>'
