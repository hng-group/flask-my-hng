from flask import flash
from dbconnect import connection
from MySQLdb import escape_string as thwart
import datetime
import gc

today_date = datetime.date.today()
def convert_date(raw_date):
	date_format='%m/%d/%Y'
	if raw_date == None:
		formatted_date = raw_date
	else:
		formatted_date = datetime.datetime.strptime(str(raw_date), '%Y-%m-%d').strftime(date_format)
	return formatted_date

class Invoice(object):
	def __init__(self, invoice_number, date_received, associated_parts):
		self.invoice_number = str(invoice_number)
		self.date_received = date_received.strftime('%Y-%m-%d')
		self.associated_parts = associated_parts

	def create(self):
		c, conn = connection()
		c.execute("INSERT INTO invoice (invoice_number, date_received) VALUES ( '%s', '%s' )" % (thwart(self.invoice_number), thwart(self.date_received) ) )
		conn.commit()
		c.close()
		conn.close()
		gc.collect()
		return True

	def import_invoice_from_excel(self):
		self.create()
		for each_part in self.associated_parts:
			invoice_detail = InvoiceDetail(invoice_number = self.invoice_number, part_number = each_part['part_number'], purchase_order_number = each_part['assoc_po'], shelf_location = None, status = 'New', claimed = 0, claimed_date = None)
			invoice_detail.create_excel()

			part = Part(part_number = each_part['part_number'], part_description = each_part['part_description'], machine_type = None, part_price = str(each_part['part_price']), image_url = None)
			part.create_or_update_excel()
		return True

	def check_if_exist(self):
		c, conn = connection()
		check = c.execute("SELECT * FROM invoice WHERE invoice_number = ('%s')" % (thwart(self.invoice_number)) )
		c.close()
		conn.close()
		gc.collect()
		if int(check) == 0:
			return False
		else:
			return True

	@staticmethod
	def get_all():
		all_invoices = []
		c, conn = connection()
		c.execute("SELECT I.*, (SELECT COUNT(*) FROM invoice_detail AS D WHERE D.invoice_number = I.invoice_number) AS number_of_items FROM invoice AS I ORDER BY date_received DESC")
		for i in c:
			all_invoices.append({ "invoice_number" : i[0], "date_received" : convert_date(i[1]), "number_of_items" : i[2]})
		c.close()
		conn.close()
		gc.collect()
		return all_invoices

class InvoiceDetail(object):
	def __init__(self, invoice_number, part_number, purchase_order_number, shelf_location, status, claimed, claimed_date):
		self.invoice_number = str(invoice_number)
		self.part_number = str(part_number)
		self.purchase_order_number = str(purchase_order_number)
		self.shelf_location = shelf_location
		self.status = str(status)
		self.claimed = str(claimed)
		self.claimed_date = claimed_date

	def create(self):
		c, conn = connection()
		c.execute("INSERT INTO invoice_detail (invoice_number, part_number, purchase_order_number, shelf_location, status, claimed, claimed_date) VALUES ( '%s', '%s', '%s', '%s', '%s', '%s', '%s' )" % ( thwart(self.invoice_number), thwart(self.part_number), thwart(self.purchase_order_number), thwart(self.shelf_location), thwart(self.status), thwart(self.claimed), thwart(self.claimed_date) ) )
		conn.commit()
		c.close()
		conn.close()
		gc.collect()
		return True

	def create_excel(self):
		c, conn = connection()
		c.execute("INSERT INTO invoice_detail (invoice_number, part_number, purchase_order_number, shelf_location, status, claimed) VALUES ( '%s', '%s', '%s', '', '%s', '%s' )" % ( thwart(self.invoice_number), thwart(self.part_number), thwart(self.purchase_order_number), thwart(self.status), thwart(self.claimed) ) )
		conn.commit()
		c.close()
		conn.close()
		gc.collect()
		return True

		
class Part(object):
	def __init__(self, part_number, part_description, machine_type, part_price, image_url):
		self.part_number = part_number
		self.part_description = part_description
		self.machine_type = machine_type
		self.part_price = part_price
		self.image_url = image_url

	def create(self):
		c, conn = connection()
		c.execute("INSERT INTO part_detail (part_number, part_description, machine_type, part_price, img_url) VALUES ( '%s', '%s', '%s', '%s', '%s')" % ( thwart(self.part_number), thwart(self.part_description), thwart(self.machine_type), thwart(self.part_price), thwart(self.image_url), thwart(self.part_number) ) )
		conn.commit()
		c.close()
		conn.close()
		gc.collect()
		return True

	def update(self):
		c, conn = connection()
		c.execute("UPDATE part_detail SET part_description = '%s', machine_type = '%s', part_price = '%s', img_url = '%s' WHERE part_number = ('%s')" % ( thwart(self.part_description), thwart(self.machine_type), thwart(self.part_price), thwart(self.image_url), thwart(self.part_number) ) )
		
		conn.commit()
		c.close()
		conn.close()
		gc.collect()
		return True

	def create_excel(self):
		c, conn = connection()
		c.execute("INSERT INTO part_detail (part_number, part_description, machine_type, part_price) VALUES ( '%s', '%s', 'Other', '%s')" % ( thwart(self.part_number), thwart(self.part_description), thwart(self.part_price) ) )
		conn.commit()
		c.close()
		conn.close()
		gc.collect()
		return True

	def update_excel(self):
		c, conn = connection()
		c.execute("UPDATE part_detail SET part_description = '%s', part_price = '%s' WHERE part_number = ('%s')" % ( thwart(self.part_description), thwart(self.part_price), thwart(self.part_number) ) )
		conn.commit()
		c.close()
		conn.close()
		gc.collect()
		return True

	def create_or_update_excel(self):
		if self.check_if_exist() == False:
			self.create_excel()
		elif self.check_if_exist() == True:
			self.update_excel()

	def check_if_exist(self):
		c, conn = connection()
		check = c.execute("SELECT * FROM part_detail WHERE part_number = ('%s')" % (thwart(self.part_number)) )
		c.close()
		conn.close()
		gc.collect()
		if int(check) == 0:
			return False
		else:
			return True

	@staticmethod
	def get_all():
		c, conn = connection()
		c.execute("SELECT * FROM part_detail")
		all_parts = c.fetchall()
		c.close()
		conn.close()
		gc.collect()
		return all_parts

	@staticmethod
	def get_stock_inventory():
		c, conn = connection()
		c.execute("SELECT * FROM part_detail")
		stock_parts = []
		for p in c:
			c.execute("SELECT P.part_number, P.part_description, P.machine_type, P.part_price, (SELECT COUNT(*) FROM invoice_detail AS I WHERE I.part_number = P.part_number AND I.status IN ('NEW', 'In Stock - Claimed')) AS total_quantity, (SELECT COUNT(*) FROM invoice_detail AS I WHERE I.part_number = P.part_number AND I.status IN ('NEW', 'In Stock - Claimed') AND I.shelf_location IS NOT NULL AND I.shelf_location NOT IN ('N/A', 'n/a', '')) AS stock_quantity, (SELECT COUNT(*) FROM invoice_detail AS I WHERE I.part_number = P.part_number AND I.status IN ('NEW') AND I.shelf_location IS NOT NULL AND I.shelf_location NOT IN ('N/A', 'n/a', '')) AS claimable_amount FROM part_detail AS P WHERE part_number = '%s'" % (thwart(p[0])) )
			part = c.fetchone()
			stock_parts.append({"part_number" : part[0], "part_description" : part[1], "machine_type" : part[2], "asc_price" : part[3], "total_quantity" : part[4], "stock_quantity" : part[5], "claimable_quanity" : part[6]})
		c.close()
		conn.close()
		gc.collect()
		return stock_parts

	@staticmethod
	def get_stock_quantity_for_part(part_number):
		c, conn = connection()
		c.execute("SELECT COUNT(*) FROM invoice_detail WHERE part_number = '%s' AND status IN ('NEW', 'In Stock - Claimed') AND shelf_location IS NOT NULL AND shelf_location NOT IN ('N/A', 'n/a', '')" % (thwart(part_number) ))
		result = c.fetchone()
		c.close()
		conn.close()
		gc.collect()
		return result[0]

	@staticmethod
	def get_by_part_number(part_number):
		c, conn = connection()
		c.execute("SELECT * FROM part_detail WHERE part_number = '%s'" % (thwart(part_number) ))
		part_detail = c.fetchone()
		c.close()
		conn.close()
		gc.collect()
		return part_detail

	@staticmethod
	def get_shelves():
		c, conn = connection()
		c.execute("SELECT DISTINCT shelf_location FROM invoice_detail")
		all_shelves = c.fetchall()
		c.close()
		conn.close()
		gc.collect()
		return all_shelves

	@staticmethod
	def get_shelf_report(shelf_name):
		c, conn = connection()
		c.execute("SELECT ID.invoice_detail_id, ID.invoice_number, ID.part_number, ID.purchase_order_number, ID.shelf_location, ID.status, ID.claimed, ID.claimed_date, P.part_price, I.date_received, P.part_description FROM inventory_mgmt.invoice_detail AS ID JOIN inventory_mgmt.part_detail AS P ON ID.part_number = P.part_number JOIN inventory_mgmt.invoice AS I ON ID.invoice_number = I.invoice_number WHERE ID.status IN ('New', 'In Stock - Claimed') AND ID.shelf_location = '%s'" % (thwart(shelf_name)))
		shelf_data = c.fetchall()
		shelf_data_list = []
		for i in shelf_data:
			shelf_data_list.append({
							"invoice_detail_id" : i[0],
							"invoice_number" : i[1],
							"part_number" : i[2],
							"assoc_po" : i[3],
							"location" : i[4],
							"status" : i[5],
							"claimed" : i[6],
							"claimed_date" : convert_date(i[7]),
							"part_price" : i[8],
							"received_date" : convert_date(i[9]),
							"part_description" : i[10]
							})

		c.close()
		conn.close()
		gc.collect()
		return shelf_data_list

	@staticmethod
	def get_invoice_detail(part_number):
		c, conn = connection()
		c.execute("SELECT * FROM invoice_detail WHERE part_number = '%s'" % (thwart(part_number) ))
		part_invoice_detail = c.fetchall()
		result = []
		for i in part_invoice_detail:
			result.append(
							{"invoice_detail_id" : i[0],
							"invoice_number" : i[1],
							"part_number" : i[2],
							"assoc_po" : i[3],
							"location" : i[4],
							"status" : i[5],
							"claimed" : i[6],
							"claimed_date" : convert_date(i[7])})
		c.close()
		conn.close()
		gc.collect()
		return result

