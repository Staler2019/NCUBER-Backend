import flask
from flask_sqlalchemy import SQLAlchemy
from flask import request, json, jsonify, Response
from sqlalchemy.orm import sessionmaker
from datetime import datetime
app = flask.Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///uberdb_empty.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII']=False
db = SQLAlchemy(app)
CLIENT_ID='iBTFJjVUJQ7uZa4MVLXRcM2WLN6S1P'
# Models


class PERSON(db.Model):
    uid = db.Column('uid', db.Integer, primary_key=True)
    phone = db.Column('phone', db.String(10))
    now_carId = db.Column('now_carId', db.Integer)
    student_id = db.Column('stuId', db.String(9))
    name = db.Column('name', db.String(30))
    gender = db.Column('gender', db.Integer)
    department = db.Column('dep', db.Integer)
    grade = db.Column('grade', db.Integer)

    def __init__(self, phone, now_carId, student_id, name, gender, department, grade):
        self.phone = phone
        self.now_carId = now_carId
        self.student_id = student_id
        self.name = name
        self.gender = gender
        self.department = department
        self.grade = grade


class CAR(db.Model):
    Id = db.Column('Id', db.Integer, primary_key=True)
    launch_person_Stuid = db.Column('launch_person_Stuid', db.String(50))
    start_time = db.Column('start_time', db.String(50))
    start_loc = db.Column('start_loc', db.String(50))
    end_time = db.Column('end_time', db.String(50))
    end_loc = db.Column('end_loc', db.String(50))
    persons_num_limit = db.Column('persons_num_limit', db.Integer)
    gender_limit = db.Column('gender_limit', db.Integer)
    roomTitle = db.Column('roomTitle', db.String(50))
    remark = db.Column('remark', db.String(50))

    def __init__(self, launch_person_Stuid, start_time, start_loc, end_time, end_loc, persons_num_limit, gender_limit, roomTitle, remark):
        self.launch_person_Stuid = launch_person_Stuid
        self.start_time = start_time
        self.start_loc = start_loc
        self.end_time = end_time
        self.end_loc = end_loc
        self.persons_num_limit = persons_num_limit
        self.gender_limit = gender_limit
        self.roomTitle = roomTitle
        self.remark = remark


class CARPOOL(db.Model):
    Id = db.Column('Id', db.Integer, primary_key=True)
    carId = db.Column('carId', db.Integer)
    studentId = db.Column('studentId', db.Integer)

    def __init__(self, carId, studentId):
        self.carId = carId
        self.studentId = studentId


@app.route("/")
def index():
    db.create_all()
    return "redirect /insert_person <br> and redirect to /view_people"

# test1


@app.route("/insert_person")
def insert_person():
    person = PERSON('0912345678', 12, '108502000',
                    'NewStudent', 1, 502, 4)
    db.session.add(person)
    db.session.commit()
    return "insert_person_test_completed"


# test2
@app.route("/view_people")
def view_person():
    datas = PERSON.query.all()
    msg = ""
    for person in datas:
        msg += f"{person.uid}, {person.phone}, {person.now_carId}, {person.student_id}, {person.name}, {person.gender}, {person.department}, {person.grade}<br>"
    return msg


@app.route("/insert_car")
def insert_car():
    car = CAR(87, datetime(2038,1,19,3,14,7), '工程五館',
              datetime(2038,1,19,3,54,38), '你家', 999, 1, '回家的路', '100分')
    db.session.add(car)
    db.session.commit()
    return "insert_car_test_completed"


@app.route("/view_car")
def view_car():
    datas = CAR.query.all()
    msg = ""
    for car in datas:
        msg += f"{car.Id}, {car.launch_person_Stuid}, {car.start_time}, {car.start_loc}, {car.end_time}, {car.end_loc}, {car.persons_num_limit},  {car.gender_limit},{car.roomTitle}, {car.remark}<br>"
    return msg

@app.route("/view_carpool")
def view_carpool():
    datas = CARPOOL.query.all()
    msg = ""
    for carpool in datas:
        msg += f"{carpool.carId}, {carpool.studentId}<br>"
    return msg

@app.route("/delete_last_car")
def deletelastcar():
    car=CAR.query.all()[-1]
    db.session.delete(car)
    db.session.commit()
    return "car deleted "

@app.route("/delete_last_person")
def deletelastPerson():
    person=PERSON.query.all()[-1]
    db.session.delete(person)
    db.session.commit()
    return "person deleted"

@app.route("/backEnd_post_test", methods=['POST', 'GET'])
def receive_data():
    if request.method=='POST':
        headers=request.headers
        clientId=headers.get('clientId')
        if clientId==CLIENT_ID:
            data={'Hello': '123',
                  '哈囉 ': '一二三'}
            json_str=json.dumps(data, ensure_ascii=False)
            response=Response(json_str, content_type="charset=utf-8")
            return response
        else:
            return jsonify("wrong cilent id")
    else:
        return jsonify("get data failed")

def verifiedReq(request, dataType):
    return (
        (request.method == "POST")
        and (request.headers.get("clientId") == CLIENT_ID)
        and (request.json["type"] == dataType)
    )


def getPeopleInACar(carId):
    # peopleIntheCar = PERSON.query.filter_by(now_carId=carId).all()
    # or
    peopleInTheCar = CARPOOL.query.filter_by(carId=carId).all()
    return [person.studentId for person in peopleInTheCar]


def getCarHists(stuId):
    cars = CARPOOL.query.filter_by(studentId=stuId).all()
    return [car.carId for car in cars]

@app.route("/req_latest_nums_of_carModel", methods=['POST', 'GET'])
def req_latest_carPools():
    if request.method=='POST':
        headers=request.headers
        clientId=headers.get('clientId')
        if clientId==CLIENT_ID:
            data=request.json
            cars=[]
            if data['type']=='req_nums_of_cars':
                db_cars = CAR.query.all()
                numbers = len(db_cars)
                for i in range(numbers):
                    car_rows=db_cars[-i]
                    latest_carId=car_rows.Id
                    # print("latest_carId= ", latest_carId)
                    stuids = getPeopleInACar(latest_carId)
                    print(stuids)
                    car={'carId':car_rows.Id,
                                'stuIds' : stuids,
                                "roomTitle": car_rows.roomTitle,
                                "launchStuId": str(car_rows.launch_person_Stuid),
                                "remark": car_rows.remark,
                                "startTime": car_rows.start_time,
                                "startLoc": car_rows.start_loc,
                                "endTime": car_rows.end_time,
                                "endLoc": car_rows.end_loc,
                                "personNumLimit": car_rows.persons_num_limit,
                                "genderLimit": car_rows.gender_limit}
                    cars.append(car)
            response={
                'type': 'req_nums_of_cars',
                'cars':cars
            }
            return jsonify(response)
        else:
            return jsonify("client id wrong")
    else:
        return jsonify("get data failed")

@app.route("/req_car_model_byid", methods=['POST', 'GET'])
def reqCarModelById():
    if request.method=='POST':
        headers=request.headers
        clientId=headers.get('clientId')
        if clientId==CLIENT_ID:
            data=request.json
            if data['type']=='req_car_by_id':
                curr_car = CAR.query.filter_by(Id = data['carId']).first()
                curr_carId=curr_car.Id
                stuids=[]
                peopleIntheCar = PERSON.query.filter_by(now_carId = curr_carId).all()
                for Ids in peopleIntheCar:
                    stuids.append(Ids.student_id)

                response={'type': 'req_car_by_id',
                    'carId':curr_car.Id,
                     'stuIds' : stuids,
                     "roomTitle": curr_car.roomTitle,
                     "launchStuId": str(curr_car.launch_person_Stuid),
                     "remark": curr_car.remark,
                     "startTime": curr_car.start_time,
                     "startLoc": curr_car.start_loc,
                     "endTime": curr_car.end_time,
                     "endLoc": curr_car.end_loc,
                     "personNumLimit": curr_car.persons_num_limit,
                     "genderLimit": curr_car.gender_limit}
            return jsonify(response)
        else:
            return("client id wrong")
    else:
        return jsonify("get data failed")


@app.route("/send_person_model", methods=['POST', 'GET'])
def sendPersonModel():
    if request.method=='POST':
        headers=request.headers
        clientId=headers.get('clientId')
        if clientId==CLIENT_ID:
            data=request.json
            if data['type']=='send_person':
                #__init__(self, phone, now_carId, student_id, name, gender, department, grade):
                student=PERSON.query.filter_by(student_id=data['stuId']).first()
                if not student:
                    person = PERSON(data['phone'], None, data['stuId'],data['name'], data['gender'], data['department'], data['grade'])
                    db.session.add(person)
                    db.session.commit()
                else:
                    student.phone=data['phone']
                    student.name=data['name']
                    student.gender=data['gender']
                    student.department=data['department']
                    student.grade=data['grade']
                    db.session.commit()

                student=PERSON.query.filter_by(student_id=data['stuId']).first()
                carHists = getCarHists(data["stuId"])
                response={
                    'type':'send_person',
                    "name": student.name,
                    "phone": student.phone,
                    "stuId": student.student_id,
                    "gender": student.gender,
                    "department": student.department,
                    "grade": student.grade, # 年級
                    "carIdHists": carHists,
                    "nowCarId": student.now_carId }
                return jsonify(response)
        else:
            return jsonify("client id wrong")
    else:
        return jsonify("get data failed")

# create car but not adding launch person to car
@app.route("/send_car_model", methods=["POST"])
def sendCarModel():
    if not verifiedReq(request, "send_car"):
        return jsonify("get data failed")

    else:
        data = request.json
        #__init__(self, launch_person_Stuid, start_time, start_loc, end_time, end_loc, persons_num_limit, gender_limit, roomTitle, remark):
        car = CAR(data['launchStuId'], data['startTime'], data['startLoc'], data['endTime'], data['endLoc'], data['personNumLimit'], data['genderLimit'], data['roomTitle'], data['remark'])
        db.session.add(car)
        db.session.commit()

        last_car = CAR.query.order_by(None).order_by(CAR.Id.desc()).first()
        # carpool=CARPOOL(last_car.Id, data['launchStuId'])
        # db.session.add(carpool)
        launch_person=PERSON.query.filter_by(student_id=data['launchStuId']).first()
        launch_person.now_carId=last_car.Id
        db.session.commit()
            # print("last car=", last_car.Id)
            # curr_carpools=CARPOOL.query.filter_by(carId=last_car.Id).all()
            # stuidsIntheCarpool=[]
            # for carpool in curr_carpools:
            #     stuidsIntheCarpool.append(carpool.studentId)
            # print(stuidsIntheCarpool)
        stuIds = getPeopleInACar(last_car.Id)
        response={'type':'send_car',
                        "carId": last_car.Id,
                        "stuIds": stuIds,
                        "roomTitle": last_car.roomTitle,
                        "launchStuId": str(last_car.launch_person_Stuid),
                        "remark":last_car.remark ,
                        "startTime": last_car.start_time,
                        "startLoc": last_car.start_loc,
                        "endTime":last_car.end_time,
                        "endLoc":last_car.end_loc ,
                        "personNumLimit": last_car.persons_num_limit,
                        "genderLimit": last_car.gender_limit}

        return jsonify(response)

@app.route("/addPersonToCar", methods=['POST','GET'])
def addPersonToCar():
    if request.method == 'POST':
        headers = request.headers
        clientId = headers.get('clientId')

        if clientId == CLIENT_ID:
            data = request.json
            user = PERSON.query.filter_by(student_id = data['stuId']).first()
            car = CAR.query.filter_by(Id = data['carId']).first()
            people = PERSON.query.filter_by(now_carId = data['carId']).all()
            people_num = len(people)
            print("len= ", people_num)
            if people_num < car.persons_num_limit or user.gender == car.gender_limit:
                user.now_carId = data['carId']
                new_carpool=CARPOOL(data['carId'], data['stuId'])
                db.session.add(new_carpool)
                db.session.commit()
                status = 1
            else:
                status = 2
            try:
                response = {'type':'add_person_to_car',
                            'status': status}
                # status: success/carFull/otherFail: 1/2/3 前端判斷是否發車(看時間)
                return jsonify(response)
            except:
                return "addPersonToCar fetch data error";
        else:
            return jsonify("user not exist")
    else:
        return jsonify('get data failed')


@app.route("/rmPersonFromCar", methods=['POST'])
def rmPersonFromCar():
    if request.method == 'POST':
        headers = request.headers
        clientId = headers.get('clientId')

        # 1. car裡的學號沒被刪掉
        # 2. 學號空了就把房間刪掉

        if clientId == CLIENT_ID:
            data = request.json
            user = PERSON.query.filter_by(student_id = data['stuId']).first()
            del_carpool_by_stuid= CARPOOL.query.filter_by(studentId=data['stuId']).all()[-1]
            print("del Carpool carid= ",del_carpool_by_stuid.carId)

            if user.now_carId == data['carId']:
                user.now_carId=None
                db.session.delete(del_carpool_by_stuid)
                db.session.commit()
                carpool_for_current_carId=CARPOOL.query.filter_by(carId=data['carId']).first()
                if not carpool_for_current_carId:
                    car=CAR.query.filter_by(Id=data['carId']).first()
                    db.session.delete(car)
                    db.session.commit()
                status = 1
            else:
                status = 2
            try:
                response = {'type':'rm_person_from_car',
                            'status': status
                        }
                # status: success/fail: 1/2
                return jsonify(response)
            except:
                return "rmPersonFromCar fetch data error";
        else:
            return jsonify("user not exist")
    else:
        return jsonify('get data failed')


@app.route("/reqPersonModelByStuIdName", methods=['POST'])
def reqPersonModelByStuId():
    if request.method == 'POST':
        headers = request.headers
        # clientId = headers.get('Authorization')
        clientId = headers.get('clientId')

        if clientId == CLIENT_ID:
            data = request.json
            user = PERSON.query.filter_by(student_id = data['stuId']).first()


            if user.name != data['name']:
                return jsonify('request error')
            else :
                try:
                    carIdHists = []
                    response = {'type':'req_person_by_stuId_name',
                                'name': user.name,
                                'phone': user.phone,
                                'stuId': user.student_id,
                                'gender': user.gender,
                                'department': user.department,
                                'grade': user.grade,
                                'carIdHists': carIdHists,
                                'nowCarId': user.now_carId,
                            }
                    return jsonify(response)
                except:
                    return "reqPersonModelByStuId fetch data error";
        else:
            return jsonify("user not exist")
    else:
        return jsonify('get data failed')


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(host='0.0.0.0', debug=False)
