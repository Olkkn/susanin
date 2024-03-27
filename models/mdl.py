class User:
    def __init__(self, user_id, user_name, email, password, role):
        self.user_id = user_id
        self.user_name = user_name
        self.email = email
        self.password = password
        self.role = role


class Area:
    def __init__(self, coordinates, area_id, address, area_status):
        self.area_id = area_id
        self.coordinates = coordinates
        self.address = address
        self.status = area_status


class Task:
    def __init__(self, task_id, area_id, doer, master, start_date, done_date, task_status, photo):
        self.task_id = task_id
        self.area_id = area_id
        self.doer = doer
        self.master = master
        self.start_date = start_date
        self.done_date = done_date
        self.task_status = task_status
        self.photo = photo


class Photo:
    def __init__(self, photo_id, task_id, area_id, take_date, file_name):
        self.photo_id = photo_id
        self.task_id = task_id
        self.area_id = area_id
        self.take_date = take_date
        self.file_name = file_name

