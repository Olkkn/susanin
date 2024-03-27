from models.mdl import User, Area, Photo, Task
from datetime import datetime

class UserRepo:
    def __init__(self):
        self._users = {}
        self._id = 0

    def create_user(self, name, role, email, password):
        self._id += 1
        u = User(user_name=name, role=role, email=email, password=password, user_id=self._id)
        self._users[u.user_id] = u

    def get_all_users(self):
        return self._users.values()

    def get_info(self, filter_name, filter_value):
        return filter(lambda u: u.__dict__[filter_name] == filter_value, self._users.values())

    def find_user_by_name(self, name):
        for k, u in self._users:
            if u.name == name:
                return u

    def find_user_by_id(self, user_id):
        for k, u in self._users.items():
            if u.user_id == user_id:
                return u
        return None

    def login(self, email, password):
        for k, u in self._users.items():
            if u.email == email:
                if u.password == password:
                    return True, u.user_id
        return False, None


class AreaRepo:
    def __init__(self):
        self._areas = {}
        self._id = 0

    def create_area(self, coordinates, address, area_status):
        self._id += 1
        a = Area(coordinates=coordinates, address=address, area_status=area_status, area_id=self._id)
        self._areas[a.area_id] = a

    def get_areas(self):
        return self._areas.values()


    def get_info(self, filter_name, filter_value):
        return filter(lambda a: a.__dict__[filter_name] == filter_value, self._areas.values())

    def find_area_by_id(self, area_id):
        for k, a in self._areas.items():
            if a.area_id == area_id:
                return a
            print('area_id', a.area_id, '  ', area_id)

    def set_status(self, area_id,  new_area_status):
        for k, a in self._areas.items():
            if a.area_id == area_id:
                a.status = new_area_status

    def get_coordinates(self):
        res = []
        for k, a in self._areas.items():
            res.append(a.coordinates)
        return res


class PhotoRepo:
    def __init__(self):
        self._photos = {}
        self._id = 0

    def create_photo(self, task_number, area_id, take_date, file_name):
        self._id += 1
        p = Photo(photo_id=self._id, task_id=task_number, area_id=area_id, take_date=take_date, file_name=file_name)
        self._photos[task_number] = p

    def get_info(self, filter_name, filter_value):
        return filter(lambda p: p.__dict__[filter_name] == filter_value, self._photos.values())


class TaskRepo:
    def __init__(self):
        self._tasks = {}
        self._id = 0

    def create_task(self, area_id, doer, start_date, done_date, task_status, master, photo):
        self._id += 1
        t = Task(task_id=self._id, area_id=area_id, doer=doer, start_date=datetime.now().strftime("%d/%m/%y %I:%M"), done_date=done_date, task_status=task_status, master=master, photo=photo)
        self._tasks[t.task_id] = t
        return t

    def get_tasks(self):
        return self._tasks.values()

    def get_info(self, filter_name, filter_value):
        return filter(lambda t: t.__dict__[filter_name] == filter_value, self._tasks.values())

    def set_status(self, task_id,  new_task_status):
        for k, t in self._tasks.items():
            if t.task_id == task_id:
                t.task_status = new_task_status

    def get_user_tasks(self, user):
        res = []
        if user.role == 'master':

            print('user is master')
            for k, t in self._tasks.items():
                if t.master == user.user_id:
                    res.append(t)
        elif user.role == 'janitor':
            print('user is janitor')
            for k, t in self._tasks.items():
                if t.doer == user.user_id:
                    res.append(t)
        return res

    def set_done_date(self, task_id):
        for k, t in self._tasks.items():
            if t.task_id == task_id:
                t.done_date = datetime.now().strftime("%d/%m/%y %I:%M")

    def find_task_by_id(self, task_id):
        for k, a in self._tasks.items():
            if a.task_id == task_id:
                return a
