from sqlalchemy import Column, Integer, Float, String, ForeignKey, Enum, DateTime, Time, Boolean, Double, \
    Date,CheckConstraint
from sqlalchemy.orm import relationship
from app import db, app
from datetime import datetime
from enum import Enum as UserEnum
from flask_login import UserMixin
class UserRole(UserEnum):
    ADMIN = 1
    CUSTOMER = 2
    EMPLOYEE = 3

class QuyDinh(db.Model):
    id = Column(Integer, autoincrement=True, primary_key=True)
    tenQuyDinh = Column(String(50), nullable=False)
    giaTri = Column(Integer, nullable=False)


class NguoiDung(db.Model, UserMixin):
    id = Column(Integer, autoincrement=True, primary_key=True)
    hoTen = Column(String(50), nullable=False)
    CCCD = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False)
    SDT = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    is_active= Column(Boolean, default=True)
    user_role= Column(Enum(UserRole), default=UserRole.CUSTOMER)
    #relationship
    nhan_vien = relationship("NhanVien", backref="nhan_vien", lazy=True)
    khach_hang = relationship("KhachHang", backref="khach_hang", lazy=True)
    quan_tri_vien = relationship("QuanTriVien", backref="quan_tri_vien", lazy=True)

class NhanVien(db.Model):
    id = Column(Integer, ForeignKey(NguoiDung.id), primary_key=True)
    bangCap = Column(String(100), nullable=False)
    ve = relationship("Ve", backref="nhan_vien", lazy=True)

class KhachHang(db.Model):
    id = Column(Integer, ForeignKey(NguoiDung.id), primary_key=True)
    diemTichLuy = Column(Integer, default=0)
    ve = relationship("Ve", backref="khach_hang", lazy=True)

class QuanTriVien(db.Model):
    id = Column(Integer, ForeignKey(NguoiDung.id), primary_key=True)
    nhiemVu = Column(String(10))

class SanBay(db.Model):
    id = Column(Integer, autoincrement=True, primary_key=True)
    tenSB = Column(String(50), nullable=False)
    tuyen_bay_den = relationship("TuyenBay", backref="san_bay_den", lazy=True, foreign_keys='TuyenBay.san_bay_den_id')
    tuyen_bay_di = relationship("TuyenBay", backref="san_bay_di", lazy=True, foreign_keys='TuyenBay.san_bay_di_id')
    cb_sb = relationship("ChuyenBay_SanBay", backref="san_bay", lazy=True)

    def __str__(self):
        return self.tenSB

class TuyenBay(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    tenTB = Column(String(100), nullable=False, unique=True)
    san_bay_den_id = Column(Integer, ForeignKey(SanBay.id))
    san_bay_di_id = Column(Integer, ForeignKey(SanBay.id))
    chuyen_bay = relationship("ChuyenBay", backref="tuyen_bay", lazy=True)
    # don_gia_ve = relationship("DonGiaVe", backref="tuyen_bay", lazy=True)
    CheckConstraint("san_bay_den_id <> san_bay_di_id", name='checkFromTo')

    def __str__(self):
        return self.tenTB


class MayBay(db.Model):
    id = Column(Integer, autoincrement=True, primary_key=True)
    tenMB = Column(String(50), nullable=False)
    chuyen_bay = relationship("ChuyenBay", backref="may_bay", lazy=True)
    ghe = relationship("Ghe", backref="ghe", lazy=True)

    def __str__(self):
        return self.tenMB


class ChuyenBay(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    tenCB = Column(String(20), nullable=False, unique=True)
    ngayBay = Column(DateTime, nullable=False)
    thoiGianBay = Column(Time, nullable=False)
    tuyen_bay_id = Column(Integer, ForeignKey(TuyenBay.id))
    ve = relationship("Ve", backref="chuyen_bay", lazy=True)
    may_bay_id = Column(Integer, ForeignKey(MayBay.id))
    cb_sb = relationship("ChuyenBay_SanBay", backref="chuyen_bay", lazy=True)

    def __str__(self):
        return self.tenCB

class ChuyenBay_SanBay(db.Model):
    id = Column(Integer, autoincrement=True, primary_key=True)
    thoiGianCho = Column(Time, nullable=False)
    ghiChu = Column(String(100))
    chuyen_bay_id = Column(Integer, ForeignKey(ChuyenBay.id))
    san_bay_id = Column(Integer, ForeignKey(SanBay.id))

class HangVe(db.Model):
    id = Column(Integer, autoincrement=True, primary_key=True)
    tenHangVe = Column(String(50), nullable=False)
    ve = relationship("Ve", backref="hang_ve", lazy=True)
    gia_ve = relationship("DonGiaVe", backref="hang_ve", lazy=True)
    def __str__(self):
        return self.tenHangVe

class Ghe(db.Model):
    id = Column(Integer, autoincrement=True, primary_key=True)
    tenGhe = Column(String(50), nullable=False)
    trangThai = Column(Boolean, default=True)
    ve = relationship("Ve", backref="ghe", lazy=True)
    hangVe_id = Column(Integer, ForeignKey(HangVe.id))
    may_bay_id = Column(Integer, ForeignKey(MayBay.id))

class Ve(db.Model):
    id = Column(Integer, autoincrement=True, primary_key=True)
    ngayThanhToan = Column(Date, default=datetime.now())
    ngayXuatVe = Column(Date, default=datetime.now())
    giaVe = Column(Double, nullable=False)
    khach_hang_id = Column(Integer, ForeignKey(KhachHang.id))
    chuyen_bay_id = Column(Integer, ForeignKey(ChuyenBay.id))
    ghe_id = Column(Integer, ForeignKey(Ghe.id))
    hang_ve_id = Column(Integer, ForeignKey(HangVe.id))
    nhan_vien_id = Column(Integer, ForeignKey(NhanVien.id))

class DonGiaVe(db.Model):
    tuyenBay_id = Column(Integer, ForeignKey(TuyenBay.id), primary_key=True)
    hangVe_id = Column(Integer, ForeignKey(HangVe.id), primary_key=True)
    donGia = Column(Double, nullable=False)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()


        gv1 = DonGiaVe(tuyenBay_id=1, hangVe_id=1, donGia=1500000)
        gv2 = DonGiaVe(tuyenBay_id=2, hangVe_id=1, donGia=1600000)

        db.session.add(gv1)
        db.session.add(gv2)
        db.session.commit()
        import hashlib
        u = NguoiDung(hoTen='Tuấn Kiệt', CCCD='079203004145', SDT='0901147032', email='a@gmail.com', username='admin1', password=str(hashlib.md5("123456".encode('utf-8')).hexdigest()), user_role=UserRole.ADMIN)
        db.session.add(u)
        db.session.commit()

        hv1 = HangVe(tenHangVe='Hạng 1')
        hv2 = HangVe(tenHangVe='Hạng 2')
        db.session.add(hv1)
        db.session.add(hv2)
        sb1 = SanBay(tenSB='TP Hồ Chí Minh')
        sb2 = SanBay(tenSB='Hà Nội')
        sb3 = SanBay(tenSB='Đà Nẵng')
        sb4 = SanBay(tenSB='Phú Quốc')

        tb1 = TuyenBay(tenTB="SGN-HN", san_bay_di_id=1, san_bay_den_id=2)
        tb2 = TuyenBay(tenTB="HN-SGN", san_bay_di_id=2, san_bay_den_id=1)
        tb3 = TuyenBay(tenTB="DNG-SGN", san_bay_di_id=3, san_bay_den_id=1)
        tb4 = TuyenBay(tenTB="DNG-PQ", san_bay_di_id=3, san_bay_den_id=4)

        mb1 = MayBay(tenMB='Airbus01')
        mb2 = MayBay(tenMB='Airbus02')
        cb1 = ChuyenBay(tenCB='SGN-HN01', ngayBay='2024/01/01 19:00:00', thoiGianBay='02:30:00', tuyen_bay_id=1, may_bay_id=1)
        cb2 = ChuyenBay(tenCB='SGN-HN02', ngayBay='2024/02/01 19:00:00', thoiGianBay='02:30:00', tuyen_bay_id=1, may_bay_id=2)
        cb3 = ChuyenBay(tenCB='DNG_SGN01', ngayBay='2023/12/01 10:00:00', thoiGianBay='01:30:00', tuyen_bay_id=3, may_bay_id=1)
        cb4 = ChuyenBay(tenCB='DNG-PQ01', ngayBay='2024/01/01 20:00:00', thoiGianBay='01:30:00', tuyen_bay_id=4, may_bay_id=2)

        db.session.add(sb1)
        db.session.add(sb2)
        db.session.add(sb3)
        db.session.add(sb4)

        db.session.add(mb1)
        db.session.add(mb2)

        db.session.add(cb1)
        db.session.add(cb2)
        db.session.add(cb3)
        db.session.add(cb4)

        db.session.add(tb1)
        db.session.add(tb2)
        db.session.add(tb3)
        db.session.add(tb4)

        db.session.commit()






