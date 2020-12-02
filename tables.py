from server import db

class User(db.Model):
	__tablename__ = 'user'
	#__table_args__ = {'extend_existing': True}
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(50), nullable=False)
	user_courses = db.relationship("User_Courses")
	course_questions = db.relationship("Course_Questions")

	def __repr__ (self):
		return f"User('{self.email}')"

class User_Courses(db.Model):
	__tablename__ = 'user_courses'
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	course_id = db.Column(db.Integer, db.ForeignKey('courses.code'))

class Teacher(db.Model):
	__tablename__ = 'teacher'
	id = db.Column(db.Integer, primary_key=True)
	first_name = db.Column(db.String(20), nullable=False)
	last_name = db.Column(db.String(20), nullable=False)
	email = db.Column(db.String(50), nullable=False)
	teacher_courses = db.relationship("Teacher_Courses")

	def __repr__ (self):
		return f"Teacher('{self.first_name}', '{self.last_name}', '{self.email}')"

class Teacher_Courses(db.Model):
	__tablename__ = 'teacher_courses'
	id = db.Column(db.Integer, primary_key=True)
	teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'))
	course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))

class Courses(db.Model):
	__tablename__ = 'courses'
	id = db.Column(db.Integer, primary_key=True)
	code = db.Column(db.String(10), nullable=False)
	course_name = db.Column(db.String(20), nullable=False)
	teacher_courses = db.relationship("Teacher_Courses")
	course_question_answer = db.relationship("Course_Question_Answer")
	course_questions = db.relationship("Course_Questions")
	message_history = db.relationship("Message_History")
	course_materials = db.relationship("Course_Materials")
	user_courses = db.relationship("User_Courses")

	def __repr__ (self):
		return f"Course('{self.code}', '{self.course_name}')"

class Course_Questions(db.Model):
	__tablename__ = 'course_questions'
	id = db.Column(db.Integer, primary_key=True)
	sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))
	message = db.Column(db.String(1000), nullable=False)
	created_on = db.Column(db.TIMESTAMP, nullable=False)

class Course_Question_Answer(db.Model):
	__tablename__ = 'course_question_answer'
	id = db.Column(db.Integer, primary_key=True)
	course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))
	question = db.Column(db.String(1000), nullable=False)
	answer = db.Column(db.String(1000), nullable=False)

class Course_Materials(db.Model):
	__tablename__ = 'course_materials'
	id = db.Column(db.Integer, primary_key=True)
	course_id = db.Column(db.Integer, db.ForeignKey('courses.code'))
	content = db.Column(db.Text, nullable=False)

class Message_History(db.Model):
	__tablename__ = 'message_history'
	id = db.Column(db.Integer, primary_key=True)
	course_id = db.Column(db.Integer, db.ForeignKey('courses.code'))
	receiver_id = db.Column(db.Integer)
	sender_id = db.Column(db.Integer)
	created_on = db.Column(db.TIMESTAMP, nullable=False)
	message = db.Column(db.String(1000), nullable=False)