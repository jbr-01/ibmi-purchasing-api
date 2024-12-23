
import ibm_db
from decimal import Decimal
from django.conf import settings

schema = settings.IBM_SCHEMA
debug = settings.DEBUG
# addl_query = "WHERE TFERDT BETWEEN 20240101 AND 20241231" if debug else "" # TEMPORARY ONLY! REMOVE THIS EVENTUALLY.

base_query = f"""
    SELECT 
        VREQNO voucher_request_no,
        CODE, DATA,
        TFERDT date_transferred,
        TFERTM time_transferred,
        REFNUM reference_no,
        DATDEL date_deleted
    FROM {schema}.VREQPF"""

# Create a connection
def get_connection():
    return ibm_db.connect(settings.IBM_DB_NAME, settings.IBM_USERNAME, settings.IBM_PASSWORD)

# def fetch_all_voucher_requests():
#     conn = get_connection()
#     query = f"""{base_query} {addl_query}"""
#     print(query)
#     stmt = ibm_db.exec_immediate(conn, query)
#     voucher_requests = []
#     row = ibm_db.fetch_assoc(stmt)
#     while row:
#         voucher_requests.append(row)
#         row = ibm_db.fetch_assoc(stmt)
    
#     ibm_db.close(conn)
#     return voucher_requests

def fetch_voucher_request_by_id(voucher_request_no):
    try:
        conn = get_connection()
        query = f"""
            {base_query} WHERE VREQNO = ?"""
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
            
    except ibm_db.IbmDbError as e:
        return {
            "status": "error",
            "message": f"Database error occurred: {e}",
            "data": None
        }
        
    finally:
        # Safely close the connection
        if 'conn' in locals() and conn:
            ibm_db.close(conn)
            print("Database connection closed.")

def format_with_commas(number):
    # Use Python's string formatting with commas and two decimal places
    return f"{number:,.2f}"

def add_voucher_request(data_list):
    
    voucher_request_no = data_list['voucher_request_no']
    reference_no = data_list['reference_no']
    header = data_list['header']
    detail = data_list['detail']
    particulars = data_list['particulars']
    particulars_total_amount = Decimal(data_list['particulars_total_amount'])
    
    i_code = []
    i_data = []
    
    # Setup Header
    
    # Remove the decimal point
    total_amount = Decimal(header['total_amount'])
    number_without_decimal = int(total_amount * 100)  # Multiply by 100 to shift two decimal places and convert to integer

    # Format with leading zeros
    header_total_amount = f"{number_without_decimal:012}"  # Pad to 12 digits with leading zeros
    
    i_code.append(1)
    i_data.append(f"""{int(header['company_code']):02}{header['branch']}{header['date_prepared']}{header['supplier_code']}{header['supplier_name']}{header_total_amount}{header['project_code']}{header['voucher_type']}""")
    
    # Setup Detail
    dtl_row = 1
    for dtl in detail: 
        amount = Decimal(dtl['amount'])
        number_no_dec = int(amount * 100)
        dtl_formatted_amt = f"{number_no_dec:013}" 
        i_code.append(2)
        i_data.append(f"""{dtl_row:03}{dtl['account_code']}{dtl_formatted_amt}""")
        dtl_row += 1
        
    # Setup Particulars
    particular_row = 1
    for particular in particulars: 
        if particular_row == 1:
            i_code.append(3)
            i_data.append(f"""{particular_row:03} Qty. Unit Description Amount""")
            particular_row += 1
        
        i_code.append(3)
        i_data.append(f"""{particular_row:03} {particular['quantity']} {particular['item_description']} {format_with_commas(Decimal(particular['amount']))}""")
        
        particular_row += 1
        
        if particular_row > len(particulars) + 1: # '+ 1' is for Particular Header count
             i_code.append(3)
             i_data.append(f"""{particular_row:03} ____________""")
             i_code.append(3)
             i_data.append(f"""{(particular_row + 1):03} {format_with_commas(particulars_total_amount)}""")
             
    try:
        voucher_exists = fetch_voucher_request_by_id(voucher_request_no)
        if len(voucher_exists["data"]) > 0:
            return {
                "status": "error",
                "message": "Voucher Request No. already exists.",
                "data": {
                    "voucher_request_no": voucher_request_no,
                }
            }
            
    except ibm_db.IbmDbError as e:
        return {
            "status": "error",
            "message": f"Database error occurred: {e}",
            "data": None
        }
        
    try:
        conn = get_connection()
        query = (f"""
            INSERT INTO {schema}.VREQPF (VREQNO, CODE, DATA, TFERDT, TFERTM, REFNUM, DATDEL) VALUES
                {', '.join(['(?, ?, ?, INT(current_date), INT(current_time), ?, 0)' for _ in i_data])}
            WITH NONE""")
        
        stmt = ibm_db.prepare(conn, query)

        # Bind parameters for all rows
        param_index = 1
        row_index = 0
        for row in i_data:
            ibm_db.bind_param(stmt, param_index, voucher_request_no)
            ibm_db.bind_param(stmt, param_index + 1, i_code[row_index])
            ibm_db.bind_param(stmt, param_index + 2, row)
            ibm_db.bind_param(stmt, param_index + 3, reference_no)
            param_index += 4
            row_index += 1

        # Execute the statement
        success = ibm_db.execute(stmt)

        if success:
            num_rows = ibm_db.num_rows(stmt)
            return {
                "status": "success",
                "message": "Record added successfully.",
                "data": {
                    "rows_inserted": num_rows,
                    "data_inserted": data_list,
                }
            }
        else:
            return {
                "status": "error",
                "message": f"Database error occurred: {e}",
                "data": None
            }
        
    except ibm_db.IbmDbError as e:
        return {
            "status": "error",
            "message": f"Database error occurred: {e}",
            "data": None
        }
        
    finally:
        # Safely close the connection
        if 'conn' in locals() and conn:
            ibm_db.close(conn)
            print("Database connection closed.")

def delete_voucher_request_by_id(voucher_request_no):
    try:
        conn = get_connection()
        query = f"""
            UPDATE {schema}.vreqpf
            SET DATDEL = INT(current_date)
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
                    "message": "Record deleted successfully.",
                    "data": {
                        "rows_updated": rows_affected
                    }
                }
            else:
                return {
                    "status": "success",
                    "message": "No records were deleted. The condition did not match any rows.",
                    "data": {
                        "rows_updated": rows_affected
                    }
                }
                
        return {
            "status": "error",
            "message": "Invalid input provided.",
            "data": None,
        }
        
        # ibm_db.close(conn)
    
    except ibm_db.IbmDbError as e:
        return {
            "status": "error",
            "message": f"Database error occurred: {e}",
            "data": None
        }
        
    finally:
        # Safely close the connection
        if 'conn' in locals() and conn:
            ibm_db.close(conn)
            print("Database connection closed.")
        