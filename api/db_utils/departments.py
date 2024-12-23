
import ibm_db
from django.conf import settings

schema = settings.IBM_SCHEMA

base_query = f"""
    SELECT 
        DEPTCD department_code,
        DEPNME department_name
    FROM {schema}.GDEPPF"""

# Create a connection
def get_connection():
    return ibm_db.connect(settings.IBM_DB_NAME, settings.IBM_USERNAME, settings.IBM_PASSWORD)

def fetch_all_departments():
    conn = get_connection()
    query = base_query
    print(query)
    stmt = ibm_db.exec_immediate(conn, query)
    departments = []
    row = ibm_db.fetch_assoc(stmt)
    while row:
        departments.append(row)
        row = ibm_db.fetch_assoc(stmt)
    
    ibm_db.close(conn)
    return departments

def fetch_department_by_id(department_code):
    conn = get_connection()
    query = f"""
        {base_query} WHERE DEPTCD = ?"""
    print(query)
    stmt = ibm_db.prepare(conn, query)
    ibm_db.bind_param(stmt, 1, department_code)
    ibm_db.execute(stmt)
    
    department = ibm_db.fetch_assoc(stmt)
    ibm_db.close(conn)
    return department
