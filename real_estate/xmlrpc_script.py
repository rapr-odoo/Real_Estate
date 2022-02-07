# This script is used to connect with ODOO server using it's api
# This Script is not part of any module

from xmlrpc.client import ServerProxy

db = "odoo15-ent"
user = "admin"
passw = "admin"

# getting connection from server odoo server
common = ServerProxy('http://rahul:8069/xmlrpc/2/common')
uid = common.authenticate(db, user, passw, {})
if uid: print("[+] Connection Successfull !!!")

models = ServerProxy('http://rahul:8069/xmlrpc/2/object')

ids = models.execute_kw(db, uid, passw, 'estate.estate', 'search_read', [[(1, '=', 1)]])
print(ids)