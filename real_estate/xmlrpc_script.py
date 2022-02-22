# This script is used to connect with ODOO server using it's api
# This Script is not part of any module

from xmlrpc.client import ServerProxy
from datetime import date,timedelta


db = "odoo15-ent"
user = "admin"
passw = "admin"

estate_dict = {'name': False,
               'mobile_no': False,
               'description': False,
               'address': False,
               'state': 'prebook',
               'client_id': False,
               'price': 0.0,
               'discount': 0.0,
               'total': 0.0,
               'booking_start': date.today(),
               'booking_end': date.today() + timedelta(days=30),
               'buyer': False,
               'offer_ids': False,
               'property_image': False
               }

client_dict = {'user_id': False,
               'mobile': False,
               'property_ids': False,
               'total_assets': 0.0
               }

# getting connection from server odoo server
common = ServerProxy('http://rahul:8069/xmlrpc/2/common')
uid = common.authenticate(db, user, passw, {})
if uid: print("[+] Connection Successfull !!!")
else: exit(1)

models = ServerProxy('http://rahul:8069/xmlrpc/2/object')

def create_record(record, model_name):
    for field in record:
        ans = input(f"{field.capitalize()} = ")
        record[field] = ans if ans != '' else record[field]
    id = models.execute_kw(db, uid, passw, model_name, 'create', [record])
    print(record, id)

def update_record(model_name):
    pass

def search_record(model_name):
    pass

def delete_record(model_name):
    pass

def main():
    model_name = input('Model Name: ')
    
    while 1:
        
        op = int(input('Option: '))
        record = None
        if op == 1:
            if model_name == 'estate.estate':
                record = estate_dict.copy()
            elif model_name == 'estate.client':
                record = client_dict.copy()
            else: 
                print('[Error]: Please Check the model name')
                model_name = input('Model Name: ')
                continue
            create_record(record, model_name)
                
        elif op == 2:
            pass
        elif op == 3:
            pass
        elif op == 4:
            pass
        elif op == 5:
            model_name = input('Model Name: ')
        elif op == 6:
            print("Good Bye !!!")
            exit(0)
        else:
            print("[Error]: Please Choose from 1 to 4 only...\n")

        # ids = models.execute_kw(db, uid, passw, 'estate.estate', 'search_read', [[(1, '=', 1)]])
        # print(ids)
        

if __name__ == "__main__":
    main()