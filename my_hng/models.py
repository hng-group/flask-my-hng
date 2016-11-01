# -*- coding: utf-8 -*-
from flask_sqlalchemy import SQLAlchemy
from flask_security import RoleMixin, UserMixin

db = SQLAlchemy()


class Invoice(db.Model):
    invoice_number = db.Column(db.Unicode(50), primary_key=True, unique=True)
    received_date = db.Column(db.Date, nullable=False)
    parts = db.relationship('InvoiceDetail', back_populates="invoice")


class Part(db.Model):
    part_number = db.Column(db.Unicode(50), primary_key=True, unique=True)
    description = db.Column(db.Unicode(255))
    machine_type = db.Column(db.Unicode(100))
    price = db.Column(db.DECIMAL(10, 2))
    image_url = db.Column(db.Unicode(500))
    invoices = db.relationship('InvoiceDetail', back_populates='part')

    @classmethod
    def get_or_create(
        cls, part_number, session,
        description=None, machine_type=None, price=None,
    ):
        part = cls.query.get(part_number)
        if not part:
            part = cls(
                part_number=part_number,
                description=description,
                machine_type=machine_type,
                price=price,
            )
            session.add(part)
        return part

    @property
    def available_invoices(self):
        return [
            i for i in self.invoices if i.status in (
                'New', 'In Stock - Claimed'
            )
        ]


class InvoiceDetail(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    invoice_number = db.Column(
        db.Unicode(50), db.ForeignKey('invoice.invoice_number')
    )
    part_number = db.Column(
        db.Unicode(50), db.ForeignKey('part.part_number')
    )
    purchase_order_number = db.Column(db.Unicode(50))
    shelf_location = db.Column(db.Unicode(5))
    status = db.Column(
        db.Enum(
            u'New', u'Dispatched', u'In Stock - Claimed',
            u'Used - Claimed', u'Returned',
        ),
        default=u'New'
    )
    claimed = db.Column(db.Boolean, default=False)
    claimed_date = db.Column(db.Date, nullable=True)
    part = db.relationship('Part', back_populates='invoices')
    invoice = db.relationship('Invoice', back_populates='parts')


roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id')),
)


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True, unique=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))

    # Personal info
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    job_title = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(50))
    start_date = db.Column(db.Date(), nullable=False)
    birth_date = db.Column(db.Date())
    ssn = db.Column(db.String(10))
    driver_license = db.Column(db.String(20))
    dl_expiration_date = db.Column(db.Date())
    gender = db.Column(db.Enum('', 'M', 'F'))
    phone = db.Column(db.String(30))
    phone2 = db.Column(db.String(30))

    # Address
    address1 = db.Column(db.String(255))
    address2 = db.Column(db.String(255))
    city = db.Column(db.String(100))
    state = db.Column(db.String(20))

    # Emergency contact
    econtact_name = db.Column(db.String(100))
    econtact_phone = db.Column(db.String(30))
    econtact_relationship = db.Column(db.String(100))

    # Account status
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))
    exams = db.relationship('UserExam', backref='user', lazy='dynamic')


class Exam(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(255))
    description = db.Column(db.String(1000))
    start_date = db.Column(db.Date(), nullable=False)
    end_date = db.Column(db.Date())
    limit_minutes = db.Column(db.Integer)
    passphrase = db.Column(db.String(20))
    questions = db.relationship('Question', backref='exam', lazy='dynamic')
    users = db.relationship('UserExam', backref='exam', lazy='dynamic')


class Question(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    exam_id = db.Column(db.Integer, db.ForeignKey('exam.id'))
    question = db.Column(db.String(255), nullable=False)
    question_type = db.Column(db.Enum('Multiple Choice', 'Essay'))
    active = db.Column(db.Enum('T', 'F'))
    answers = db.relationship('Answer', backref='question', lazy='dynamic')


class Answer(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    answer = db.Column(db.String(255), nullable=False)
    is_correct = db.Column(db.Enum('T', 'F'))

user_exam_answers = db.Table(
    'user_exam_answers',
    db.Column('user_exam_id', db.Integer, db.ForeignKey('users_exams.id')),
    db.Column('answer_id', db.Integer, db.ForeignKey('answer.id')),
)


class UserExam(db.Model, UserMixin):
    __tablename__ = 'users_exams'
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    exam_id = db.Column(db.Integer, db.ForeignKey('exam.id'))
    score = db.Column(db.String(5))
    taken_date = db.Column(db.Date())
    is_available = db.Column(db.Enum('T', 'F'))
    answers = db.relationship("Answer", secondary=user_exam_answers)


class Client(db.Model, UserMixin):
    id = db.Column(db.String(255), primary_key=True, unique=True)
    email = db.Column(db.String(255))
    password = db.Column(db.String(255))

    # Personal info
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    added_date = db.Column(db.Date())
    phone = db.Column(db.String(30))
    phone2 = db.Column(db.String(30))

    # Address
    address1 = db.Column(db.String(255))
    address2 = db.Column(db.String(255))
    city = db.Column(db.String(100))
    state = db.Column(db.String(20))
    zip_code = db.Column(db.String(20))
    is_subscribed = db.Column(db.Enum('T', 'F'))


class Article(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    published_date = db.Column(db.Date())
    added_date = db.Column(db.Date())
    title = db.Column(db.String(500))
    category = db.Column(db.String(100))
    summary = db.Column(db.String(500))
    content = db.Column(db.Text())
    author_id = db.Column(db.String(50))
    status = db.Column(db.String(50))

# db.create_all()
