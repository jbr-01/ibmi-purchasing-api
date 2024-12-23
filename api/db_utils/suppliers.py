
import ibm_db
from django.conf import settings

schema = settings.IBM_SCHEMA

base_query = f"""
    SELECT 
        A.PAYCOD supplier_code, 
        LNAME supplier_last_name, 
        FNAME supplier_first_name, 
        MI supplier_middle_initial, 
        TRIM(TEXT1)||' '||TRIM(TEXT2)||' '||TRIM(TEXT3) supplier_extension_name,
        TRIM(ADDR1)||' '||TRIM(ADDR2) supplier_address,
        CITICD citizenship,
        NATINC nature_of_income,
        TAN tin,
        ICCODE corporate_code
    FROM {schema}.GPAYPF A

    LEFT JOIN DBRLIB.GPAXPF B
    ON A.PAYCOD = B.PAYCOD"""

# Create a connection
def get_connection():
    return ibm_db.connect(settings.IBM_DB_NAME, settings.IBM_USERNAME, settings.IBM_PASSWORD)

def fetch_all_suppliers():
    conn = get_connection()
    query = base_query
    print(query)
    stmt = ibm_db.exec_immediate(conn, query)
    suppliers = []
    row = ibm_db.fetch_assoc(stmt)
    while row:
        suppliers.append(row)
        row = ibm_db.fetch_assoc(stmt)
    
    ibm_db.close(conn)
    return suppliers

def fetch_supplier_by_id(supplier_code):
    conn = get_connection()
    query = f"""
        {base_query} WHERE A.PAYCOD = ?"""
    print(query)
    stmt = ibm_db.prepare(conn, query)
    ibm_db.bind_param(stmt, 1, supplier_code)
    ibm_db.execute(stmt)
    
    supplier = ibm_db.fetch_assoc(stmt)
    ibm_db.close(conn)
    return supplier
