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

    def __init__(self, birth_date, first_name, last_name, gender, hire_date):

        
        self.birth_date = birth_date
        self.first_name = first_name
        self.last_name = last_name
        self.gender = gender
        self.hire_date = hire_date





@app.route('/')

def hell():
    return 'hello man'

@app.route('/index')

def index():

    all_data = Employee.query.all()
    
    return render_template("list.html", emp = all_data)


@app.route('/register', methods=['POST'])

def register():



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


@app.route('/update', methods=['GET', 'POST'])

def update():

    if request.method == 'POST':

        my_data = Employee.query.get(request.form.get('emp_no'))

        my_data.first_name = request.form['first_name']

        my_data.last_name = request.form['last_name']

        my_data.birth_date = request.form['birth_date']

        my_data.gender = request.form['gender']

        my_data.hire_date = request.form['hire_date']

        db.session.commit()

        return redirect(url_for('index'))


@app.route('/delete/<emp_no>/', methods=['GET', 'POST'])

def delete(emp_no):
    my_data = Employee.query.get(emp_no)

    db.session.delete(my_data)

    db.session.commit()

    return redirect(url_for('index'))



if __name__ == "__main__":
    app.run(debug=True)