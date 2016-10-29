import MySQLdb


def connection():
    conn = MySQLdb.connect(
        host="localhost",
        user="root",
        db="inventory_mgmt"
    )
    c = conn.cursor()
    return c, conn
