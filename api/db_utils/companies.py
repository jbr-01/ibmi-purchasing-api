
import ibm_db
from django.conf import settings

schema = settings.IBM_SCHEMA
db_name = settings.IBM_DB_NAME
db_user = settings.IBM_USERNAME
db_pwd = settings.IBM_PASSWORD

base_query = f"""
    SELECT 
        A.COMPCD company_code, 
        CONAME company_name, 
        COINIT company_initials, 
        TIN company_tin, 
        0 company_contact_no, 
        coalesce(TRIM(B.ADDR1) ||' '||TRIM(B.ADDR2)||' '||TRIM(B.ADDR3), '') company_address
    FROM {schema}.ICOMPF A

    LEFT JOIN {schema}.TSECPF B
    ON A.COMPCD = B.COMPCD"""

# Create a connection
def get_connection():
    return ibm_db.connect(db_name, db_user, db_pwd)

def fetch_all_companies():
    conn = get_connection()
    query = base_query
    print(query)
    stmt = ibm_db.exec_immediate(conn, query)
    companies = []
    row = ibm_db.fetch_assoc(stmt)
    while row:
        companies.append(row)
        row = ibm_db.fetch_assoc(stmt)
    
    ibm_db.close(conn)
    return companies

def fetch_company_by_id(company_code):
    conn = get_connection()
    query = f"""{base_query} WHERE A.COMPCD = ?"""
    stmt = ibm_db.prepare(conn, query)
    ibm_db.bind_param(stmt, 1, company_code)
    ibm_db.execute(stmt)
    
    company = ibm_db.fetch_assoc(stmt)
    ibm_db.close(conn)
    return company
