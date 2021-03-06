#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Hello fellow developer, this project is coded using Flask framework, for more
info visit http://flask.pocoo.org/
Languages used: Python (Flask), Javascript (jQuery)
If you see this comment, I'm probably no longer working for HNG Appliances.
My code is definitely not pretty as this is only my second project since I
graduated from school. It was a result of my limited knowledge, google and
stack overflow. I will make sure the source code is well commented.
"""

import simplejson
import json
import datetime
import os
import flask_excel as excel # noqa
from random import shuffle
from flask import (
    Flask, render_template, redirect, url_for,
    flash, jsonify, request,
)
from models import (
    db, Invoice, Part, InvoiceDetail, Role, User,
    Exam, Question, Answer, UserExam, Client, Article,
)
from serializers import (
    users_schema, roles_schema, clients_schema, articles_schema,
    invoices_schema, parts_schema, part_schema, invoices_detail_schema
)
from flask_socketio import SocketIO, emit
from flask_security import (
    Security, SQLAlchemyUserDatastore,
    login_required, roles_required, roles_accepted, current_user
)
from flask_security.utils import encrypt_password
from flask_mail import Mail, Message
from utils import sql_to_us_date, us_to_sql_date

# App config
app = Flask(__name__)
app.jinja_env.globals.update(sql_to_us_date=sql_to_us_date)
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
app.config['TRAP_BAD_REQUEST_ERRORS'] = True

# Mysql config 'mysql+pymysql://root@localhost/my_hng
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# Flask-security config
# app.config['SECURITY_REGISTERABLE'] = True
app.config['SECURITY_RECOVERABLE'] = True
# app.config['SECURITY_CONFIRMABLE'] = True
app.config['SECURITY_CHANGEABLE'] = True
app.config['SECURITY_PASSWORD_HASH'] = 'pbkdf2_sha512'
app.config['SECURITY_PASSWORD_SALT'] = os.environ['SALT']
app.config['SECURITY_TOKEN_MAX_AGE'] = 10
app.config['SECURITY_POST_LOGIN_VIEW'] = '/'
app.config['SECURITY_POST_LOGOUT_VIEW'] = '/login'

# Email config
app.config['SECURITY_EMAIL_SENDER'] = 'no-reply@hngappliances.com'
app.config['DEFAULT_MAIL_SENDER'] = 'no-reply@hngappliances.com'
app.config['MAIL_SERVER'] = 'mail.hngappliances.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'no-reply@hngappliances.com'
app.config['MAIL_PASSWORD'] = os.environ['EMAIL_PASSWORD']
app.config['MAIL_DEFAULT_SENDER'] = 'no-reply@hngappliances.com'
app.config['MAIL_MAX_EMAILS'] = 30


mail = Mail(app)  # Flask-Mail init
db.init_app(app)  # Flask-SQLAlchemy init
socketio = SocketIO(app)  # Flask-Socketio init
# Flask-Security init
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)


@app.errorhandler(500)
def internal_error(error):
    return render_template('employee_site/500.html', error=error), 500


@app.route('/')
@login_required
def dashboard():
    page = "Dashboard"
    return render_template('employee_site/dashboard.html', page=page)


@socketio.on('create role', namespace='/socketio')
def socketio_admin_createrole(message):
    if current_user.is_authenticated:
        if (Role.query.filter_by(name=message['role'])).count() > 0:
            emit(
                'create role error',
                {'data': 'Role existed, please choose another one'}
            )
        if not message['role'] or not message['role_description']:
            emit('create role error', {'data': 'Please enter all fields'})
        else:
            user_datastore.create_role(
                name=message['role'],
                description=message['role_description']
            )
            db.session.commit()
            emit('create role success', {'data': 'New role added'})
    else:
        emit(
            'create role error',
            {'data': 'Current user is not authenticated'}
        )


@socketio.on('delete role', namespace='/socketio')
def socketio_admin_deleterole(message):
    if current_user.is_authenticated:
        if (Role.query.filter_by(name=message['role'])).count() > 0:
            Role.query.filter_by(name=message['role']).delete()
            db.session.commit()
            emit('delete role success', {'data': 'Role deleted'})
    else:
        emit(
            'delete role error',
            {'data': 'Current user is not authenticated'}
        )


@app.route('/admin/user-base/')
@login_required
@roles_required('admin')
def internal_userbase():
    page = 'User Base'
    return render_template('employee_site/admin/user_base.html', page=page)


@app.route('/admin/user-base/ajax/all-users')
@login_required
def internal_userbase_ajax_allusers():
    all_users = users_schema.dump(User.query.with_entities(
        User.id,
        User.email,
        User.active,
        User.confirmed_at,
        User.first_name,
        User.last_name,
        User.job_title,
        User.department,
        User.address1,
        User.address2,
        User.city,
        User.state,
        User.birth_date,
        User.dl_expiration_date,
        User.driver_license,
        User.econtact_name,
        User.econtact_phone,
        User.econtact_relationship,
        User.gender,
        User.phone,
        User.phone2,
        User.start_date
    ).all()).data
    return jsonify(all_users)


@app.route('/admin/user-base/ajax/all-roles')
@login_required
def internal_userbase_ajax_allroles():
    all_roles = roles_schema.dump(Role.query.all()).data
    return jsonify(all_roles)


@app.route('/admin/user-base/new-user/', methods=["GET", "POST"])
@login_required
@roles_required('admin')
def internal_userbase_newuser():
    page = 'User Base'
    if request.method == "POST":
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        start_date = datetime.datetime.strptime(
            str(request.form['start_date']),
            '%m/%d/%Y'
        ).strftime('%Y-%m-%d')
        email = request.form['email']
        job_title = request.form['job_title']
        department = request.form['department']
        gender = request.form['gender']
        password = encrypt_password('Welc0me')
        if (User.query.filter_by(email=email)).count() > 0:
            flash('Email existed, please choose another one', 'alert-danger')
            return render_template(
                'employee_site/admin/new_user.html',
                page=page
            )
        else:
            user_datastore.create_user(
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                start_date=start_date,
                job_title=job_title,
                department=department,
                gender=gender
            )
            db.session.commit()
            flash('New account created', 'alert-success')
            return redirect(url_for('internal_userbase'))

    else:
        return render_template('employee_site/admin/new_user.html', page=page)


@app.route('/admin/user-base/<path:user_id>/view/', methods=["GET", "POST"])
@login_required
@roles_required('admin')
def internal_userbase_viewuser(user_id):
    page = 'View User'
    if request.method == "POST":
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        start_date = datetime.datetime.strptime(
            str(request.form['start_date']),
            '%m/%d/%Y'
        ).strftime('%Y-%m-%d')
        # email = request.form['email']
        job_title = request.form['job_title']
        department = request.form['department']
        gender = request.form['gender']
        role = Role.query.filter_by(id=request.form['role']).first()
        password = request.form['password']

        if User.query.filter_by(id=user_id).count() == 1:
            user = User.query.filter_by(id=user_id).first()
            if role is not None:
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
            return render_template(
                'employee_site/admin/new_user.html',
                page=page
            )
    else:
        user = User.query.filter_by(id=user_id).first()
        roles = Role.query.all()
        return render_template(
            'employee_site/admin/view_user.html',
            page=page,
            user=user,
            roles=roles
        )


@app.route('/client/client-list/', methods=["GET", "POST"])
@login_required
@roles_required('admin')
def client_list():
    page = 'Client List'
    if request.method == "POST":
        try:
            excel_file = request.get_array(field_name='client_list_file')
            # Check for valid SF client list excel file
            # NOTE: This feature is dependent on Service Fusion customer report
            # If they change their excel format, the source code has to be
            # modified to accomodate.
            if (excel_file[5][5] == 'Primary Contact First Name' and
                excel_file[5][6] == 'Primary Contact Last Name' and
                excel_file[5][7] == 'Primary Contact Phone 1' and
                excel_file[5][14] == 'Primary Service Location Address 1' and
                excel_file[5][15] == 'Primary Service Location Address 2' and
                excel_file[5][16] == 'Primary Service Location City' and
                    excel_file[5][27] == 'Date Created'):
                for each_line in excel_file[6:]:
                    email = str(each_line[8]).strip()
                    first_name = str(each_line[5]).strip()
                    last_name = str(each_line[6]).strip()
                    phone = filter(str.isdigit, str(each_line[7]).strip())
                    address1 = str(each_line[15]).strip()
                    address2 = str(each_line[14]).strip()
                    city = str(each_line[16]).strip()
                    state = str(each_line[17]).strip()
                    zip_code = str(each_line[18]).strip()
                    added_date = str(each_line[27]).strip()
                    is_subscribed = "T"
                    client_id = (first_name + last_name + zip_code).lower()

                    if Client.query.filter(
                        Client.first_name == first_name,
                        Client.last_name == last_name
                    ).count() == 1:
                        client = Client.query.filter_by(id=client_id).first()
                        client.email = email
                        client.first_name = first_name
                        client.last_name = last_name
                        client.added_date = added_date
                        client.phone = phone
                        client.address1 = address1
                        client.address2 = address2
                        client.city = city
                        client.state = state
                        client.zip_code = zip_code

                    elif Client.query.filter_by(id=client_id).count() == 0:
                        client = Client(
                            id=client_id,
                            email=email,
                            first_name=first_name,
                            last_name=last_name,
                            added_date=added_date,
                            phone=phone,
                            address1=address1,
                            address2=address2,
                            city=city,
                            state=state,
                            zip_code=zip_code,
                            is_subscribed=is_subscribed
                        )
                        db.session.add(client)
                    db.session.commit()
                flash("Synced successfully", "alert-success")
            else:
                flash("Invalid file, try again", 'alert-danger')
            return render_template(
                'employee_site/client/client_list.html',
                page=page
            )
        except Exception as e:
            flash(e, 'alert-danger')
            return render_template(
                'employee_site/client/client_list.html',
                page=page
            )
    else:
        return render_template(
            'employee_site/client/client_list.html',
            page=page
        )


@app.route('/client/client-list/ajax/all-clients')
def client_list_ajax_allclients():
    all_clients = clients_schema.dump(Client.query.all()).data
    return json.dumps(all_clients)


@app.route('/client/newsletter/', methods=["GET", "POST"])
@login_required
@roles_required('admin')
def client_newsletter():
    page = 'Newsletter'
    if request.method == "POST":
        send_mode = request.json['mode']
        if send_mode == 'test':
            test_email = request.json['testEmail']
            subject = request.json['subject']
            newsletter_html = request.json['newsletterBody']
            unsubscription_html = """
                <p style="text-align: center; "><font color="#9c9c94">
                <a href="http://myhng.net/client/email-setting/{}">
                Change your email setting</a></font></p>
                """.format(test_email)
            msg = Message(
                sender=("HNG Appliances", "no-reply@hngappliances.com"),
                recipients=[test_email],
                html=newsletter_html + unsubscription_html,
                subject=subject)
            mail.send(msg)
            return jsonify(**request.json)

        elif send_mode == 'normal':
            subject = request.json['subject']
            newsletter_html = request.json['newsletterBody']
            with mail.connect() as conn:
                clients = Client.query.filter(
                    Client.email != '',
                    Client.is_subscribed == "T").group_by(Client.email).all()
                for client in clients:
                    unsubscription_html = """
                        <p style="text-align: center; "><font color="#9c9c94">
                        <a href="http://myhng.net/client/email-setting/%s">
                        Change your email setting</a></font></p>
                        """ % (client.email)
                    msg = Message(
                        sender=(
                            'HNG Appliances',
                            'no-reply@hngappliances.com'
                        ),
                        recipients=[client.email],
                        html=newsletter_html + unsubscription_html,
                        subject=subject)
                    conn.send(msg)
            return jsonify(**request.json)
    else:
        return render_template(
            'employee_site/client/newsletter.html',
            page=page
        )


@app.route('/client/email-setting/<path:client_email>/', methods=['GET', 'POST'])
def client_email_setting(client_email):
    page = 'Email Setting'
    if request.method == "POST":
        client_email = request.json['clientEmail']
        if Client.query.filter(
            Client.email == client_email,
            Client.is_subscribed == "T"
        ).count() >= 1:
            clients = Client.query.filter(
                Client.email == client_email,
                Client.is_subscribed == "T"
            ).all()
            for client in clients:
                client.is_subscribed = "F"
                # db.session.add(client)
            db.session.commit()

            return jsonify({
                'status': 'found',
            })

        else:
            return jsonify({
                'status': 'not found',
            })
    else:
        return render_template(
            'employee_site/client/email_setting.html',
            page=page,
            client_email=client_email
        )


@app.route('/knowledge/exam/')
@login_required
def knowledge_exam():
    page = "Exam"
    return render_template('employee_site/knowledge/exam.html', page=page)


@app.route('/knowledge/exam/ajax/all-exams')
@login_required
def knowledge_exam_ajax_allexams():
    available_exams = []
    all_exams = UserExam.query.filter_by(
        user_id=current_user.id,
        is_available="T"
    ).all()
    for each in all_exams:
        exam = Exam.query.filter_by(id=each.exam_id).first()
        available_exams.append({
            "id": exam.id,
            "name": exam.name,
            "description": exam.description,
            "start_date": sql_to_us_date(exam.start_date),
            "end_date": sql_to_us_date(exam.end_date),
            "limit_minutes": exam.limit_minutes
        })
    return simplejson.dumps(available_exams)


@app.route('/knowledge/exam/ajax/completed-exams')
@login_required
def knowledge_exam_ajax_completedexams():
    completed_exams = []
    all_exams = UserExam.query.filter_by(
        user_id=current_user.id,
        is_available="F"
    ).all()
    for each in all_exams:
        exam = Exam.query.filter_by(id=each.exam_id).first()
        completed_exams.append({
            "id": exam.id,
            "name": exam.name,
            "description": exam.description,
            "start_date": sql_to_us_date(exam.start_date),
            "end_date": sql_to_us_date(exam.end_date),
            "limit_minutes": exam.limit_minutes,
            "score": each.score,
            "taken_date": sql_to_us_date(each.taken_date)
        })
    return simplejson.dumps(completed_exams)


@app.route('/knowledge/exam/<path:exam_id>/view/', methods=["GET", "POST"])
@login_required
def knowledge_exam_view(exam_id):
    if request.method == "POST":
        results = {}
        score = 0
        user_exam = UserExam.query.filter_by(
            exam_id=exam_id,
            user_id=current_user.id
        ).first()
        user_exam.answers = []
        for question in Question.query.filter_by(exam_id=exam_id).all():
            answer_id = request.form[str(question.id)]
            if answer_id != 'None':
                answer = Answer.query.filter_by(id=answer_id).first()
                user_exam.answers.append(answer)
                if answer.is_correct == 'T':
                    score += 1
            else:
                answer = 'Unanswered'
            results[question.id] = answer

        user_exam.score = score
        user_exam.taken_date = datetime.date.today()
        user_exam.is_available = "F"
        db.session.commit()
        flash('Test submitted', 'alert-success')
        return redirect(url_for('knowledge_exam'))
    else:
        page = "Exam"
        exam = Exam.query.filter_by(id=exam_id).first()
        all_questions = Question.query.filter_by(exam_id=exam_id).all()
        shuffle(all_questions)
        question_answers = {}
        for question in all_questions:
            answers = {}
            for a in Answer.query.filter_by(question_id=question.id).all():
                answers[a.id] = a.answer
            question_answers[question.id] = answers
        return render_template(
            'employee_site/knowledge/view_exam.html',
            page=page,
            exam=exam,
            all_questions=all_questions,
            question_answers=question_answers
        )


@app.route('/knowledge/exam/<path:exam_id>/result/', methods=["GET", "POST"])
@login_required
def knowledge_exam_report(exam_id):
    if request.method == "POST":
        pass

    else:
        page = "Exam Result"
        exam = Exam.query.filter_by(id=exam_id).first()
        return render_template(
            'employee_site/knowledge/view_exam_result.html',
            page=page,
            exam=exam
         )


@app.route('/flow-chart/')
@login_required
def flow_chart():
    page = "Flow Chart"
    return render_template('employee_site/flow-chart.html', page=page)


@app.route('/front-page/cms/')
@login_required
def frontpage_cms():
    page = 'CMS'
    return render_template('employee_site/front-page/cms.html', page=page)


@app.route('/front-page/cms/ajax/allarticles')
def frontpage_cms_ajax_allarticles():
    all_articles = articles_schema.dump(
        Article.query.filter(Article.status != 'Trashed').all()
    ).data
    return json.dumps(all_articles)


@app.route('/front-page/cms/new/', methods=["GET", "POST"])
@login_required
def frontpage_cms_new():
    page = 'CMS'
    if request.method == "POST":
        title = request.json['articleTitle']
        category = request.json['articleCategory']
        summary = request.json['articleSummary']
        content = request.json['articleContent']
        status = request.json['articleStatus']
        if status == 'Published':
            published_date = datetime.date.today()
            added_date = datetime.date.today()
        elif status == 'Draft':
            published_date = None
            added_date = datetime.date.today()
        article = Article(
            title=title,
            content=content,
            author_id=current_user.id,
            category=category,
            published_date=published_date,
            added_date=added_date,
            summary=summary,
            status=status
        )
        db.session.add(article)
        db.session.commit()
        return jsonify(**request.json)
    else:
        return render_template(
            'employee_site/front-page/new_article.html',
            page=page
        )


@app.route('/front-page/cms/<path:article_id>/edit/', methods=["GET", "POST"])
@login_required
def frontpage_cms_edit(article_id):
    page = 'CMS'
    if request.method == "POST":
        title = request.json['articleTitle']
        category = request.json['articleCategory']
        status = request.json['articleStatus']
        summary = request.json['articleSummary']
        content = request.json['articleContent']
        article = Article.query.filter_by(id=article_id).first()
        article.title = title
        article.category = category
        article.status = status
        article.summary = summary
        article.content = content
        if status == 'Published':
            article.published_date = datetime.date.today()
        db.session.commit()
        return jsonify(**request.json)
    else:
        article = Article.query.filter_by(id=article_id).first()
        return render_template(
            'employee_site/front-page/edit_article.html',
            page=page,
            article=article
        )


@app.route('/inventory/invoices/')
@login_required
@roles_accepted('admin', 'management')
def invoices():
    category = 3
    page = "Invoices"
    return render_template(
        'employee_site/inventory/invoices.html',
        category=category,
        page=page
    )


@app.route('/inventory/invoices/', methods=['POST'])
@login_required
@roles_accepted('admin', 'management')
def new_invoice_excel():
    excel_file = request.get_dict(field_name='invoice_file')
    samsung_keys = (
        'Shipped Parts', 'Qty', 'Amount', 'Delivery No',
        'P/O No', 'Description', 'Tracking No',
    )
    # Check for valid Samsung invoice format
    if all(k in excel_file for k in samsung_keys):
        invoice_number = excel_file['Delivery No'][0]
        if Invoice.query.get(invoice_number):
            flash('This invoice already exists', 'alert-danger')
            return redirect(url_for('invoices'))
        invoice = Invoice(invoice_number=invoice_number)
        for idx, part_number in enumerate(excel_file['Shipped Parts']):
            qty = int(excel_file['Qty'][idx])
            purchase_order_number = excel_file['P/O No'][idx]
            description = excel_file['Description'][idx].strip()
            price = float(excel_file['Amount'][idx]) / qty
            part = Part.get_or_create(part_number, db.session)
            part.description = description
            part.price = price
            for _ in range(qty):
                invoice_detail = InvoiceDetail(
                    invoice_number=invoice_number,
                    purchase_order_number=purchase_order_number,
                )
                invoice_detail.part = part
                invoice.parts.append(invoice_detail)
        db.session.add(invoice)
        db.session.commit()
        flash('Imported excel file successfully', 'alert-success')
    else:
        flash('Invalid file, try again', 'alert-danger')
    return redirect(url_for('invoices'))


@app.route('/inventory/invoices/ajax')
@login_required
def invoices_ajax():
    response = {}
    response['draw'] = int(request.args.get('draw', 0))
    per_page = int(request.args.get('length', 30))
    try:
        page = int(request.args['start']) / int(request.args['length']) + 1
    except:
        page = 1
    search = u'{}{}{}'.format('%', request.args.get('search[value]', ''), '%')
    response['recordsTotal'] = Invoice.query.count()
    if len(search) > 3:
        pagination_obj = Invoice.query.filter(
            (Invoice.invoice_number.like(search)) |
            (Invoice.received_date.like(search))
        ).order_by(
            Invoice.received_date.desc(), Invoice.invoice_number.desc()
        ).paginate(page=page, per_page=per_page)
    else:
        pagination_obj = Invoice.query.order_by(
            Invoice.received_date.desc(), Invoice.invoice_number.desc()
        ).paginate(page=page, per_page=per_page)
    response['invoices'] = invoices_schema.dump(pagination_obj.items).data
    response['recordsFiltered'] = pagination_obj.total
    return jsonify(response)


@socketio.on('import invoice', namespace='/socketio')
def socketio_invoice_import(message):
    if current_user.is_authenticated:
        import_invoice_data = message['file']
        emit('import invoice success', import_invoice_data)
    else:
        emit(
            'shelf report error',
            {'data': 'Current user is not authenticated'}
        )


@app.route('/inventory/invoices/new/')
@login_required
@roles_accepted('admin', 'management')
def new_invoice():
    category = 3
    page = "New Invoice"
    return render_template(
        'employee_site/inventory/new_invoice.html',
        category=category,
        page=page
    )


@app.route('/inventory/invoices/new/', methods=['POST'])
@login_required
@roles_accepted('admin', 'management')
def new_invoice_post():
    invoice_number = request.form['invoice_number']
    received_date = us_to_sql_date(request.form['date_received']),
    part_numbers = filter(None, request.form.getlist('part_numbers[]'))
    part_numbers = [x.upper() for x in part_numbers]
    assoc_pos = request.form.getlist('assoc_pos[]')
    shelf_locations = request.form.getlist('shelf_locations[]')
    if Invoice.query.get(invoice_number):
        flash("The invoice number has already existed", 'alert-danger')
        return redirect(url_for('new_invoice'))
    invoice = Invoice(
        invoice_number=invoice_number,
        received_date=received_date
    )
    for idx, x in enumerate(part_numbers):
        invoice_detail = InvoiceDetail(
            purchase_order_number=assoc_pos[idx],
            shelf_location=shelf_locations[idx],
        )
        part = Part.get_or_create(x, db.session)
        invoice_detail.part = part
        invoice.parts.append(invoice_detail)
    db.session.add(invoice)
    db.session.commit()
    flash('Invoice created successfully', 'alert-success')
    return redirect(url_for('invoices'))


@app.route('/inventory/invoices/<invoice_number>/',)
@login_required
def view_invoice(invoice_number):
    category = 3
    page = "View Invoice"
    invoice = Invoice.query.get_or_404(invoice_number)
    return render_template(
        'employee_site/inventory/view_invoice.html',
        category=category,
        page=page,
        invoice=invoice,
    )


@app.route('/inventory/invoices/<invoice_number>/', methods=['POST'])
@login_required
def update_invoice(invoice_number):
    invoice = Invoice.query.get(invoice_number)
    if not invoice:
        flash('The invoice number does not exist', 'alert-danger')
        return redirect(url_for('invoices'))
    received_date = us_to_sql_date(request.form['date_received'])
    invoice_detail_id = request.form.getlist('invoice_detail_id[]')
    part_numbers = filter(None, request.form.getlist('part_numbers[]'))
    part_numbers = [x.upper() for x in part_numbers]
    assoc_pos = request.form.getlist('assoc_pos[]')
    shelf_locations = request.form.getlist('locations[]')
    statuses = request.form.getlist('statuses[]')
    invoice.received_date = received_date
    for idx, x in enumerate(part_numbers):
        invoice_detail = InvoiceDetail.query.get(invoice_detail_id[idx])
        part = Part.get_or_create(x, db.session)
        if not invoice_detail:
            invoice_detail = InvoiceDetail(
                purchase_order_number=assoc_pos[idx],
                shelf_location=shelf_locations[idx],
            )
            invoice_detail.part = part
            invoice_detail.purchase_order_number = assoc_pos[idx]
            invoice_detail.status = statuses[idx]
            invoice_detail.shelf_location = shelf_locations[idx]
            invoice.parts.append(invoice_detail)
        else:
            if statuses[idx] == 'Remove':
                db.session.delete(invoice_detail)
            else:
                if (statuses[idx] in ('In Stock - Claimed', 'Used - Claimed')
                        and statuses[idx] != invoice_detail.status):
                    invoice_detail.claimed = True
                    invoice_detail.claimed_date = datetime.date.today()
                elif statuses[idx] == 'New':
                    invoice_detail.claimed = False
                    invoice_detail.claimed_date = None
                invoice_detail.part = part
                invoice_detail.purchase_order_number = assoc_pos[idx]
                invoice_detail.status = statuses[idx]
                invoice_detail.shelf_location = shelf_locations[idx]
    db.session.commit()
    flash('Change(s) saved', 'alert-success')
    return redirect(url_for('invoices'))


@app.route('/inventory/parts/')
@login_required
@roles_accepted('admin', 'management')
def get_stock():
    category = 3
    page = "Stock Inventory"
    return render_template(
        'employee_site/inventory/parts.html',
        category=category,
        page=page
    )


@app.route('/inventory/parts/ajax')
@login_required
def get_stock_ajax():
    response = {}
    response['draw'] = int(request.args.get('draw', 0))
    per_page = int(request.args.get('length', 30))
    try:
        page = int(request.args['start']) / int(request.args['length']) + 1
    except:
        page = 1
    search = u'{}{}{}'.format('%', request.args.get('search[value]', ''), '%')
    response['recordsTotal'] = Part.query.count()
    if len(search) > 3:
        pagination_obj = Part.query.filter(
            (Part.part_number.like(search)) | (Part.description.like(search)) |
            (Part.machine_type.like(search)) | (Part.price.like(search))
        ).paginate(page=page, per_page=per_page)
    else:
        pagination_obj = Part.query.paginate(page=page, per_page=per_page)
    response['parts'] = parts_schema.dump(pagination_obj.items).data
    response['recordsFiltered'] = pagination_obj.total
    return jsonify(response)


@app.route('/inventory/parts/<path:part_number>/')
@login_required
@roles_accepted('admin', 'management')
def view_part(part_number):
    category = 3
    page = "Part Detail"
    part = Part.query.get_or_404(part_number)
    return render_template(
        'employee_site/inventory/part_detail.html',
        category=category,
        page=page,
        part=part
    )


@app.route('/inventory/parts/<path:part_number>/', methods=['POST'])
@login_required
@roles_accepted('admin', 'management')
def update_part(part_number):
    part = Part.query.get_or_404(part_number)
    part.description = request.form['part_description']
    part.machine_type = request.form['machine_type']
    part.price = (
        float(request.form['part_price']) if request.form['part_price']
        else None
    )
    part.image_url = request.form['image_url']
    db.session.commit()
    flash('Part detail updated', 'alert-success')
    return redirect(url_for('view_part', part_number=part_number))


@app.route('/inventory/parts/<path:part_number>/ajax')
@login_required
def view_part_ajax(part_number):
    part = Part.query.get_or_404(part_number)
    return jsonify(part_schema.dump(part).data)


@app.route('/inventory/report/')
@login_required
@roles_accepted('admin', 'management')
def inventory_report():
    category = 3
    page = "Inventory Report"
    return render_template(
        'employee_site/inventory/report.html',
        category=category,
        page=page
    )


@app.route('/inventory/report/ajax')
@login_required
def inventory_stats():
    from decimal import Decimal
    all_parts = Part.query.all()
    if request.args['type'] == 'parts':
        res = {}
        res['parts'] = parts_schema.dump(sorted(
            all_parts,
            key=lambda p: len(p.invoices),
            reverse=True
        )[:50]).data
    elif request.args['type'] == 'stat':
        res = {
            'cur_total_val': Decimal('0.00'),
            'cur_unclaimed_val': Decimal('0.00'),
            'cur_claimed_val': Decimal('0.00'),
        }
        for part in all_parts:
            if part.price:
                total_qty = len(
                    [i for i in part.invoices if (
                        i.status in ('New', 'In Stock - Claimed') and
                        i.shelf_location not in ('N/A', 'n/a', 'N/a', '', None)
                    )]
                )
                unclaimed_qty = len(
                    [i for i in part.invoices if (
                        i.status == 'New' and
                        i.shelf_location not in ('N/A', 'n/a', 'N/a', '', None)
                    )]
                )
                claimed_qty = len(
                    [i for i in part.invoices if (
                        i.status == 'In Stock - Claimed' and
                        i.shelf_location not in ('N/A', 'n/a', 'N/a', '', None)
                    )]
                )
                res['cur_total_val'] += total_qty * part.price
                res['cur_unclaimed_val'] += unclaimed_qty * part.price
                res['cur_claimed_val'] += claimed_qty * part.price
    return jsonify(res)


@app.route('/inventory/shelf/')
@login_required
@roles_accepted('admin', 'management')
def inventory_shelf_report():
    category = 3
    page = "Shelf Report"
    query = db.session.query(
        InvoiceDetail.shelf_location.distinct().label('shelf_location')
    )
    all_shelves = sorted(
        [i.shelf_location for i in query.all() if i.shelf_location]
    )
    return render_template(
        'employee_site/inventory/shelf_report.html',
        category=category,
        page=page,
        all_shelves=all_shelves
    )


@app.route('/inventory/shelf/', methods=['POST'])
@login_required
@roles_accepted('admin', 'management')
def shelf_report():
    shelf = request.form['shelf']
    invoices = InvoiceDetail.query.filter(
        InvoiceDetail.shelf_location == shelf,
    ).filter(
        InvoiceDetail.status.in_(('New', 'In Stock - Claimed')),
    ).all()
    return jsonify(
        invoices_detail_schema.dump(invoices).data
    )


@app.route('/test/')
@login_required
def internal_test():
    return render_template('employee_site/main_template.html')


@app.route('/test/ajax')
@login_required
def test_ajax():
    try:
        socketio.emit('my response',
                      {'data': 'Server generated event'},
                      namespace='/test/socketio')
        return 'test socketio'

    except Exception as e:
        return render_template('employee_site/500.html', error=e)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', debug=True)
