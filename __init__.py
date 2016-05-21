# -*- coding: utf-8 -*-
# Hello fellow developer, this project is coded using Flask framework, for more info visit http://flask.pocoo.org/
# Languages used: Python (Flask), Javascript (jQuery)
# If you're seeing this comment, I'm probably no longer working for HNG Appliances. My code is definitely not pretty as this is only my second project since I graduated from school. It was a result of my limited knowledge, google and stackoverflow. I will make sure the source code is well commented, but if you're confused, HMU at me@steventhan.net.

import flask, simplejson, json, datetime, random, string, gc, time
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, abort, request, session

from dbconnect import connection
from classes import *
from decimal import Decimal
from random import shuffle

from MySQLdb import escape_string as thwart
from flask_socketio import SocketIO, emit, join_room, leave_room, close_room, rooms, disconnect
from flask.ext import excel
from pyexcel.ext import xls, xlsx, ods, text



#SQLAlchemy imports, ORM was used since 01/24/2016, so there might be raw SQL in code developed prior that date
import flask.ext.login as flask_login
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin, login_required, roles_required, roles_accepted, current_user
from flask_security.utils import encrypt_password
from flask_mail import Mail
from flask_marshmallow import Marshmallow

#App config
app = Flask(__name__)
app.config['SECRET_KEY'] = 'super-secret'
app.config['TRAP_BAD_REQUEST_ERRORS'] = True

#Mysql config
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Steven93@localhost/hng'
app.config['SQLALCHEMY_BINDS'] = {
                                    'admin' : 'mysql://root:Steven93@localhost/admin'
                                    }

#Flask-security config
# app.config['SECURITY_REGISTERABLE'] = True
app.config['SECURITY_RECOVERABLE'] = True
# app.config['SECURITY_CONFIRMABLE'] = True
app.config['SECURITY_CHANGEABLE'] = True
app.config['SECURITY_PASSWORD_HASH'] = 'pbkdf2_sha512'
app.config['SECURITY_PASSWORD_SALT'] = '$2a$16$PnnIgfMwkOjGX4SkHqSOPO'
app.config['SECURITY_TOKEN_MAX_AGE'] = 10
app.config['SECURITY_POST_LOGIN_VIEW'] = '/internal/'
app.config['SECURITY_POST_LOGOUT_VIEW'] = '/login'


#Email config
app.config['SECURITY_EMAIL_SENDER'] = 'no-reply@hngappliances.com'
app.config['DEFAULT_MAIL_SENDER'] = 'no-reply@hngappliances.com'
app.config['MAIL_SERVER'] = 'mail.hngappliances.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'no-reply@hngappliances.com'
app.config['MAIL_PASSWORD'] = '%~?qL63t-EqK'
mail = Mail(app)



# Create database connection object
db = SQLAlchemy(app)
ma = Marshmallow(app)
socketio = SocketIO(app)


# Define Flask-SQLAlchemy models
roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')),
        info={'bind_key': 'admin'})

class Role(db.Model, RoleMixin):
    __bind_key__ ='admin'
    id = db.Column(db.Integer(), primary_key = True, unique = True)
    name = db.Column(db.String(80), unique = True)
    description = db.Column(db.String(255))



class User(db.Model, UserMixin):
    __bind_key__ ='admin'
    id = db.Column(db.Integer, primary_key = True, unique = True)
    email = db.Column(db.String(255), unique = True)
    password = db.Column(db.String(255))
    
    #Personal info
    first_name = db.Column(db.String(50), nullable = False)
    last_name = db.Column(db.String(50), nullable = False)
    job_title = db.Column(db.String(100), nullable = False)
    department = db.Column(db.String(50))
    start_date = db.Column(db.Date(), nullable = False)
    birth_date = db.Column(db.Date())
    ssn = db.Column(db.String(10))
    driver_license = db.Column(db.String(20))
    dl_expiration_date = db.Column(db.Date())
    gender = db.Column(db.Enum('', 'M', 'F'))
    phone = db.Column(db.String(30))
    phone2 = db.Column(db.String(30))

    #Address
    address1 = db.Column(db.String(255))
    address2 = db.Column(db.String(255))
    city = db.Column(db.String(100))
    state = db.Column(db.String(20))
    
    #Emergency contact
    econtact_name = db.Column(db.String(100))
    econtact_phone = db.Column(db.String(30))
    econtact_relationship = db.Column(db.String(100))
    
    #Account status
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))
    exams = db.relationship('UserExam', backref='user', lazy='dynamic')

class Exam(db.Model, UserMixin):
    __bind_key__ ='admin'
    id = db.Column(db.Integer, primary_key = True, unique = True)
    name = db.Column(db.String(255))
    description = db.Column(db.String(1000))
    start_date = db.Column(db.Date(), nullable = False)
    end_date = db.Column(db.Date())
    limit_minutes = db.Column(db.Integer)
    passphrase = db.Column(db.String(20))
    questions = db.relationship('Question', backref='exam', lazy='dynamic')
    users = db.relationship('UserExam', backref='exam', lazy='dynamic')

class Question(db.Model, UserMixin):
    __bind_key__ ='admin'
    id = db.Column(db.Integer, primary_key = True, unique = True)
    exam_id = db.Column(db.Integer, db.ForeignKey('exam.id'))
    question = db.Column(db.String(255), nullable = False)
    question_type = db.Column(db.Enum('Multiple Choice', 'Essay'))
    active = db.Column(db.Enum('T', 'F'))
    answers = db.relationship('Answer', backref='question', lazy='dynamic')

class Answer(db.Model, UserMixin):
    __bind_key__ ='admin'
    id = db.Column(db.Integer, primary_key = True, unique = True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    answer = db.Column(db.String(255), nullable = False)
    is_correct = db.Column(db.Enum('T', 'F'))

user_exam_answers = db.Table('user_exam_answers',
    db.Column('user_exam_id', db.Integer, db.ForeignKey('users_exams.id')),
    db.Column('answer_id', db.Integer, db.ForeignKey('answer.id')),
    info={'bind_key': 'admin'}
)

class UserExam(db.Model, UserMixin):
    __bind_key__ = 'admin'
    __tablename__ = 'users_exams'
    id = db.Column(db.Integer, primary_key = True, unique = True, nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    exam_id = db.Column(db.Integer, db.ForeignKey('exam.id'))
    score = db.Column(db.String(5))
    taken_date = db.Column(db.Date())
    is_available = db.Column(db.Enum('T', 'F'))
    answers = db.relationship("Answer", secondary = user_exam_answers)



class RoleSchema(ma.ModelSchema):
	class Meta:
		model = Role

class UserSchema(ma.ModelSchema):
	class Meta:
		model = User

class ExamSchema(ma.ModelSchema):
	class Meta:
		model = Exam

class QuestionSchema(ma.ModelSchema):
	class Meta:
		model = Question

class AnswerSchema(ma.ModelSchema):
	class Meta:
		model = Answer

class UserExamSchema(ma.ModelSchema):
	class Meta:
		model = UserExam

# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)
role_schema = RoleSchema()
roles_schema = RoleSchema(many = True)
user_schema = UserSchema()
users_schema = UserSchema(many = True)
exam_schema = ExamSchema()
exams_schema = ExamSchema(many = True)
question_schema = QuestionSchema()
questions_schema = QuestionSchema(many = True)
answer_schema = AnswerSchema()
answers_schema = AnswerSchema(many = True)
user_exam_schema = UserExamSchema()
users_exams_schema = UserExamSchema(many = True)







#################################################################################################



@app.errorhandler(500)
def internal_error(error):
	return render_template('employee_site/500.html', error = error), 500


date_format='%m/%d/%Y'
today_date = datetime.date.today()
# Converting date received from mysql to American datetype
def convert_date(raw_date):
	if raw_date == None:
		formatted_date = raw_date
	else:
		formatted_date = datetime.datetime.strptime(str(raw_date), '%Y-%m-%d').strftime(date_format)
	return formatted_date


@app.route('/')
@app.route('/internal/')
@login_required
def internal():
	page = "Dashboard"
	return render_template('employee_site/dashboard.html', page = page)

@socketio.on('create role', namespace='/socketio')
def socketio_admin_createrole(message):
	if current_user.is_authenticated:
		if (Role.query.filter_by(name = message['role'])).count() > 0:
			emit('create role error', {'data': 'Role existed, please choose another one'})
		if not message['role'] or not message['role_description']:
			emit('create role error', {'data': 'Please enter all fields'})
		else:
			user_datastore.create_role(name = message['role'], description = message['role_description'])
			db.session.commit()
			emit('create role success', {'data': 'New role added'})
	else:
		emit('create role error', {'data': 'Current user is not authenticated to perform this action'})

@socketio.on('delete role', namespace='/socketio')
def socketio_admin_deleterole(message):
	if current_user.is_authenticated:
		if (Role.query.filter_by(name = message['role'])).count() > 0:
			role = Role.query.filter_by(name = message['role']).delete()
			db.session.commit()
			emit('delete role success', {'data': 'Role deleted'})
	else:
		emit('delete role error', {'data': 'Current user is not authenticated to perform this action'})


@app.route('/admin/user-base/')
@login_required
@roles_required('admin')
def internal_userbase():
	page = 'User Base'
	return render_template('employee_site/admin/user_base.html', page = page)


@app.route('/admin/user-base/ajax/all-users')
@login_required
def internal_userbase_ajax_allusers():
	all_users = users_schema.dump(User.query.with_entities(User.id, User.email, User.active, User.confirmed_at, User.first_name, User.last_name, User.job_title, User.department, User.address1, User.address2, User.city, User.state, User.birth_date, User.dl_expiration_date, User.driver_license, User.econtact_name, User.econtact_phone, User.econtact_relationship, User.gender, User.phone, User.phone2, User.start_date).all()).data
	return json.dumps(all_users)

@app.route('/admin/user-base/ajax/all-roles')
@login_required
def internal_userbase_ajax_allroles():
	all_roles = roles_schema.dump(Role.query.all()).data
	return json.dumps(all_roles)

@app.route('/admin/user-base/new-user/', methods=["GET", "POST"])
@login_required
@roles_required('admin')
def internal_userbase_newuser():
	page = 'User Base'
	if request.method == "POST":
		first_name = request.form['first_name']
		last_name = request.form['last_name']
		start_date = datetime.datetime.strptime(str(request.form['start_date']), '%m/%d/%Y').strftime('%Y-%m-%d')
		email = request.form['email']
		job_title = request.form['job_title']
		department = request.form['department']
		gender = request.form['gender']
		password = encrypt_password('Welc0me')
		if (User.query.filter_by(email = email)).count() > 0:
			flash('Email existed, please choose another one', 'alert-danger')
			return render_template('employee_site/admin/new_user.html', page = page)
		else:
			user_datastore.create_user(email = email, password = password, first_name = first_name, last_name = last_name, start_date = start_date, job_title = job_title, department = department, gender = gender)
			db.session.commit()
			flash('New account created', 'alert-success')
			return redirect(url_for('internal_userbase'))
		
	else:
		return render_template('employee_site/admin/new_user.html', page = page)

@app.route('/admin/user-base/<path:user_id>/view/', methods=["GET", "POST"])
@login_required
@roles_required('admin')
def internal_userbase_viewuser(user_id):
	page = 'View User'
	if request.method == "POST":
		first_name = request.form['first_name']
		last_name = request.form['last_name']
		start_date = datetime.datetime.strptime(str(request.form['start_date']), '%m/%d/%Y').strftime('%Y-%m-%d')
		# email = request.form['email']
		job_title = request.form['job_title'] 
		department = request.form['department']
		gender = request.form['gender']
		role = Role.query.filter_by(id = request.form['role']).first()
		password = request.form['password']

		if User.query.filter_by(id = user_id).count() == 1:
			user = User.query.filter_by(id = user_id).first()
			if role != None:
				user.roles = []
				user.roles.append(role)
			user.first_name = first_name
			user.last_name = last_name
			user.start_date = start_date
			user.job_title = job_title
			user.department = department
			user.gender = gender
			if password:
				user.password = encrypt_password(password)
			db.session.commit()
			flash('Account updated', 'alert-success')
			return redirect(url_for('internal_userbase'))
			
		else:
			flash('Email existed, please choose another one', 'alert-danger')
			return render_template('employee_site/admin/new_user.html', page = page)
			
	else:
		user = User.query.filter_by(id = user_id).first()
		roles = Role.query.all()
		return render_template('employee_site/admin/view_user.html', page = page, user = user, roles = roles)

@app.route('/knowledge/exam/')
@login_required
def knowledge_exam():
	page = "Exam"
	return render_template('employee_site/knowledge/exam.html', page = page)

@app.route('/knowledge/exam/ajax/all-exams')
@login_required
def knowledge_exam_ajax_allexams():
	available_exams = []
	all_exams = UserExam.query.filter_by(user_id = current_user.id, is_available = "T").all()
	for each in all_exams:
		exam = Exam.query.filter_by(id = each.exam_id).first()
		available_exams.append({"id" : exam.id, "name" : exam.name, "description" : exam.description, "start_date" : convert_date(exam.start_date), "end_date" : convert_date(exam.end_date), "limit_minutes" : exam.limit_minutes})
	return simplejson.dumps(available_exams)

@app.route('/knowledge/exam/ajax/completed-exams')
@login_required
def knowledge_exam_ajax_completedexams():
	completed_exams = []
	all_exams = UserExam.query.filter_by(user_id = current_user.id, is_available = "F").all()
	for each in all_exams:
		exam = Exam.query.filter_by(id = each.exam_id).first()
		completed_exams.append({"id" : exam.id, "name" : exam.name, "description" : exam.description, "start_date" : convert_date(exam.start_date), "end_date" : convert_date(exam.end_date), "limit_minutes" : exam.limit_minutes, "score" : each.score, "taken_date" : convert_date(each.taken_date)})
	return simplejson.dumps(completed_exams)

@app.route('/knowledge/exam/<path:exam_id>/view/', methods=["GET", "POST"])
@login_required
def knowledge_exam_view(exam_id):
	if request.method == "POST":
		results = {}
		score = 0
		user_exam = UserExam.query.filter_by(exam_id = exam_id, user_id = current_user.id).first()
		user_exam.answers = []
		for question in Question.query.filter_by(exam_id = exam_id).all():
			answer_id = request.form[str(question.id)]
			if answer_id != 'None':
				answer = Answer.query.filter_by(id = answer_id).first()
				user_exam.answers.append(answer)
				if answer.is_correct == 'T':
					score += 1
			else:
				answer = 'Unanswered'
			results[question.id] = answer
			
		user_exam.score = score
		user_exam.taken_date = today_date
		user_exam.is_available = "F"
		db.session.commit()
		flash('Test submitted', 'alert-success')
		return redirect(url_for('knowledge_exam'))

	else:
		page = "Exam"
		exam = Exam.query.filter_by(id = exam_id).first()
		all_questions = Question.query.filter_by(exam_id = exam_id).all()
		shuffle(all_questions)
		question_answers = {}
		for question in all_questions:
			answers = {}
			for answer in Answer.query.filter_by(question_id = question.id).all():
				answers[answer.id] = answer.answer
			question_answers[question.id] = answers
		return render_template('employee_site/knowledge/view_exam.html', page = page, exam = exam, all_questions = all_questions, question_answers = question_answers)

@app.route('/knowledge/exam/<path:exam_id>/result/', methods=["GET", "POST"])
@login_required
def knowledge_exam_report(exam_id):
	if request.method == "POST":
		pass

	else:
		page = "Exam Result"
		exam = Exam.query.filter_by(id = exam_id).first()
		return render_template('employee_site/knowledge/view_exam_result.html', page = page, exam = exam)

@app.route('/internal/flow-chart/')
@login_required
def internal_flow_chart():
	page = "Flow Chart"
	return render_template('employee_site/flow-chart.html', page = page)


@app.route('/internal/inventory/invoices/', methods=["GET", "POST"])
@login_required
@roles_accepted('admin', 'management')
def internal_invoices():
	category = 3
	page = "Invoices"
	if request.method == "POST":
		try:
			excel_file = request.get_array(field_name = 'invoice_file')
			#Check for valid Samsung invoice format
			if excel_file[0][0] == 'No' and excel_file[0][1] == 'Billing Doc': 
				invoice_number = excel_file[1][13]
				date_received = datetime.date.today()
				associated_parts = []
				for each_line in excel_file[1:]:
					for _ in range(int(each_line[8])):
						part = {
								'part_number' : each_line[7],
								'part_description' : each_line[16],
								'part_price': (float(each_line[9])/float(each_line[8])),
								'assoc_po' : each_line[18],
								}
						associated_parts.append(part)
				invoice = Invoice(invoice_number, date_received, associated_parts)
				if invoice.check_if_exist() == False:
					invoice.import_invoice_from_excel()
					flash("Imported excel file successfully", 'alert-success')
				else:
					flash("Invoice existed, action denied", 'alert-danger')
			else:
				flash("Invalid file, try again", 'alert-danger')
			return render_template('employee_site/inventory/invoices.html', category = category, page = page)
		except Exception as e:
			flash('Something went wrong, please try again', 'alert-danger')
			return render_template('employee_site/inventory/invoices.html', category = category, page = page)
	else:
		return render_template('employee_site/inventory/invoices.html', category = category, page = page)

@app.route('/internal/inventory/invoices/ajax')
@login_required
def internal_invoices_ajax():
	all_invoices = Invoice.get_all()
	return simplejson.dumps(all_invoices)

@socketio.on('import invoice', namespace='/socketio')
def socketio_invoice_import(message):
	if current_user.is_authenticated:
		import_invoice_data = message['file']
		emit('import invoice success', import_invoice_data)
	else:
		emit('shelf report error', {'data': 'Current user is not authenticated to perform this action'})

@app.route('/internal/inventory/invoices/new/', methods=["GET", "POST"])
@login_required
@roles_accepted('admin', 'management')
def internal_new_invoices():
	category = 3
	page = "New Invoice"
	try:
		if request.method == "POST":
			invoice_number = request.form['invoice_number']
			date_received = request.form['date_received']
			part_numbers = filter( None, request.form.getlist('part_numbers[]') )
			part_numbers = [x.upper() for x in part_numbers]
			assoc_pos = request.form.getlist('assoc_pos[]')
			shelf_locations = request.form.getlist('shelf_locations[]')
			c, conn = connection()
			execute = c.execute("SELECT * FROM invoice WHERE invoice_number = '%s'" % (thwart(invoice_number)) )
			if int(execute) > 0:
				flash("The invoice number has already existed", 'alert-danger')
				return render_template('employee_site/inventory/new_invoice.html', page = page)
			else:
				c.execute("INSERT INTO invoice (invoice_number, date_received) VALUES ( '%s', STR_TO_DATE('%s', '%%m/%%d/%%Y') )" % (thwart(invoice_number), date_received) )
				for x in range(0, len(part_numbers)):
					c.execute("INSERT INTO invoice_detail (invoice_number, part_number, purchase_order_number, shelf_location, status, claimed) VALUES ( '%s', '%s', '%s', '%s', 'New', 0 )" % ( thwart(invoice_number), thwart(part_numbers[x]), thwart(assoc_pos[x]), thwart(shelf_locations[x])) )
					check_duplicate_part = c.execute("SELECT * FROM part_detail WHERE part_number = '%s'" % (thwart(part_numbers[x])) )
					if int(check_duplicate_part) == 0:
						c.execute("INSERT INTO part_detail (part_number) VALUES ('%s')" % ( thwart(part_numbers[x])) )
				
				conn.commit()
				flash('Invoice created successfully', 'alert-success')
				c.close()
				conn.close()
				gc.collect()
			return redirect(url_for('internal_invoices'))
		else:	
			return render_template('employee_site/inventory/new_invoice.html', category = category, page = page)
	except Exception as e:
		return render_template('employee_site/500.html', error = e)

@app.route('/internal/inventory/invoices/<invoice_number>/view/', methods=["GET", "POST"])
@login_required
def internal_invoices_view(invoice_number):
	category = 3
	page = "View Invoice"
	# Legacy code, should be updated to OO style
	try:
		if request.method == "POST":
			post_invoice_number = request.form['post_invoice_number']
			date_received = request.form['date_received']
			invoice_detail_id = request.form.getlist('invoice_detail_id[]')
			part_numbers = filter( None, request.form.getlist('part_numbers[]') )
			part_numbers = [x.upper() for x in part_numbers]
			part_descriptions = request.form.getlist('part_descriptions[]')
			part_prices = request.form.getlist('part_prices[]')
			assoc_pos = request.form.getlist('assoc_pos[]')
			locations = request.form.getlist('locations[]')
			statuses = request.form.getlist('statuses[]')
			c, conn = connection()
			execute = c.execute("SELECT * FROM invoice WHERE invoice_number = '%s'" % (thwart(invoice_number)) )
			if int(execute) == 0:
				flash('The invoice number does not exist', 'alert-danger')
			elif int(execute) == 1:
				c.execute("UPDATE invoice SET date_received = STR_TO_DATE('%s', '%%m/%%d/%%Y') WHERE invoice_number = '%s'" % ( date_received, thwart(invoice_number) ) )
				for x in range(0, len(part_numbers)):
					# flash(assoc_pos[x])
					if statuses[x] == "Remove":
						c.execute("DELETE FROM invoice_detail WHERE invoice_detail_id= '%s'" % ( invoice_detail_id[x] ) )
					elif invoice_detail_id[x] == 'add':
						c.execute("INSERT INTO invoice_detail (invoice_number, part_number, purchase_order_number, shelf_location, status, claimed) VALUES ( '%s', '%s', '%s', '%s', 'New', 0 )" % ( thwart(post_invoice_number), thwart(part_numbers[x]), thwart(assoc_pos[x]), thwart(locations[x])) )
						check_duplicate_part = c.execute("SELECT * FROM part_detail WHERE part_number = '%s'" % (thwart(part_numbers[x])) )
						if int(check_duplicate_part) == 0:
							c.execute("INSERT INTO part_detail (part_number) VALUES  ('%s')" % ( thwart(part_numbers[x])) )
					elif statuses[x] == 'In Stock - Claimed' or statuses[x] == 'Used - Claimed':
						c.execute("UPDATE invoice_detail SET part_number = '%s', purchase_order_number = '%s', shelf_location = '%s', status = '%s', claimed = 1, claimed_date = '%s' WHERE invoice_detail_id = '%s'" % ( thwart(part_numbers[x]), thwart(assoc_pos[x]), thwart(locations[x]), thwart(statuses[x]), today_date, invoice_detail_id[x] ) )
					else:	
						c.execute("UPDATE invoice_detail SET part_number = '%s', purchase_order_number = '%s', shelf_location = '%s', status = '%s' WHERE invoice_detail_id = '%s'" % ( thwart(part_numbers[x]), thwart(assoc_pos[x]), thwart(locations[x]), thwart(statuses[x]), invoice_detail_id[x] ) )
						check_duplicate_part = c.execute("SELECT * FROM part_detail WHERE part_number = '%s'" % (thwart(part_numbers[x])) )
						if int(check_duplicate_part) == 0:
							c.execute("INSERT INTO part_detail (part_number) VALUES ('%s')" % ( thwart(part_numbers[x])) )
				conn.commit()
				socketio.emit('my response',
                      {'data': 'Server generated event'},
                      namespace='/test/socketio')
				flash("Change(s) saved", 'alert-success')
				c.close()
				conn.close()
				gc.collect()
			return redirect(url_for('internal_invoices'))
		else:	
			c, conn = connection()
			c.execute("SELECT * FROM invoice WHERE invoice_number = '%s'" % (thwart(invoice_number)) )
			invoice_data = c.fetchone()
			c.execute("SELECT * FROM invoice_detail WHERE invoice_number = '%s'" % (thwart(invoice_number)) )
			invoice_detail_data = c.fetchall()
			c.close()
			conn.close()
			gc.collect()
			date_received = convert_date(invoice_data[1])
			return render_template('employee_site/inventory/view_invoice.html', category = category, page = page, invoice_data = invoice_data, invoice_detail_data = invoice_detail_data, date_received = date_received)
	except Exception as e:
		return render_template('employee_site/500.html', error = e)

@app.route('/internal/inventory/stock-inventory/', methods=["GET", "POST"])
@login_required
@roles_accepted('admin', 'management')
def internal_stock_inventory():
	category = 3
	page = "Stock Inventory"
	return render_template('employee_site/inventory/stock_inventory.html', category = category, page = page)

@app.route('/internal/inventory/stock-inventory/ajax')
@login_required
def internal_stock_inventory_ajax():
	stock_parts = Part.get_stock_inventory()
	return simplejson.dumps(stock_parts)

@app.route('/internal/inventory/stock-inventory/settings/', methods=["GET", "POST"])
@login_required
@roles_accepted('admin', 'management')
def stock_inventory_settings():
	category = 3
	page = "Stock Inventory Settings"
	if request.method == 'POST':
		return jsonify({"result": request.get_array(field_name='file')})
	return render_template('employee_site/inventory/stock_inventory_settings.html', category = category, page = page)

@app.route('/internal/inventory/stock-inventory/<path:part_number>/view/', methods=["GET", "POST"])
@login_required
@roles_accepted('admin', 'management')
def internal_part_detail(part_number):
	category = 3
	page = "Part Detail"
	try:
		if request.method == "POST":
			pass
		else:
			part_detail_data = Part.get_by_part_number(part_number)
			stock_quantity = Part.get_stock_quantity_for_part(part_number)
			return render_template('employee_site/inventory/part_detail.html', category = category, page = page, stock_quantity = stock_quantity, part_detail_data = part_detail_data)
	except Exception as e:
		return render_template('employee_site/500.html', error = e)

@app.route('/internal/inventory/stock-inventory/<path:part_number>/view/ajax/stock-status', methods=["GET", "POST"])
@login_required
def internal_part_detail_ajax(part_number):
	category = 3
	page = "Part Detail"
	
	if request.method == "POST":
		pass
	else:
		invoice_detail_data = Part.get_invoice_detail(part_number)
		return simplejson.dumps(invoice_detail_data)

@app.route('/internal/inventory/stock-inventory/<path:part_number>/edit/', methods=["GET", "POST"])
@login_required
@roles_accepted('admin', 'management')
def internal_part_edit(part_number):
	category = 3
	page = "Part Edit"
	try:
		if request.method == "POST":
			part_description = request.form['part_description']
			machine_type = request.form['machine_type']
			part_price = request.form['part_price']
			image_url = request.form['image_url']
			part = Part(part_number, part_description, machine_type, part_price, image_url)
			if part.update() == True:
				flash("Updated part detail successfully", 'alert-success')
			return redirect(url_for('internal_stock_inventory'))
		else:
			part_detail_data = Part.get_by_part_number(part_number)
			return render_template('employee_site/inventory/part_edit.html', category = category, page = page, part_number = part_number, part_detail_data = part_detail_data)
	except Exception as e:
		return render_template('employee_site/500.html', error = e)

@app.route('/internal/inventory/report/')
@login_required
@roles_accepted('admin', 'management')
def internal_inventory_report():
	category = 3
	page = "Inventory Report"
	try:
		return render_template('employee_site/inventory/report.html', category = category, page = page)
	except Exception as e:
		return render_template('employee_site/500.html', error = e)

@app.route('/internal/inventory/report/ajax/top-50-part')
@login_required
def internal_inventory_ajax_top50part():
	try:
		c, conn = connection()
		c.execute("SELECT P.*,  (SELECT COUNT(*) FROM invoice_detail AS I WHERE I.part_number = P.part_number  AND I.status IN ('NEW', 'In Stock - Claimed')) AS total_quantity, (SELECT COUNT(*) FROM invoice_detail AS I WHERE I.part_number = P.part_number  AND I.status IN ('NEW', 'In Stock - Claimed') AND I.shelf_location IS NOT NULL AND I.shelf_location NOT IN ('N/A', 'n/a', '')) AS stock_quantity, (SELECT COUNT(*) FROM invoice_detail AS I WHERE I.part_number = P.part_number  AND I.status IN ('NEW') AND I.shelf_location IS NOT NULL AND I.shelf_location NOT IN ('N/A', 'n/a', '')) AS claimable_amount, (SELECT COUNT(*) FROM invoice_detail AS I WHERE I.part_number = P.part_number ) AS total_bought FROM part_detail AS P ORDER BY total_bought DESC LIMIT 50")
		data = c.fetchall()
		c.close()
		conn.close()
		gc.collect()
		return simplejson.dumps(data)

	except Exception as e:
		return render_template('employee_site/500.html', error = e)

@app.route('/internal/inventory/report/ajax/statistics')
@login_required
def internal_inventory_ajax_statistics():
	try:
		c, conn = connection()
		c.execute("SELECT * FROM part_detail")
		part_detail_data = []
		for p in c:
			c.execute("SELECT P.part_number, P.part_description, P.machine_type, P.part_price, (SELECT COUNT(*) FROM invoice_detail AS I WHERE I.part_number = P.part_number AND I.status IN ('NEW', 'In Stock - Claimed')) AS total_quantity, (SELECT COUNT(*) FROM invoice_detail AS I WHERE I.part_number = P.part_number AND I.status IN ('NEW', 'In Stock - Claimed') AND I.shelf_location IS NOT NULL AND I.shelf_location NOT IN ('N/A', 'n/a', '')) AS stock_quantity, (SELECT COUNT(*) FROM invoice_detail AS I WHERE I.part_number = P.part_number AND I.status IN ('NEW') AND I.shelf_location IS NOT NULL AND I.shelf_location NOT IN ('N/A', 'n/a', '')) AS claimable_amount FROM part_detail AS P WHERE part_number = '%s'" % ( thwart(p[0]) ))
			part = c.fetchone()
			if part[3] != None and part[5] != None:
				stock_value = part[3] * part[5]
			else:
				stock_value = 0
			if part[3] != None and part[6] != None:
				unclaimed_value = part[3] * part[6]
			else:
				unclaimed_value = 0
			part_detail_data.append([part[0], part[1], part[2], part[3], part[4], part[5], part[6], stock_value, unclaimed_value])
		c.close()
		conn.close()
		gc.collect()
		return simplejson.dumps(part_detail_data)

	except Exception as e:
		return render_template('employee_site/500.html', error = e)

@app.route('/internal/inventory/report/shelf/', methods=["GET", "POST"])
@login_required
@roles_accepted('admin', 'management')
def inventory_shelf_report():
	category = 3
	page = "Shelf Report"
	all_shelves = ['A0', 'A1', 'A2', 'A2-1', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'B0', 'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'C1', 'C2', 'C3', 'C4', 'D0']
	if request.method == "POST":
		shelf = request.form['shelf']
		shelf_report_data = Part.get_shelf_report(shelf)
		flash(shelf_report_data, 'alert-success')
		return render_template('employee_site/inventory/shelf_report.html', category = category, page = page, all_shelves = all_shelves)
	else:
		
		return render_template('employee_site/inventory/shelf_report.html', category = category, page = page, all_shelves = all_shelves)

@app.route('/internal/inventory/report/shelf/ajax', methods=["GET", "POST"])
@login_required
@roles_accepted('admin', 'management')
def inventory_shelf_report_ajax():
	category = 3
	page = "Shelf Report"
	all_shelves = ['A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'B0', 'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'C1', 'C2', 'C3', 'C4', 'D0']
	shelf_report_data = simplejson.dumps(Part.get_shelf_report('A0'))

	return shelf_report_data

@socketio.on('shelf report', namespace='/socketio')
def socketio_inv_shelf_report(message):
	if current_user.is_authenticated:
		shelf_report_data = simplejson.dumps(Part.get_shelf_report(message['shelf']))
		emit("shelf report data", shelf_report_data)
	else:
		emit('shelf report error', {'data': 'Current user is not authenticated to perform this action'})


@app.route('/internal/frontpage/cms')
@login_required
@roles_accepted('admin', 'management')
def internal_frontpage_cms():
	page = "CMS"
	try:
		return render_template('employee_site/front-page/code-editor.html', page = page)
	except Exception as e:
		return render_template('employee_site/500.html', error = e)	

@app.route('/internal/frontpage/code-editor')
@login_required
@roles_accepted('admin', 'management')
def internal_frontpage_editor():
	page = "Code Editor"
	try:
		return render_template('employee_site/front-page/code-editor.html', page = page)
	except Exception as e:
		return render_template('employee_site/500.html', error = e)	

###############################
###############################TEST SECTION
###############################
        


@app.route('/test/')
@login_required
def internal_test():
    return render_template('employee_site/main_template.html')


@app.route('/test/ajax')
@login_required
def test_ajax():
	category = 3
	page = "Stock Inventory"
	try:
		socketio.emit('my response',
                      {'data': 'Server generated event'},
                      namespace='/test/socketio')
		return 'test socketio'

	except Exception as e:
		return render_template('employee_site/500.html', error = e)

if __name__ == '__main__':
	socketio.run(app, host = '0.0.0.0', debug = True)