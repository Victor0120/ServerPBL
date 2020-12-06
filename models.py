from server import db
import datetime

UserCourse = db.Table('user_course', db.Model.metadata,
	db.Column('user', db.Integer, db.ForeignKey('user.id')),
	db.Column('course', db.Integer, db.ForeignKey('course.id'))
)


TeacherCourse = db.Table('teacher_course', db.Model.metadata,
	db.Column('user', db.Integer, db.ForeignKey('teacher.id')),
	db.Column('course', db.Integer, db.ForeignKey('course.id'))
)

class User(db.Model):
	__tablename__ = 'user'
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(50), nullable=False)

	courses = db.relationship("Course", secondary=UserCourse, backref='users')
	course_questions = db.relationship("CourseQuestion", back_populates="sender")
	#sent_messages = db.relationship("MessageHistory", back_populates="sender", foreign_keys=[message_history.sender_id])
	#received_messages = db.relationship("MessageHistory", back_populates="receiver", foreign_keys=[message_history.receiver_id])

	def __repr__ (self):
		return f"User('{self.email}')"


class Teacher(db.Model):
	__tablename__ = 'teacher'
	id = db.Column(db.Integer, primary_key=True)
	first_name = db.Column(db.String(20), nullable=False)
	last_name = db.Column(db.String(20), nullable=False)
	email = db.Column(db.String(50), nullable=False)

	courses = db.relationship("Course", secondary=TeacherCourse, backref="teachers")
	#courses = db.relationship("TeacherCourse", back_populates="teachers")

	def __repr__ (self):
		return f"Teacher('{self.first_name}', '{self.last_name}', '{self.email}')"



class Course(db.Model):
	__tablename__ = 'course'
	id = db.Column(db.Integer, primary_key=True)
	code = db.Column(db.String(10), nullable=False)
	course_name = db.Column(db.String(50), nullable=False)

	#users = db.relationship("UserCourse",  back_populates="course")
	#teachers = db.relationship("TeacherCourse", back_populates="courses")
	course_questions = db.relationship("CourseQuestion", back_populates="course")
	course_materials = db.relationship("CourseMaterial", back_populates="course")
	message_history = db.relationship("MessageHistory", back_populates="course")
	course_question_answers = db.relationship("CourseQuestionAnswer", back_populates="course")

	def __repr__ (self):
		return f"Course('{self.code}', '{self.course_name}')"


class CourseQuestion(db.Model):
	__tablename__ = 'course_question'
	id = db.Column(db.Integer, primary_key=True)
	sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
	message = db.Column(db.String(1000), nullable=False)
	created_on = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)

	course = db.relationship("Course", back_populates="course_questions")
	sender = db.relationship("User", back_populates="course_questions")

	def __repr__(self):
		return f"CourseQuestion[course_id,sender_id, question]('{self.course_id}', '{self.sender_id}', {self.message})"


class CourseQuestionAnswer(db.Model):
	__tablename__ = 'course_question_answer'
	id = db.Column(db.Integer, primary_key=True)
	course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
	question = db.Column(db.String(1000), nullable=False)
	answer = db.Column(db.String(1000), nullable=False)

	course = db.relationship("Course", back_populates="course_question_answers")

	def __repr__(self):
		return f"CourseQuestionAnswer[course_id, question, answer]('{self.course_id}, {self.question}, {self.answer}')"


class CourseMaterial(db.Model):
	__tablename__ = 'course_material'
	id = db.Column(db.Integer, primary_key=True)
	course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
	data = db.Column(db.LargeBinary)

	course = db.relationship("Course", back_populates="course_materials")

	def __repr__(self):
		return f"CourseMaterial[course_id]('{self.course_id})"


class MessageHistory(db.Model):
	__tablename__ = 'message_history'
	id = db.Column(db.Integer, primary_key=True)
	course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
	receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	created_on = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)
	message = db.Column(db.String(1000), nullable=False)

	sender = db.relationship("User", backref="sent_messages", foreign_keys=[sender_id])
	receiver = db.relationship("User", backref="received_messages", foreign_keys=[receiver_id])
	course = db.relationship("Course", back_populates="message_history")

	def __repr__(self):
		return f"MessageHistory[course_id]({self.course_id})"

#schemes
from server import marshmallow

class CourseScheme(marshmallow.SQLAlchemySchema):
	class Meta:
		model = Course

	id = marshmallow.auto_field()
	code = marshmallow.auto_field()
	course_name = marshmallow.auto_field()

class UserScheme(marshmallow.SQLAlchemySchema):
	class Meta:
		model = User

	id = marshmallow.auto_field()
	email = marshmallow.auto_field()

class TeacherScheme(marshmallow.SQLAlchemySchema):
	class Meta:
		model = Teacher

	id = marshmallow.auto_field()
	first_name = marshmallow.auto_field()
	last_name = marshmallow.auto_field()
	email = marshmallow.auto_field()

class CourseQuestionScheme(marshmallow.SQLAlchemySchema):
	class Meta:
		model = CourseQuestion

	id = marshmallow.auto_field()
	sender_id = marshmallow.auto_field()
	course_id = marshmallow.auto_field()
	message = marshmallow.auto_field()
	created_on = marshmallow.auto_field()

class CourseQuestionAnswerScheme(marshmallow.SQLAlchemySchema):
	class Meta:
		model = CourseQuestionAnswer

	id = marshmallow.auto_field()
	course_id = marshmallow.auto_field()
	question = marshmallow.auto_field()
	answer = marshmallow.auto_field()

class CourseMaterialScheme(marshmallow.SQLAlchemySchema):
	class Meta:
		model = CourseMaterial

	id = marshmallow.auto_field()
	course_id = marshmallow.auto_field()
	data = marshmallow.auto_field()

class MessageHistoryScheme(marshmallow.SQLAlchemySchema):
	class Meta:
		model = MessageHistory

	id = marshmallow.auto_field()
	course_id = marshmallow.auto_field()
	receiver_id = marshmallow.auto_field()
	sender_id = marshmallow.auto_field()
	created_on = marshmallow.auto_field()
	message = marshmallow.auto_field()				