
-- DROP TABLE JBLIB.TRNRFPF;
CREATE OR REPLACE TABLE JBLIB.VFL_API (
  
  VREQNO CHAR(12) NOT NULL,
  VRDTL CLOB(1048576) NOT NULL,
  VRSTAT CHAR(10),
  PRIMARY KEY (VREQNO)
);

/*
  FIRST FILE
*/
INSERT INTO JBLIB.VFL1PF VALUES(
  'VR0100000000', 'C', 1, 1, 0 , 0, 0, '', 0, 0, 0, 0, 'TA04',
  'T.C. MEGAKONSTRUK AND TRADING CORP.', '', 735069.08, 0, 0, 0,
  0, 0, '', 0, '', '', 0) 
WITH NONE;

/*
  SECOND FILE
*/
INSERT INTO JBLIB.VFL2PF VALUES
  ('VR0100000000', 'C', 1, 1, 0, 0, 0, '', 0, 1, '1044C740014456', 170374.05, 0,
    0, '', '', 0, '', 0),
  ('VR0100000000', 'C', 1, 1, 0, 0, 0, '', 0, 2, '1044C740014462', 71928.38, 0,
    0, '', '', 0, '', 0),
  ('VR0100000000', 'C', 1, 1, 0, 0, 0, '', 0, 3, '1044C740014463', 80063.4, 0,
    0, '', '', 0, '', 0),
  ('VR0100000000', 'C', 1, 1, 0, 0, 0, '', 0, 4, '1044C740014464', 412703.25, 0,
    0, '', '', 0, '', 0)
WITH NONE;

/*
  THIRD FILE
*/
INSERT INTO JBLIB.VPARPF VALUES
  ('VR0100000000', 'C', 1, 1, 0, 0, 0, '', 0, 1, 'Qty. Unit Description Amount'),
  ('VR0100000000', 'C', 1, 1, 0, 0, 0, '', 0, 2, '8 LEN C.I. PIPES 200MM 80,063.40'),
  ('VR0100000000', 'C', 1, 1, 0, 0, 0, '', 0, 3, '5 PCS CI PIPES 250 MM( 71,928.38'),
  ('VR0100000000', 'C', 1, 1, 0, 0, 0, '', 0, 4, '30 PCS C.I. PIPE 150MM 184,792.50'),
  ('VR0100000000', 'C', 1, 1, 0, 0, 0, '', 0, 5, '37 PCS C.I. PIPE 150MM 227,910.75'),
  ('VR0100000000', 'C', 1, 1, 0, 0, 0, '', 0, 6, '7 PCS CI PIPES 300MM X 170,374.05'),
  ('VR0100000000', 'C', 1, 1, 0, 0, 0, '', 0, 7, '____________'),
  ('VR0100000000', 'C', 1, 1, 0, 0, 0, '', 0, 8, '735,069.08')
WITH NONE;

/*
  FOURTH FILE
*/
INSERT INTO JBLIB.VFL_API VALUES
  ('VR0100000000', '
    {
      "voucher": {
        "prs_username": "test_user1",
        "voucher_request_no": "VR0100000000",
        "branch_code": "1",
        "date_prepared": "20250408",
        "time_prepared": "151836",
        "supplier": {
          "code": "TA04",
          "name": "T.C. MEGAKONSTRUK AND TRADING CORP.",
          "tin": "233-561-302"
        },
        "total_amount": 735,069.08,
        "project_code": "C74",
        "lines": [
          {
            "account_code": "1044C740014456",
            "amount": 170374.05,
            "items": [
              {
                "quantity": 7,
                "unit": "PCS",
                "description": "CI PIPES 300MM X",
                "amount": 170374.05
              }
            ]
          },
          {
            "account_code": "1044C740014462",
            "amount": 71928.38,
            "items": [
              {
                "quantity": 5,
                "unit": "PCS",
                "description": "CI PIPES 250 MM(",
                "amount": 71928.38
              }
            ]
          },
          {
            "account_code": "1044C740014463",
            "amount": 80063.4,
            "items": [
              {
                "quantity": 8,
                "unit": "LEN",
                "description": "C.I. PIPES 200MM",
                "amount": 80063.40
              }
            ]
          },
          {
            "account_code": "1044C740014464",
            "amount": 412703.25,
            "items": [
              {
                "quantity": 30,
                "unit": "PCS",
                "description": "C.I. PIPE 150MM",
                "amount": 184792.50
              },
              {
                "quantity": 37,
                "unit": "PCS",
                "description": "C.I. PIPE 150MM",
                "amount": 227910.75
              },
            ]
          },
        ]
      }
    }
  ', '')
  WITH NONE;

SELECT 
    VREQNO VOUCHER_REQUEST_NO,
    VRDTL VOUCHER_REQUEST_DETAIL,
    trim(VRSTAT) VOUCHER_REQUEST_STATUS
FROM JBLIB.VFL_API;

/*
  IT LOG FILE (FIFTH FILE)
*/

INSERT INTO JBLIB.ITLOGPF VALUES (
  'test_user1', INT(CURRENT_DATE), INT(CURRENT_TIME), 'VFL_API', 'ADD',
  'VR0100000000', 'RECORD ADDED FROM PRS WEB APP', 'THRU IBM i API'
) WITH NONE;

/*
  CANCEL VOUCHER REQUEST
*/

UPDATE JBLIB.VFL_API
SET VRSTAT = 'CANCELLED'
WHERE VREQNO = 'VR0100000007'
WITH NONE;


/*
  TEST
*/

SELECT COLUMN_NAME, DATA_TYPE, LENGTH, NUMERIC_SCALE, IS_NULLABLE
FROM QSYS2.SYSCOLUMNS
WHERE TABLE_NAME = 'Vfl2PF' AND TABLE_SCHEMA = 'DBRLIB';

SELECT * FROM JBLIB.VFL2PF 
WHERE VREQNO = 'VR0100000000'
ORDER BY VREQNO DESC;


SELECT * FROM DBRLIB.ITLOGPF
ORDER BY DATACS DESC;
WHERE VREQNO = '2025-03-0249';


;


SELECT * FROM JBLIB.Vfl1PF
WHERE VREQNO = 'VR0100000006';

SELECT * FROM JBLIB.VFL2PF
-- WHERE ACCTCD LIKE '1044C740014456';
WHERE VREQNO = 'VR0100000006';

SELECT * FROM JBLIB.VPARPF
WHERE VREQNO = 'VR0100000006';
WHERE VREQNO = '2025-03-0266';

SELECT * FROM JBLIB.VFL_API
WHERE VREQNO = 'VR0100000007';

SELECT * FROM JBLIB.ITLOGPF
WHERE RMARK1 = 'VR0100000006';

SELECT 
  I.JSNDTA
  -- JSON_QUERY(I.JSNDTA, 'lax $.author')
FROM JBLIB.prpslpf I
WHERE PRPLNO = 1000;
