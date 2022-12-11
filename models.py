from sqlalchemy import Column, Integer, String, Text, Boolean, Float, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship, backref
from CNPM import db, app
from flask_login import UserMixin
from datetime import datetime
from enum import Enum as UserEnum
import datetime
import hashlib


class UserRole(UserEnum):
    EMPLOYEE = 1
    ADMIN = 2


class BaseModel(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)


class TuyenBay(BaseModel):
    name = Column(String(50), nullable=False)
    so_luot_bay= Column(Integer, default=0)
    ty_le=Column(Float, default=0)
    doanh_thu=Column(Float, default=0)
    chuyen_bay = relationship('ChuyenBay', backref='tuyen_bay', lazy=True)

    def __str__(self):
        return self.name


class SanBay(BaseModel):
    name=Column(String(50), nullable=False)
    city=Column(String(50), nullable=False)
    country=Column(String(50), nullable=False)
    chuyen_bay_co_san_bay_di=relationship('ChuyenBay',primaryjoin=("and_(SanBay.id==ChuyenBay.sanBayDi_id)"), backref='san_bay_di', lazy=True)
    chuyen_bay_co_san_bay_den=relationship('ChuyenBay',primaryjoin=("and_(SanBay.id==ChuyenBay.sanBayDen_id)"), backref='san_bay_den', lazy=True)
    #chuyen_bay_co_san_bay = relationship('ChuyenBay', primaryjoin=("and_(SanBay.id==ChuyenBay.sanBayDi_id)"), backref='san_bay', lazy=True)
    def __str__(self):
        return self.name


class ThoiDiemBay(BaseModel):
    name = Column(String(50), nullable=False)
    ngay_gio_bay=Column(DateTime, nullable=False)
    thoi_gian_bay=Column(Float, nullable=False)
    thoi_gian_dung=Column(Float, nullable=True)
    chuyenbay=relationship('ChuyenBay', backref='thoi_diem_bay', lazy=True)
    def __str__(self):
        return self.name



ChuyenBayCoSanBayTrungGian = db.Table('sb_trunggian', Column('chuyenBay_id' ,Integer, ForeignKey('chuyen_bay.id'), primary_key=True), Column('sanBayTrungGian_id' ,Integer, ForeignKey('san_bay.id'), primary_key=True))


MayBayThuocChuyenBay = db.Table('may_bay_thuoc_chuyen_bay', Column('mayBay_id', Integer, ForeignKey('may_bay.id'), primary_key=True), Column('chuyenBay_id', Integer, ForeignKey('chuyen_bay.id'), primary_key=True))



class ChuyenBay(BaseModel):
    name = Column(String(50), nullable=False)
    sanBayDi_id = Column(Integer, ForeignKey(SanBay.id), nullable=False)
    sanBayDen_id = Column(Integer, ForeignKey(SanBay.id), nullable=False)
    thoiDiemBay_id = Column(Integer, ForeignKey(ThoiDiemBay.id), nullable=False)
    tuyenBay_id = Column(Integer, ForeignKey(TuyenBay.id), nullable=False)
    ve = relationship('Ve', backref='chuyen_bay', lazy=True)
    khach_hang = relationship('KhachHang', backref='chuyen_bay', lazy=True)
    san_bay_trung_gian = relationship('SanBay', secondary='sb_trunggian', lazy=True, backref=backref('chuyen_bay', lazy=True))
    may_bay=relationship('MayBay', secondary='may_bay_thuoc_chuyen_bay', lazy=True, backref=backref('chuyen_bay', lazy=True))
    created_date = Column(DateTime, default=datetime.datetime.now())

    def __str__(self):
        return self.name


class User(BaseModel, UserMixin):
    name = Column(String(10), nullable=False)
    lastName = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)
    created_date = Column(DateTime, default=datetime.datetime.now())
    avatar = Column(String(100), nullable=False)
    active = Column(Boolean, default=True)
    user_role = Column(Enum(UserRole), default=UserRole.EMPLOYEE)
    ve = relationship('Ve', backref='nhan_vien', lazy=True)
    def  __str__(self):
        return self.name


class MayBay(BaseModel):
    name = Column(String(50), nullable=False)
    hang_ve = relationship('HangVe', backref='may_bay', lazy=True)
    def  __str__(self):
        return self.name


class HangVe(BaseModel):
    name = Column(String(50), nullable=False)
    price = Column(Float, default=0)
    so_luong_con_lai = Column(Integer, default=80)
    mayBay_id = Column(Integer, ForeignKey(MayBay.id), nullable=False)
    ve = relationship('Ve', backref='hang_ve', lazy=True)
    def  __str__(self):
        return self.name


class Ve(BaseModel):
    name = Column(String(50), nullable=False)
    nhanVien_id = Column(Integer, ForeignKey(User.id), nullable=False)
    chuyenBay_id = Column(Integer, ForeignKey(ChuyenBay.id), nullable=False)
    hangVe_id = Column(Integer, ForeignKey(HangVe.id), nullable=False)
    khachhang = relationship('KhachHang', backref='ve', lazy=True)

    def __str__(self):
        return self.name


class KhachHang(BaseModel):
    name = Column(String(10), nullable=False)
    lastName = Column(String(50), nullable=False)
    cccd = Column(String(12), nullable=False)
    hinh_cccd = Column(String(100), nullable=False)
    sdt = Column(String(12), nullable=False)
    ve_id = Column(Integer, ForeignKey(Ve.id), nullable=False)
    chuyenBay_id = Column(Integer, ForeignKey(ChuyenBay.id), nullable=False)

    def __str__(self):
        return self.name


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        tdb = ThoiDiemBay(name= "Thời điểm bay TpHCM-HaNoi",ngay_gio_bay=datetime.datetime(2022,12,10,14,9,1), thoi_gian_bay= (datetime.datetime(2022, 12,10,16,9,1) - datetime.datetime(2022,12,10,14,9,1)).total_seconds()/3600)
        sb1 = SanBay(name="Tp.HCM", city="Tp.HCM", country="VN")
        sb2 = SanBay(name="Ha Noi", city="Ha Noi", country="VN")
        mb = MayBay(name="xxx")
        db.session.add_all([tdb, sb1, sb2, mb])
        db.session.commit()
        password = str(hashlib.md5('123'.encode('utf-8')).hexdigest())
        u1 = User(name="thao", lastName="thao", username="thao", password=password, avatar="asa")
        db.session.add(u1)
        db.session.commit()