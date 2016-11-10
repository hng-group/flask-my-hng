from flask_marshmallow import Marshmallow
from models import (
    Invoice, Part, InvoiceDetail, Role, User,
    Exam, Question, Answer, UserExam, Client, Article,
)


ma = Marshmallow()  # Flask-Marshmallow init


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


class ClientSchema(ma.ModelSchema):
    class Meta:
        model = Client


class ArticleSchema(ma.ModelSchema):
    class Meta:
        model = Article


class InvoiceSchema(ma.ModelSchema):
    class Meta:
        model = Invoice


class InvoiceDetailSchema(ma.ModelSchema):
    class Meta:
        model = InvoiceDetail

    invoice = ma.Nested(InvoiceSchema(), exclude=('parts',))
    part = ma.Nested('PartSchema', exclude=('invoices',))


class PartSchema(ma.ModelSchema):
    class Meta:
        model = Part

    invoices = ma.Nested(InvoiceDetailSchema(), many=True)


role_schema = RoleSchema()
roles_schema = RoleSchema(many=True)
user_schema = UserSchema()
users_schema = UserSchema(many=True)
exam_schema = ExamSchema()
exams_schema = ExamSchema(many=True)
question_schema = QuestionSchema()
questions_schema = QuestionSchema(many=True)
answer_schema = AnswerSchema()
answers_schema = AnswerSchema(many=True)
user_exam_schema = UserExamSchema()
users_exams_schema = UserExamSchema(many=True)
client_schema = ClientSchema()
clients_schema = ClientSchema(many=True)
article_schema = ArticleSchema()
articles_schema = ArticleSchema(many=True)
invoice_schema = InvoiceSchema()
invoices_schema = InvoiceSchema(many=True)
part_schema = PartSchema()
parts_schema = PartSchema(many=True)
invoice_detail_schema = InvoiceDetailSchema()
invoices_detail_schema = InvoiceDetailSchema(many=True)
