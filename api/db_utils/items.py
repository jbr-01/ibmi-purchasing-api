
import ibm_db
from django.conf import settings

schema = settings.IBM_SCHEMA

base_query = f"""
    SELECT 
        ITEMCD item_code,
        ITMDES item_description,
        UNIT unit_of_measurement,
        ACCTCD account_code
    FROM {schema}.JITMPF """

# Create a connection
def get_connection():
    return ibm_db.connect(settings.IBM_DB_NAME, settings.IBM_USERNAME, settings.IBM_PASSWORD)

def fetch_all_items():
    conn = get_connection()
    query = base_query
    print(query)
    stmt = ibm_db.exec_immediate(conn, query)
    items = []
    row = ibm_db.fetch_assoc(stmt)
    while row:
        items.append(row)
        row = ibm_db.fetch_assoc(stmt)
    
    ibm_db.close(conn)
    return items

def fetch_item_by_id(item_code):
    conn = get_connection()
    query = f"""
        {base_query} WHERE ITEMCD = ?"""
    print(query)
    stmt = ibm_db.prepare(conn, query)
    ibm_db.bind_param(stmt, 1, item_code)
    ibm_db.execute(stmt)
    
    item = ibm_db.fetch_assoc(stmt)
    ibm_db.close(conn)
    return item
