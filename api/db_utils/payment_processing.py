import ibm_db
from decimal import Decimal
from django.conf import settings

schema = settings.IBM_SCHEMA
debug = settings.DEBUG

# Create a connection
def get_connection():
    return ibm_db.connect(settings.IBM_DB_NAME, settings.IBM_USERNAME, settings.IBM_PASSWORD)

def fetch_voucher_request_by_id(voucher_request_no):
    try:
        conn = get_connection()
        query = f""" 
            SELECT
                VREQNO VOUCHER_REQUEST_NO,
                VRDTL VOUCHER_REQUEST_DETAIL,
                TRIM(VRSTAT) VOUCHER_REQUEST_STATUS
            FROM {schema}.VFL_API WHERE VREQNO = ?"""
        stmt = ibm_db.prepare(conn, query)
        ibm_db.bind_param(stmt, 1, voucher_request_no)
        ibm_db.execute(stmt)
        
        voucher_requests = []
        row = ibm_db.fetch_assoc(stmt)
        while row:
            voucher_requests.append(row)
            row = ibm_db.fetch_assoc(stmt)
        
        return {
            "data": voucher_requests
        }
            
    except Exception as e:
        return {
            "status": "error",
            "error": "SQL_ERROR",
            "message": f"Database error occurred: {e}",
            "data": None
        }
        
    finally:
        # Safely close the connection
        if 'conn' in locals() and conn:
            ibm_db.close(conn)
            # print("Database connection closed.")

def format_with_commas(number):
    # Use Python's string formatting with commas and two decimal places
    return f"{number:,.2f}"

def add_voucher_request(data_list):
    try:
        voucher_type = 'C' # TODO: FIGURE OUT LOGIC FOR 'C' 
        conn = get_connection()
        query = f"""
            INSERT INTO {schema}.VFL1PF VALUES (
            ?, ?, ?, ?, 0, 0, 0, '', 0, 0, 0, 0, ?,
            ?, '', ?, 0, 0, 0, 0, 0, '', 0, '', '', 0) 
            WITH NONE
        """
        stmt = ibm_db.prepare(conn, query)
        
        voucher = data_list
        supplier = voucher["supplier"]
        
        ibm_db.bind_param(stmt, 1, voucher["voucher_request_no"])
        ibm_db.bind_param(stmt, 2, voucher_type)
        ibm_db.bind_param(stmt, 3, voucher["company_code"])
        ibm_db.bind_param(stmt, 4, voucher["branch_code"])
        ibm_db.bind_param(stmt, 5, supplier["code"])
        ibm_db.bind_param(stmt, 6, supplier["name"])
        ibm_db.bind_param(stmt, 7, Decimal(voucher["total_amount"]))
        
        ibm_db.execute(stmt)
        
        # Insert lines
        par_ctr = 1
        for line in voucher["lines"]:
            line_no = voucher["lines"].index(line) + 1
            
            if line_no == 1:
                # Insert 1st row in particulars file
                line_query = f"""
                    INSERT INTO {schema}.VPARPF VALUES 
                        (?, ?, ?, ?, 0, 0, 0, '', 0, ?, 'Qty. Unit Description Amount')
                    WITH NONE"""
                line_stmt = ibm_db.prepare(conn, line_query)
                ibm_db.bind_param(line_stmt, 1, voucher["voucher_request_no"])
                ibm_db.bind_param(line_stmt, 2, voucher_type)
                ibm_db.bind_param(line_stmt, 3, voucher["company_code"])
                ibm_db.bind_param(line_stmt, 4, voucher["branch_code"])
                ibm_db.bind_param(line_stmt, 5, par_ctr)
                ibm_db.execute(line_stmt)
            
            # Insert items
            for item in line["items"]:
                item_query = f"""
                    INSERT INTO {schema}.VFL2PF VALUES 
                        (?, ?, ?, ?, 0, 0, 0, '', 0, ?, ?, ?, 0,
                        0, '', '', 0, '', 0) 
                    WITH NONE"""
                item_stmt = ibm_db.prepare(conn, item_query)
                ibm_db.bind_param(item_stmt, 1, voucher["voucher_request_no"])
                ibm_db.bind_param(item_stmt, 2, voucher_type)
                ibm_db.bind_param(item_stmt, 3, voucher["company_code"])
                ibm_db.bind_param(item_stmt, 4, voucher["branch_code"])
                ibm_db.bind_param(item_stmt, 5, line_no)
                ibm_db.bind_param(item_stmt, 6, line["account_code"])
                ibm_db.bind_param(item_stmt, 7, Decimal(item["amount"]))
                ibm_db.execute(item_stmt)
                
                # Insert items as succeeding rows in particulars file
                par_ctr += 1
                line_query = f"""
                    INSERT INTO {schema}.VPARPF VALUES 
                        (?, ?, ?, ?, 0, 0, 0, '', 0, ?, ?)
                    WITH NONE"""
                line_stmt = ibm_db.prepare(conn, line_query)
                ibm_db.bind_param(line_stmt, 1, voucher["voucher_request_no"])
                ibm_db.bind_param(line_stmt, 2, voucher_type)
                ibm_db.bind_param(line_stmt, 3, voucher["company_code"])
                ibm_db.bind_param(line_stmt, 4, voucher["branch_code"])
                ibm_db.bind_param(line_stmt, 5, par_ctr)
                particular = f"""{item["quantity"]} {item["unit"]} {item["description"][:16]} {format_with_commas(Decimal(item["amount"]))}"""
                ibm_db.bind_param(line_stmt, 6, particular)
                ibm_db.execute(line_stmt)
            
        # Insert 'Totals' rows in particulars file
        par_ctr += 1
        line_query = f"""
            INSERT INTO {schema}.VPARPF VALUES 
                (?, ?, ?, ?, 0, 0, 0, '', 0, ?, ?),
                (?, ?, ?, ?, 0, 0, 0, '', 0, ?, ?)
            WITH NONE"""
        line_stmt = ibm_db.prepare(conn, line_query)
        ibm_db.bind_param(line_stmt, 1, voucher["voucher_request_no"])
        ibm_db.bind_param(line_stmt, 2, voucher_type)
        ibm_db.bind_param(line_stmt, 3, voucher["company_code"])
        ibm_db.bind_param(line_stmt, 4, voucher["branch_code"])
        ibm_db.bind_param(line_stmt, 5, par_ctr)
        ibm_db.bind_param(line_stmt, 6, '____________')
        ibm_db.bind_param(line_stmt, 7, voucher["voucher_request_no"])
        ibm_db.bind_param(line_stmt, 8, voucher_type)
        ibm_db.bind_param(line_stmt, 9, voucher["company_code"])
        ibm_db.bind_param(line_stmt, 10, voucher["branch_code"])
        ibm_db.bind_param(line_stmt, 11, par_ctr + 1)
        ibm_db.bind_param(line_stmt, 12, format_with_commas(Decimal(voucher["total_amount"])))
        ibm_db.execute(line_stmt)
        
        # Insert into VR API Details file 
        api_query = f"""INSERT INTO {schema}.VFL_API VALUES (?, ?, '') WITH NONE"""
        api_stmt = ibm_db.prepare(conn, api_query)
        ibm_db.bind_param(api_stmt, 1, voucher["voucher_request_no"])
        ibm_db.bind_param(api_stmt, 2, str(data_list))
        ibm_db.execute(api_stmt)
        
        # Insert into logs file
        log_query = f"""
            INSERT INTO {schema}.ITLOGPF VALUES (
                ?, INT(CURRENT_DATE), INT(CURRENT_TIME), 'VFL_API', 'ADD',
                ?, 'RECORD ADDED FROM PRS WEB APP', 'THRU IBM i API'
            ) WITH NONE"""
        log_stmt = ibm_db.prepare(conn, log_query)
        ibm_db.bind_param(log_stmt, 1, voucher["prs_username"])
        ibm_db.bind_param(log_stmt, 2, voucher["voucher_request_no"])
        ibm_db.execute(log_stmt)
        
        return {
            "status": "success",
            "message": "Voucher request added successfully.",
            "data": str(data_list)
        }

    except Exception as e:
        return {
            "status": "error",
            "error": "SQL_ERROR",
            "message": f"Database error occurred: {e}",
            "data": { "voucher_request_no": voucher["voucher_request_no"]}
        }

    finally:
        if 'conn' in locals() and conn:
            ibm_db.close(conn)
            # print("Database connection closed.")


def cancel_voucher_request_by_id(voucher_request_no):
    try:
        conn = get_connection()
        query = f"""
            UPDATE {schema}.VFL_API
            SET VRSTAT = 'CANCELLED'
            WHERE VREQNO = ?
            WITH NONE"""
        
        stmt = ibm_db.prepare(conn, query)
        ibm_db.bind_param(stmt, 1, voucher_request_no)
        res = ibm_db.execute(stmt)
        if res:
            rows_affected = ibm_db.num_rows(stmt)
            if rows_affected > 0:
                return {
                    "status": "success",
                    "message": "Voucher request CANCELLED successfully.",
                    "data": { "voucher_request_no": voucher_request_no }
                }
            else:
                return {
                    "status": "error",
                    "error": "NOT_FOUND",
                    "message": "No records were cancelled. The condition did not match any rows.",
                    "data": { "voucher_request_no": voucher_request_no }
                }
                
        return {
            "status": "error",
            "error": "VALIDATION_ERROR",
            "message": "Invalid input provided.",
            "data": { "voucher_request_no": voucher_request_no },
        }
    
    except Exception as e:
        return {
            "status": "error",
            "error": "SQL_ERROR",
            "message": f"Database error occurred: {e}",
            "data": { "voucher_request_no": voucher_request_no },
        }
        
    finally:
        # Safely close the connection
        if 'conn' in locals() and conn:
            ibm_db.close(conn)
            # print("Database connection closed.")
        