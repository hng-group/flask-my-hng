import MySQLdb

def connection():
	conn = MySQLdb.connect(host = "localhost", user = "root", passwd ="Steven93", db = "inventory_mgmt")
	c = conn.cursor()
	return c, conn