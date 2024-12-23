
import ibm_db
from django.conf import settings

schema = settings.IBM_SCHEMA

base_query = f"""
    SELECT DISTINCT
    A.PROJCD project_code,
    PTITLE project_title,
    PJINIT project_initials,
    COALESCE(TRIM(D.LOCATN), '') || ' ' || COALESCE(TRIM(E.LOCTN2), '') ||' '|| 
        COALESCE(TRIM(E.LOCTN3), '') project_address,
    COALESCE(B.COMPCD, 0) company_code,
    COALESCE(C.CONAME, '') company_name

    FROM {schema}.IPRJPF A

    LEFT JOIN {schema}.INV1PF B
    ON A.PROJCD = B.PROJCD

    LEFT JOIN {schema}.ICOMPF C
    ON B.COMPCD = C.COMPCD
    
    LEFT JOIN {schema}.TASFPF D
    ON A.PROJCD = D.PROJCD
    AND D.RESCOM = 'R'

    LEFT JOIN {schema}.TASF3PF E
    ON A.PROJCD = E.PROJCD
    AND E.RESCOD = 'R' """

# Create a connection
def get_connection():
    return ibm_db.connect(settings.IBM_DB_NAME, settings.IBM_USERNAME, settings.IBM_PASSWORD)

def fetch_all_projects():
    conn = get_connection()
    query = base_query
    stmt = ibm_db.exec_immediate(conn, query)
    projects = []
    row = ibm_db.fetch_assoc(stmt)
    while row:
        projects.append(row)
        row = ibm_db.fetch_assoc(stmt)
    
    ibm_db.close(conn)
    return projects

def fetch_project_by_id(project_code):
    conn = get_connection()
    query = f"""
        {base_query} WHERE A.PROJCD = UPPER(?)"""
    stmt = ibm_db.prepare(conn, query)
    ibm_db.bind_param(stmt, 1, project_code)
    ibm_db.execute(stmt)
    
    project = ibm_db.fetch_assoc(stmt)
    ibm_db.close(conn)
    return project
