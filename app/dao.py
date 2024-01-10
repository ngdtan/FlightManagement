from app.models import ChuyenBay, TuyenBay, SanBay, MayBay, NguoiDung
from app import app, db
import hashlib
def load_flights(tuyen_bay=None, page=None):
    flights = ChuyenBay.query
    if tuyen_bay:
        flights = flights.filter(ChuyenBay.tenCB.contains(tuyen_bay))

    if page:
        page = int(page)
        page_size = app.config['PAGE_SIZE']
        start = (page - 1)*page_size

        return flights.slice(start, start + page_size)

    return flights.all()


def count_flight():
    return ChuyenBay.query.count()

def load_airpots():
    airpots = SanBay.query
    return airpots.all()

def load_routes():
    routes = TuyenBay.query
    return routes.all()

def get_user_by_id(user_id):
    return NguoiDung.query.get(user_id)

def auth_user(username, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

    return NguoiDung.query.filter(NguoiDung.username.__eq__(username.strip()),
                                  NguoiDung.password.__eq__(password)).first()

def add_user(username, password, hoTen, CCCD, SDT, email):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    u = NguoiDung(username=username, password=password, hoTen=hoTen, CCCD=CCCD, SDT=SDT, email=email)
    db.session.add(u)
    db.session.commit()