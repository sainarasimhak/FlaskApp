from typing import List, Dict
import simplejson as json
from flask import Flask, request, Response, redirect, session
from flask import render_template
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor
from forms import LoginForm
from flask_login import login_required, logout_user
from flask_session import Session

app = Flask(__name__)

mysql = MySQL(cursorclass=DictCursor)

sess = Session()

app.config.from_object('config.Config')

app.config['MYSQL_DATABASE_HOST'] = 'db'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['MYSQL_DATABASE_DB'] = 'namedb'
mysql.init_app(app)

sess.init_app(app)

@app.route('/', methods=['GET'])
def index():
    user = {'username': 'SaiK'}
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM details')
    result = cursor.fetchall()
    return render_template('index.html', title='Home', user=user, persons=result)


@app.route('/view/<int:person_id>', methods=['GET'])
def record_view(person_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM details WHERE id=%s', person_id)
    result = cursor.fetchall()
    return render_template('view.html', title='View Form', person=result[0])


@app.route('/edit/<int:person_id>', methods=['GET'])
def form_edit_get(person_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM details WHERE id=%s', person_id)
    result = cursor.fetchall()
    return render_template('edit.html', title='Edit Form', person=result[0])


@app.route('/edit/<int:person_id>', methods=['POST'])
def form_update_post(person_id):
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('first_name'), request.form.get('last_name'), request.form.get('company_name'),
                 request.form.get('address'), request.form.get('phone'), person_id)
    sql_update_query = """UPDATE details d SET d.first_name = %s, d.last_name = %s, d.company_name = %s, d.address = %s, 
                        d.phone = %s WHERE d.id = %s """
    cursor.execute(sql_update_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/person/new', methods=['GET'])
def form_insert_get():
    return render_template('new.html', title='New Person Form')


@app.route('/person/new', methods=['POST'])
def form_insert_post():
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('first_name'), request.form.get('last_name'), request.form.get('company_name'),
                 request.form.get('address'), request.form.get('phone'))
    sql_insert_query = """INSERT INTO details (first_name,last_name, company_name, address, phone) 
                VALUES (%s,%s,%s,%s,%s)"""
    cursor.execute(sql_insert_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/delete/<int:person_id>', methods=['POST'])
def form_delete_post(person_id):
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM details WHERE id = %s """
    cursor.execute(sql_delete_query, person_id)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/api/v1/people', methods=['GET'])
def api_browse() -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM details')
    result = cursor.fetchall()
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/people/<int:person_id>', methods=['GET'])
def api_retrieve(person_id) -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM details WHERE id=%s', person_id)
    result = cursor.fetchall()
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/people/<int:person_id>', methods=['PUT'])
def api_edit(person_id) -> str:
    cursor = mysql.get_db().cursor()
    content = request.json
    inputData = (content['first_name'], content['last_name'], content['company_name'],
                 content['address'], content['phone'], person_id)
    sql_update_query = """UPDATE details d SET d.first_name = %s, d.last_name = %s, d.company_name = %s, d.address = %s, 
                        d.phone = %s WHERE d.id = %s """
    cursor.execute(sql_update_query, inputData)
    mysql.get_db().commit()
    resp = Response(status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/people', methods=['POST'])
def api_add() -> str:
    content = request.json
    cursor = mysql.get_db().cursor()
    inputData = (content['first_name'], content['last_name'], content['company_name'],
                 content['address'], content['phone'])
    sql_insert_query = """INSERT INTO details (first_name, last_name, company_name, address, phone) 
                VALUES (%s,%s,%s,%s,%s)"""
    cursor.execute(sql_insert_query, inputData)
    mysql.get_db().commit()
    resp = Response(status=201, mimetype='application/json')
    return resp


@app.route('/api/v1/people/<int:person_id>', methods=['DELETE'])
def api_delete(person_id) -> str:
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM details WHERE id = %s"""
    cursor.execute(sql_delete_query, person_id)
    mysql.get_db().commit()
    resp = Response(status=200, mimetype='application/json')
    return resp

@app.route('/signup', methods=['GET', 'POST'])
def signup_page():
    return render_template(
        '/signup.jinja2',
        title='Create an Account.',
        form=SignupForm(),
        template='signup-page',
        body="Sign up for a user account."
    )


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    return render_template(
        '/login.html',
        title='Create an Account.',
        form=LoginForm,
        template='login-page',
        body="Log in to your account."
    )

@app.route("/session", methods=["GET"])
@login_required
def session_view():
    """Display session variable value."""
    return render_template(
        "session.jinja2",
        title="Flask-Session Tutorial.",
        template="dashboard-template",
        session_variable=str(session["redis_test"]),
    )

@app.route('/', methods=['GET'])
@login_required
def dashboard():
    """Logged-in User Dashboard."""
    return render_template(
        'dashboard.jinja2',
        title='Flask-Login Tutorial.',
        template='dashboard-template',
        current_user=current_user,
        body="You are now logged in!"
    )


@app.route("/logout")
@login_required
def logout():
    """User log-out logic."""
    logout_user()
    return redirect(url_for('login.html'))


@app.errorhandler(404)
def not_found(arg):
    """Page not found."""
    return render_template('404.html', title='404 error.', message='Page Not Found')


@app.errorhandler(400)
def bad_request():
    """Bad request."""
    return render_template('400.html', title='400 error.', message='Bad request.  Page Not Found')


@app.errorhandler(500)
def server_error(arg):
    """Internal server error."""
    return render_template('500.html', message='Server Error')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
