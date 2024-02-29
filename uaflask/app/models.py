import sqlalchemy as sa
import sqlalchemy.orm as sao
import hashlib
import re
import uuid
from flask_login import UserMixin
from datetime import datetime, timezone, timedelta
from decimal import Decimal
from app import db, login


class Users(UserMixin, db.Model):
    id: sao.Mapped[uuid.UUID] = sao.mapped_column(sa.Uuid, primary_key=True, index=True)
    email: sao.Mapped[str] = sao.mapped_column(sa.VARCHAR(128), unique=True)
    name: sao.Mapped[str] = sao.mapped_column(sa.VARCHAR(30), unique=True)
    password: sao.Mapped[str] = sao.mapped_column(sa.CHAR(128))
    password_last: sao.Mapped[dict] = sao.mapped_column(sa.JSON)
    business: sao.Mapped[bool] = sao.mapped_column(sa.BOOLEAN, default=False)
    updated_at: sao.Mapped[datetime] = sao.mapped_column(sa.DATETIME, default=lambda: datetime.now(timezone.utc))
    created_at: sao.Mapped[datetime] = sao.mapped_column(sa.DATETIME, default=lambda: datetime.now(timezone.utc))
    deleted_at: sao.Mapped[datetime] = sao.mapped_column(sa.DATETIME, nullable=True, default=None)
    status: sao.Mapped[bool] = sao.mapped_column(sa.BOOLEAN, default=True)
    # user_id: sao.WriteOnlyMapped['Profiles' | 'UsedPassword'] = sao.relationship(back_populates='user', cascade="all, delete", passive_deletes=True)

    def __repr__(self):
        return f'<User {self.name}>'
    
    def digest_password(self, pw: str):
        return hashlib.sha3_256(pw.encode()).hexdigest()
    
    def check_password(self, pw: str):
        return self.password == self.digest_password(pw)
    
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
            re.compile(f'(?i){self.name}|{self.email.split('@')[0]}').search(pw) #유저 이름, 이메일 아이디 포함
        ]
        for x in ptrn:
            if x:
                return (False, 'easy pattern')

        return (True, 'success')

@login.user_loader
def load_user(id):
    return db.session.get(Users, id)

class Profiles(db.Model):
    user_id: sao.Mapped[uuid.UUID] = sao.mapped_column(sa.Uuid, sa.ForeignKey(Users.id, ondelete='CASCADE'), index=True)
    image: sao.Mapped[bytes] = sao.mapped_column(sa.LargeBinary)
    nationality: sao.Mapped[str] = sao.mapped_column(sa.CHAR(2))
    like: sao.Mapped[dict] = sao.mapped_column(sa.JSON)
    clip: sao.Mapped[list] = sao.mapped_column(sa.ARRAY)
    follow: sao.Mapped[list] = sao.mapped_column(sa.ARRAY)
    comment: sao.Mapped[list] = sao.mapped_column(sa.ARRAY)
    accommodation: sao.Mapped[list] = sao.mapped_column(sa.ARRAY)
    # user_id_r: sao.Mapped[Users] = sao.relationship(back_populates='user_id')

    def __repr__(self):
        return f'<Profile {self.user_id}>'

class Posts(db.Model):
    id: sao.Mapped[int] = sao.mapped_column(primary_key=True, index=True)
    author: sao.Mapped[uuid.UUID] = sao.mapped_column(sa.Uuid, sa.ForeignKey(Users.id, ondelete='CASCADE'))
    title: sao.Mapped[str] = sao.mapped_column(sa.VARCHAR(64))
    images: sao.Mapped[dict] = sao.mapped_column(sa.JSON, nullable=True)
    content: sao.Mapped[str] = sao.mapped_column(sa.TEXT)
    amenity: sao.Mapped[list] = sao.mapped_column(sa.ARRAY, nullable=True)
    price: sao.Mapped[Decimal] = sao.mapped_column(sa.DECIMAL)
    like_vag_score: sao.Mapped[float] = sao.mapped_column(sa.FLOAT)
    like_count: sao.Mapped[int] = sao.mapped_column(sa.INTEGER)
    clip_count: sao.Mapped[int] = sao.mapped_column(sa.INTEGER)
    start_at: sao.Mapped[datetime] = sao.mapped_column(sa.DATETIME)
    end_at: sao.Mapped[datetime] = sao.mapped_column(sa.DATETIME)
    checkin: sao.Mapped[datetime] = sao.mapped_column(sa.DATETIME)
    checkout: sao.Mapped[datetime] = sao.mapped_column(sa.DATETIME)
    position: sao.Mapped[str] = sao.mapped_column(sa.VARCHAR, nullable=True, default=None)
    hashtag: sao.Mapped[list] = sao.mapped_column(sa.ARRAY, nullable=True, default=None)
    public: sao.Mapped[bool] = sao.mapped_column(sa.BOOLEAN, default=True)
    # user: sao.Mapped[Users] = sao.relationship(back_populates='used_pw')

    def __repr__(self):
        return f'<Post {self.title[:9]}>'

class Comments(db.Model):
    id: sao.Mapped[int] = sao.mapped_column(primary_key=True, index=True)
    post_id: sao.Mapped[int] = sao.mapped_column(sa.INTEGER, sa.ForeignKey(Posts.id, ondelete='CASCADE'))
    author: sao.Mapped[uuid.UUID] = sao.mapped_column(sa.Uuid, sa.ForeignKey(Users.id, ondelete='CASCADE'))
    content: sao.Mapped[str] = sao.mapped_column(sa.VARCHAR(300))
    created_at: sao.Mapped[datetime] = sao.mapped_column(sa.DATETIME, default=lambda: datetime.now(timezone.utc))
    public: sao.Mapped[bool] = sao.mapped_column(sa.BOOLEAN, default=True)
    # user_id_r: sao.Mapped[Users] = sao.relationship(back_populates='user_id')

    def __repr__(self):
        return f'<Comment {self.id}>'

class Reservations(db.Model):
    id: sao.Mapped[int] = sao.mapped_column(primary_key=True, index=True)
    user_id: sao.Mapped[uuid.UUID] = sao.mapped_column(sa.Uuid, sa.ForeignKey(Users.id, ondelete='CASCADE'))
    created_at: sao.Mapped[datetime] = sao.mapped_column(sa.DATETIME, default=lambda: datetime.now(timezone.utc))
    head_count: sao.Mapped[int] = sao.mapped_column(sa.INTEGER)
    checkin: sao.Mapped[datetime] = sao.mapped_column(sa.DATETIME)
    checkout: sao.Mapped[datetime] = sao.mapped_column(sa.DATETIME)
    payment_price: sao.Mapped[Decimal] = sao.mapped_column(sa.DECIMAL)
    # user_id_r: sao.Mapped[Users] = sao.relationship(back_populates='user_id')

    def __repr__(self):
        return f'<Reservation {self.id}>'

class Hashtags(db.Model):
    id: sao.Mapped[int] = sao.mapped_column(primary_key=True, index=True)
    theme: sao.Mapped[str] = sao.mapped_column(sa.VARCHAR(18))
    tag: sao.Mapped[str] = sao.mapped_column(sa.VARCHAR(30))
    note: sao.Mapped[str] = sao.mapped_column(sa.VARCHAR(100))
    
    def __repr__(self):
        return f'<Hashtag {self.tag}>'
