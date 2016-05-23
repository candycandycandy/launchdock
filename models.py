import datetime

from peewee import *

DATABASE = SqliteDatabase('launch.sqlite')

class Company(Model):
	name = CharField()
	address = CharField()
	created_at = DateTimeField(default=datetime.datetime.now)

	class Meta:
		database = DATABASE

class Marina(Model):
	name = CharField()
	address = CharField()
	company = ForeignKeyField(Company, related_name='marinas')
	created_at = DateTimeField(default=datetime.datetime.now)

	class Meta:
		database = DATABASE

def initialize():
	DATABASE.connect()
	DATABASE.create_tables([Company, Marina], safe=True)
	DATABASE.close()
