from flask import Flask,render_template,request,session,url_for,redirect,jsonify

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.secret_key = "9486"

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Mariaselvam@96@localhost/flasksqlalchemy'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Employee(db.Model):



    emp_no = db.Column(db.Integer(), primary_key=True)
    birth_date = db.Column(db.Date())
    first_name = db.Column(db.String(14), nullable=False)

    last_name = db.Column(db.String(16), nullable=False)

    gender = db.Column(db.Enum('Male', 'Female'))

    hire_date = db.Column(db.Date())

    dep_emp_map = db.relationship("DepartmentEmployee", backref='employee')

    dep_man_map = db.relationship("DepartmentManager", backref='employee')

    emp_salary = db.relationship("Salary", backref='employee')

    emp_title = db.relationship("Title", backref='employee')

    

    

    def __init__(self, birth_date, first_name, last_name, gender, hire_date):

        
        self.birth_date = birth_date
        self.first_name = first_name
        self.last_name = last_name
        self.gender = gender
        self.hire_date = hire_date

class Department(db.Model):

    dep_no = db.Column(db.Integer(), primary_key=True)
    department_name = db.Column(db.String(20), nullable=False)

    dep_emp_map = db.relationship("DepartmentEmployee", backref='department')

    dep_man_map = db.relationship("DepartmentManager", backref='department')




    def __init__(self, department_name):

        self.department_name = department_name


class DepartmentEmployee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    emp_no = db.Column(db.Integer, db.ForeignKey(Employee.emp_no))
    dep_no = db.Column(db.Integer, db.ForeignKey(Department.dep_no))
    from_date = db.Column(db.Date())
    to_date = db.Column(db.Date())

    def __init__(self, emp_no, dep_no, from_date, to_date):

        self.emp_no = emp_no
        self.dep_no = dep_no
        self.from_date = from_date
        self.to_date = to_date


class DepartmentManager(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dep_no = db.Column(db.Integer, db.ForeignKey(Department.dep_no))

    emp_no = db.Column(db.Integer, db.ForeignKey(Employee.emp_no))
    from_date = db.Column(db.Date())
    to_date = db.Column(db.Date())

    def __init__(self, dep_no, emp_no, from_date, to_date):
        self.dep_no = dep_no
        self.emp_no = emp_no
        self.from_date = from_date
        self.to_date = to_date

class Salary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    emp_no = db.Column(db.Integer, db.ForeignKey(Employee.emp_no))
    salary = db.Column(db.Integer)
    from_date = db.Column(db.Date())
    to_date = db.Column(db.Date())

    def __init__(self, emp_no, salary, from_date, to_date):
        self.emp_no = emp_no
        self.salary = salary
        self.from_date = from_date
        self.to_date = to_date

class Title(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    emp_no = db.Column(db.Integer, db.ForeignKey(Employee.emp_no))
    title = db.Column(db.String(30))
    from_date = db.Column(db.Date())
    to_date = db.Column(db.Date())

    def __init__(self, emp_no, title, from_date, to_date):
        self.emp_no = emp_no
        self.title = title
        self.from_date = from_date
        self.to_date = to_date


@app.route('/')

def hell():
    return 'hello man'

@app.route('/index')

def index():

    employees = Employee.query.all()

    departments = Department.query.all()

    departmentemployees = DepartmentEmployee.query.all()

    departmentmanagers = DepartmentManager.query.all()

    salaries = Salary.query.all()

    titles = Title.query.all()



    
    return render_template(
        "list.html",
         employees=employees, 
         departments=departments, 
         departmentemployees=departmentemployees,
         departmentmanagers=departmentmanagers,
         salaries=salaries,
         titles=titles
         )


@app.route('/insertemployee', methods=['POST'])

def insertemployee():



      if request.method == 'POST':

          first_name = request.form['first_name']

          last_name = request.form['last_name']

          birth_date = request.form['birth_date']

          gender = request.form['gender']

          hire_date = request.form['hire_date']

          my_data = Employee(birth_date=birth_date, first_name=first_name, last_name=last_name, gender=gender, hire_date=hire_date)

          db.session.add(my_data)
          db.session.commit()

          return redirect(url_for('index'))


@app.route('/updateemployee', methods=['GET', 'POST'])

def updateemployee():

    if request.method == 'POST':

        my_data = Employee.query.get(request.form.get('emp_no'))

        my_data.first_name = request.form['first_name']

        my_data.last_name = request.form['last_name']

        my_data.birth_date = request.form['birth_date']

        my_data.gender = request.form['gender']

        my_data.hire_date = request.form['hire_date']

        db.session.commit()

        return redirect(url_for('index'))


@app.route('/deleteemployee/<emp_no>/', methods=['GET', 'POST'])

def deleteemployee(emp_no):
    my_data = Employee.query.get(emp_no)

    db.session.delete(my_data)

    db.session.commit()

    return redirect(url_for('index'))


@app.route('/insertdepartment', methods=['GET', 'POST'])

def insertdepartment():

    if request.method == 'POST':

        department_name = request.form['department_name']

        data = Department(department_name=department_name)

        db.session.add(data)

        db.session.commit()

        return redirect(url_for('index'))


@app.route('/deletedepartment/<dep_no>/', methods=['GET', 'POST'])

def deletedepartment(dep_no):
    department = Department.query.get(dep_no)

    db.session.delete(department)

    db.session.commit()

    return redirect(url_for('index'))

@app.route('/updatedepartment', methods=['GET', 'POST'])

def updatedepartment():

    if request.method == 'POST':

        department = Department.query.get(request.form.get('dep_no'))


        department.department_name = request.form['department_name']

        db.session.commit()

        return redirect(url_for('index'))


@app.route('/insertdepartmentemployee', methods=['GET', 'POST'])

def insertdepartmentemployee():

    if request.method == 'POST':

        emp_no = request.form['emp_no']

        dep_no = request.form['dep_no']

        from_date = request.form['from_date']

        to_date = request.form['to_date']

        my_depemp = DepartmentEmployee(emp_no=emp_no, dep_no=dep_no, from_date=from_date, to_date=to_date)

        db.session.add(my_depemp)

        db.session.commit()

        return redirect(url_for('index'))

@app.route('/updatedepartmentemployee', methods=['GET', 'POST'])

def updatedepartmentemployee():

    if request.method == 'POST':
        

        up_depemp = DepartmentEmployee.query.get(request.form.get('id'))

        up_depemp.emp_no = request.form['emp_no']

        up_depemp.dep_no = request.form['dep_no']

        up_depemp.from_date = request.form['from_date']

        up_depemp.to_date = request.form['to_date']

        db.session.commit()

        return redirect(url_for('index'))


@app.route('/deletedepartmentemployee/<id>', methods=['GET', 'POST'])

def deletedepartmentemployee(id):

    dep_emp_id = DepartmentEmployee.query.get(id)

    db.session.delete(dep_emp_id)

    db.session.commit()

    return redirect(url_for('index'))





@app.route('/insertdepartmentmanager', methods=['GET', 'POST'])

def insertdepartmentmanager():

    if request.method == 'POST':

        emp_no = request.form['emp_no']

        dep_no = request.form['dep_no']

        from_date = request.form['from_date']

        to_date = request.form['to_date']

        my_depman = DepartmentManager(emp_no=emp_no, dep_no=dep_no, from_date=from_date, to_date=to_date)

        db.session.add(my_depman)

        db.session.commit()

        return redirect(url_for('index'))

@app.route('/updatedepartmentmanager', methods=['GET', 'POST'])

def updatedepartmentmanager():

    if request.method == 'POST':

        up_depman = DepartmentManager.query.get(request.form.get('id'))

        up_depman.emp_no = request.form['emp_no']

        up_depman.dep_no = request.form['dep_no']

        up_depman.from_date = request.form['from_date']

        up_depman.to_date = request.form['to_date']

        db.session.commit()

        return redirect(url_for('index'))


@app.route('/deletedepartmentmanager/<id>', methods=['GET', 'POST'])

def deletedepartmentmanager(id):

    dep_man_id = DepartmentManager.query.get(id)

    db.session.delete(dep_man_id)

    db.session.commit()

    return redirect(url_for('index'))

@app.route('/insertsalary', methods=['GET', 'POST'])

def insertsalary():

    if request.method == 'POST':

        emp_no = request.form['emp_no']

        salary = request.form['salary']

        from_date = request.form['from_date']

        to_date = request.form['to_date']

        ins_salary = Salary(emp_no=emp_no, salary=salary, from_date=from_date, to_date=to_date)

        db.session.add(ins_salary)

        db.session.commit()

        return redirect(url_for('index'))


@app.route('/updatesalary', methods=['GET', 'POST'])

def updatesalary():

    up_salary = Salary.query.get(request.form.get('id'))

    up_salary.emp_no = request.form['emp_no']

    up_salary.salary = request.form['salary']

    up_salary.from_date = request.form['from_date']

    up_salary.to_date = request.form['to_date']

    db.session.commit()

    return redirect(url_for('index'))


@app.route('/deletesalary/<id>', methods=['GET', 'POST'])

def deletesalary(id):

    salary = Salary.query.get(id)

    db.session.delete(salary)

    db.session.commit()

    return redirect(url_for('index'))




@app.route('/inserttitle', methods=['GET', 'POST'])

def inserttitle():

    if request.method == 'POST':

        emp_no = request.form['emp_no']

        title = request.form['title']

        from_date = request.form['from_date']

        to_date = request.form['to_date']

        ins_title = Title(emp_no=emp_no, title=title, from_date=from_date, to_date=to_date)

        db.session.add(ins_title)

        db.session.commit()

        return redirect(url_for('index'))


@app.route('/updatetitle', methods=['GET', 'POST'])

def updatetitle():

    up_title = Title.query.get(request.form.get('emp_no'))

    up_title.emp_no = request.form['emp_no']

    up_title.title = request.form['title']

    up_title.from_date = request.form['from_date']

    up_title.to_date = request.form['to_date']

    db.session.commit()

    return redirect(url_for('index'))


@app.route('/deletetitle/<id>', methods=['GET', 'POST'])

def deletetitle(id):

    title = Title.query.get(id)

    db.session.delete(title)

    db.session.commit()

    return redirect(url_for('index'))

    







if __name__ == "__main__":
    app.run(debug=True)
