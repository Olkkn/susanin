from flask import Flask, render_template, request,flash, session, redirect, url_for
from werkzeug.utils import secure_filename
import os

class repositories(object):
    def __init__(self):
        self.task_repo = None
        self.user_repo = None
        self.area_repo = None

    def set_repos(self, user, area, task):
        self.user_repo = user
        self.area_repo = area
        self.task_repo = task

class TaskViewModel(object):
    def __init__(self, id, address, d_name, m_name, s_date, d_date, status):
        self.task_id = id
        self.area_address = address
        self.doer_name = d_name
        self.master_name = m_name
        self.start_date = s_date
        self.done_date = d_date
        self.status = status



app = Flask(__name__)
app.config['UPLOAD_FOLDER']="./photos"
app.config['MAX_CONTENT_PATH']=1024^3*50
app.secret_key = "!super_secret!"
repos = repositories()


@app.route("/")
def index():
    areas_data = [{"status": x.status, "coordinates": x.coordinates, "address": x.address} for x in
                      repos.area_repo.get_areas()]
    return render_template('index.html', areas_data=areas_data)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']
        logged, user_id  = repos.user_repo.login(login, password)

        if logged:
            session['user_id']=user_id
            print("set current user to", user_id)
            return redirect(url_for('tasks'))

        return render_template('login.html', wrong_pass=True)


@app.route("/tasks")
def tasks():

    user_id = session["user_id"]
    c_user = repos.user_repo.find_user_by_id(user_id)
    if user_id is not None:
        areas_data = [{"status": x.status, "coordinates": x.coordinates, "address": x.address} for x in
                      repos.area_repo.get_areas()]
        if c_user.role == 'master':

            return render_template('mastertasks.html',
                                    c_user_name=c_user.user_name,
                                    users=repos.user_repo.get_all_users(),
                                    areas=repos.area_repo.get_areas(),
                                    tasks=user_tasks_list(user_id),
                                    areas_data=areas_data)

        if c_user.role == 'janitor':
            return render_template('janitortasks.html',
                                   c_user_name=c_user.user_name,
                                   users=repos.user_repo.get_all_users(),
                                   areas=repos.area_repo.get_areas(),
                                   tasks=user_tasks_list(user_id),
                                   areas_data=areas_data)

    return redirect(url_for('login'))


@app.route("/tasks/<int:task_id>", methods=['GET', 'POST'])
def edit_tasks(task_id):
    user = repos.user_repo.find_user_by_id(session["user_id"])
    if user is not None:
        t = list(repos.task_repo.get_info(filter_name='task_id', filter_value=task_id))
        if request.method == 'GET':
            if len(t) > 0:
                task = t[0]
                if user.role == "janitor":
                    if task.doer == user.user_id:
                        return render_template('jedittask.html', task=task)

            if user.role == "master":
                pass

            return "Not found"
        if request.method == 'POST':

            status = request.form["status"]
            
            
            if 'photo_file' not in request.files:
                flash('no photo')
                print("no photo in form")
                return render_template('jedittask.html', task=t[0])

            task_photo = request.files['photo_file']
            fname = secure_filename(task_photo.filename)
            task_photo.save(os.path.join(app.config['UPLOAD_FOLDER'], fname))
         
            repos.task_repo.set_status(task_id, status)
            repos.task_repo.set_done_date(task_id)
            a_id = repos.task_repo.find_task_by_id(task_id).area_id
            repos.area_repo.set_status(a_id, status)
            return redirect(url_for('tasks'))
    else:
        return redirect(url_for('jedittask.html'))

@app.route("/logout")
def logout():
    session["user_id"] = None
    return redirect(url_for('index'))

@app.route("/newtask", methods=['GET', 'POST'])
def newtask():

    user_id = session["user_id"]
    a_user = repos.user_repo.find_user_by_id(user_id)

    if request.method == 'GET':
        if a_user.role == 'master':
            return render_template('newtask.html',
                                   users=repos.user_repo.get_info(filter_name='role', filter_value='janitor'),
                                                                areas=repos.area_repo.get_areas())
    if request.method == 'POST':
        selected_user = int(request.form['user_list'])
        selected_area = int(request.form['area_list'])

        t = repos.task_repo.create_task(area_id=selected_area, doer=selected_user,
                                        start_date='2024-02-10', done_date='--', task_status='Новая', master=a_user.user_id, photo='')

        print("t.area", t.area_id)

        return redirect(url_for('tasks'))



def run(user_repo, area_repo, task_repo):
    repos.set_repos(user_repo, area_repo, task_repo)
    app.run(host="localhost", port=8080, debug=True)


def user_tasks_list(user_id):
    result = []
    user = repos.user_repo.find_user_by_id(user_id)

    if user is not None:
        tasks = repos.task_repo.get_user_tasks(user)

        for t in tasks:
            doer = repos.user_repo.find_user_by_id(t.doer)
            master = repos.user_repo.find_user_by_id(t.master)
            area = repos.area_repo.find_area_by_id(t.area_id)
            print('find area: ', area, ' id ', t.area_id)
            tv = TaskViewModel(id=t.task_id, address=area.address,d_name=doer.user_name,
                           m_name=master.user_name, s_date=t.start_date, d_date=t.done_date, status=t.task_status)

            result.append(tv)

        return result

    return []