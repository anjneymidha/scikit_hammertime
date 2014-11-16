import MySQLdb
import re

class DB():

	def __init__(self):
		self.db = MySQLdb.connect(host="localhost",user="root",
                  passwd="timber",db="rx")

	def query(self, qstring):
		newqstring = re.sub(r'\([^)]*\)', '', qstring)
		newerstring = re.sub(r'\W+', '', newqstring)
		q = """SELECT RXCUI FROM RXNCONSO WHERE str ='""" + newerstring + """' LIMIT 1"""
		c = self.db.cursor()
		results = c.execute(q)
		r=c.fetchone()
		return r[0]





from p import DB
d = DB()

d.query("modafinil")