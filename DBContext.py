import oracledb
from datetime import datetime, timedelta
import time
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
# import sendSMTP as sendSMTP
import configparser
import pandas as pd

class UserDefineError(Exception):
    def __init__(self, errorType, msg, procName="", params=[]):
        self.msg = msg
        self.errorType = errorType
        self.procName = procName
        self.params = params

    def __str__(self):
        return self.msg


class DBContext:
    def __init__(self):
      currentDbInfo = configparser.ConfigParser()
      currentDbInfo.read("./DBConnectionInfo.ini")

      self.user = currentDbInfo["DBConnectionInfo"]["user"]
      self.database = currentDbInfo["DBConnectionInfo"]["database"]
      self.config = configparser.ConfigParser()        
      self.config.read("./DBConnectionList.ini")
      password = self.config[self.user]["password"]
      self.con = oracledb.connect(
        user = self.user,
        password = password,
        dsn = self.config[self.user]["url"] + ":" + self.config[self.user]["port"] + "/" + self.config[self.user]["service_name"]
      )
      self.cur = self.con.cursor()

    # open, close 중복하지 않도록 하기 위함.
    def checkPing(self):
      try:
        self.con.ping()
        return True
      except:
        return False

    def open(self):
      if self.checkPing() == False:
        self.con = oracledb.connect(
            user=self.user,
            password=self.config[self.user]["password"],
            dsn=self.dsnStr,
        )
        self.con.autocommit = False
        self.cur = self.con.cursor()

    def close(self):
      if self.checkPing() == True:
        self.con.close()

    def commit(self):
      self.con.commit()

    def rollback(self):
      self.con.rollback()

    # def executeWithCommit(self,SQL):
    #     self.cur.execute(SQL)
    #     self.con.commit()

    # 프로그램 내에 쿼리문 1번만 사용할 경우
    def executeWithCon(self, SQL):
        self.open()
        self.cur.execute(SQL)
        self.con.commit()
        self.close()

    # Insert, Update, Delete문
    def execute(self, SQL):
        self.cur.execute(SQL)

    # select문 return을 tuple -> dict 형태로 변환
    def makeDictFactory(self):
        columnNames = [d[0] for d in self.cur.description]

        def createRow(*args):
            return dict(zip(columnNames, args))

        return createRow

    def makeDictFactory4SP(self, cursor):
        columnNames = [d[0] for d in cursor.description]

        def createRow(*args):
            return dict(zip(columnNames, args))

        return createRow

    # select문 return을 tuple -> dict 형태로 변환
    def select(self, SQL):
        try:
            self.cur.execute(SQL)
            self.cur.rowfactory = self.makeDictFactory()

            res = self.cur.fetchall()

            return res

        except Exception as ex:
            return ex

    # 결과값 Tuple List
    def selectTuple(self, SQL):
        try:
            self.cur.execute(SQL)

            res = self.cur.fetchall()

            return res

        except Exception as ex:
            return ex

    def selectDataFrame(self, SQL):
        try:
            res = pd.read_sql(SQL, self.con)
            return res
        except Exception as ex:
            return ex

    # procedure 컬럼 정보
    def get_args_type(self, procName, inout):

        splitByDot = procName.upper().split(".")
        inout = inout.upper()
        procName = procName.upper()

        SQL = f"""SELECT ARGUMENT_NAME ARGNM, SEQUENCE SEQ, DATA_TYPE DATATYPE, IN_OUT INOUT, '' VALUE 
                FROM ALL_ARGUMENTS 
                WHERE """

        if len(splitByDot) == 3:
            SQL += f"""UPPER(OWNER) = '{splitByDot[0]}' AND UPPER(PACKAGE_NAME) = '{splitByDot[1]}' AND UPPER(OBJECT_NAME) = '{splitByDot[2]}' 
                    AND UPPER(IN_OUT) = '{inout}'"""
        elif len(splitByDot) == 2:
            SQL += f"""UPPER(OWNER) = '{splitByDot[0]}' AND UPPER(OBJECT_NAME) = '{splitByDot[1]}'
            AND UPPER(IN_OUT) = '{inout}' 
            UNION 
            SELECT ARGUMENT_NAME ARGNM, SEQUENCE SEQ, DATA_TYPE DATATYPE, IN_OUT INOUT, '' VALUE 
            FROM ALL_ARGUMENTS 
            WHERE UPPER(OWNER) = '{self.user.upper()}' AND UPPER(PACKAGE_NAME) = '{splitByDot[0]}' AND UPPER(OBJECT_NAME) = '{splitByDot[1]}' 
            AND UPPER(IN_OUT) = '{inout}' 
            ORDER BY SEQ"""
        elif len(splitByDot) == 1:
            SQL += f"""UPPER(OWNER) = '{self.user.upper()}' AND UPPER(OBJECT_NAME) = '{procName}' 
            AND UPPER(IN_OUT) = '{inout}'"""
        else:
            raise UserDefineError(
                "db.get_args_type", "INVALID PROCEDURE(FUNCTION) CALL"
            )

        # SQL =  "SELECT ARGUMENT_NAME ARGNM, SEQUENCE SEQ, DATA_TYPE DATATYPE, IN_OUT INOUT, '' VALUE "
        # SQL += "FROM ALL_ARGUMENTS "
        # SQL += "WHERE "
        # if len(splitByDot) == 3:
        #     SQL += "UPPER(OWNER) = '" + splitByDot[0] + "' AND UPPER(PACKAGE_NAME) = '" + splitByDot[1] + "' AND UPPER(OBJECT_NAME) = '" + splitByDot[2] + "' "
        #     SQL += "AND UPPER(IN_OUT) = '" + inout.upper() + "'"
        # elif len(splitByDot) == 2:
        #     SQL += "UPPER(OWNER) = '" + splitByDot[0] + "' AND UPPER(OBJECT_NAME) = '" + splitByDot[1] + "' "
        #     SQL += "AND UPPER(IN_OUT) = '" + inout.upper() + "' "
        #     SQL += "UNION "
        #     SQL +=  "SELECT ARGUMENT_NAME ARGNM, SEQUENCE SEQ, DATA_TYPE DATATYPE, IN_OUT INOUT, '' VALUE "
        #     SQL += "FROM ALL_ARGUMENTS "
        #     SQL += "WHERE "
        #     SQL += "UPPER(OWNER) = '" + self.user.upper() + "' AND UPPER(PACKAGE_NAME) = '" + splitByDot[0] + "' AND UPPER(OBJECT_NAME) = '" + splitByDot[1] + "' "
        #     SQL += "AND UPPER(IN_OUT) = '" + inout.upper() + "' "
        #     SQL += "ORDER BY SEQ"
        # elif len(splitByDot) == 1:
        #     SQL += "UPPER(OWNER) = '" + self.user.upper() + "' AND UPPER(OBJECT_NAME) = '" + procName.upper() + "' "
        #     SQL += "AND UPPER(IN_OUT) = '" + inout.upper() + "'"
        # else:
        #     raise UserDefineError("INVALID PROCEDURE(FUNCTION) CALL")

        # SQL =  "SELECT ARGUMENT_NAME ARGNM, SEQUENCE SEQ, DATA_TYPE DATATYPE, IN_OUT INOUT, '' VALUE "
        # SQL += "FROM ALL_ARGUMENTS "
        # SQL += "where owner || '.' || nvl2(package_name,package_name || '.' ,'') || object_name like upper('%" + procName + "%')"
        # SQL += "and owner = '" + self.user.upper() + "' and in_out = '" + inout + "'"
        res = self.select(SQL)
        # inParams = dict()
        # outParams = dict()
        # for row in res:
        #     if row['INOUT'] == 'IN':
        #         inParams[row['ARGNM']] = row['DATATYPE']
        #     else:
        #         inParams[row['ARGNM']] = row['DATATYPE']
        #         # outParams[row['ARGNM']] = row['DATATYPE']
        return res

    def get_args_type_df(self, procName, inout):

        splitByDot = procName.upper().split(".")
        inout = inout.upper()
        procName = procName.upper()

        SQL = f"""SELECT ARGUMENT_NAME ARGNM, SEQUENCE SEQ, DATA_TYPE DATATYPE, IN_OUT INOUT, '' VALUE 
                FROM ALL_ARGUMENTS 
                WHERE """

        if len(splitByDot) == 3:
            SQL += f"""UPPER(OWNER) = '{splitByDot[0]}' AND UPPER(PACKAGE_NAME) = '{splitByDot[1]}' AND UPPER(OBJECT_NAME) = '{splitByDot[2]}' 
                    AND UPPER(IN_OUT) = '{inout}'"""
        elif len(splitByDot) == 2:
            SQL += f"""UPPER(OWNER) = '{splitByDot[0]}' AND UPPER(OBJECT_NAME) = '{splitByDot[1]}'
            AND UPPER(IN_OUT) = '{inout}' 
            UNION 
            SELECT ARGUMENT_NAME ARGNM, SEQUENCE SEQ, DATA_TYPE DATATYPE, IN_OUT INOUT, '' VALUE 
            FROM ALL_ARGUMENTS 
            WHERE UPPER(OWNER) = '{self.user.upper()}' AND UPPER(PACKAGE_NAME) = '{splitByDot[0]}' AND UPPER(OBJECT_NAME) = '{splitByDot[1]}' 
            AND UPPER(IN_OUT) = '{inout}' 
            ORDER BY SEQ"""
        elif len(splitByDot) == 1:
            SQL += f"""UPPER(OWNER) = '{self.user.upper()}' AND UPPER(OBJECT_NAME) = '{procName}' 
            AND UPPER(IN_OUT) = '{inout}'"""
        else:
            raise UserDefineError(
                "db.get_args_type", "INVALID PROCEDURE(FUNCTION) CALL"
            )

        # SQL =  "SELECT ARGUMENT_NAME ARGNM, SEQUENCE SEQ, DATA_TYPE DATATYPE, IN_OUT INOUT, '' VALUE "
        # SQL += "FROM ALL_ARGUMENTS "
        # SQL += "WHERE "
        # if len(splitByDot) == 3:
        #     SQL += "UPPER(OWNER) = '" + splitByDot[0] + "' AND UPPER(PACKAGE_NAME) = '" + splitByDot[1] + "' AND UPPER(OBJECT_NAME) = '" + splitByDot[2] + "' "
        #     SQL += "AND UPPER(IN_OUT) = '" + inout.upper() + "'"
        # elif len(splitByDot) == 2:
        #     SQL += "UPPER(OWNER) = '" + splitByDot[0] + "' AND UPPER(OBJECT_NAME) = '" + splitByDot[1] + "' "
        #     SQL += "AND UPPER(IN_OUT) = '" + inout.upper() + "' "
        #     SQL += "UNION "
        #     SQL +=  "SELECT ARGUMENT_NAME ARGNM, SEQUENCE SEQ, DATA_TYPE DATATYPE, IN_OUT INOUT, '' VALUE "
        #     SQL += "FROM ALL_ARGUMENTS "
        #     SQL += "WHERE "
        #     SQL += "UPPER(OWNER) = '" + self.user.upper() + "' AND UPPER(PACKAGE_NAME) = '" + splitByDot[0] + "' AND UPPER(OBJECT_NAME) = '" + splitByDot[1] + "' "
        #     SQL += "AND UPPER(IN_OUT) = '" + inout.upper() + "' "
        #     SQL += "ORDER BY SEQ"
        # elif len(splitByDot) == 1:
        #     SQL += "UPPER(OWNER) = '" + self.user.upper() + "' AND UPPER(OBJECT_NAME) = '" + procName.upper() + "' "
        #     SQL += "AND UPPER(IN_OUT) = '" + inout.upper() + "'"
        # else:
        #     raise UserDefineError("INVALID PROCEDURE(FUNCTION) CALL")

        # SQL =  "SELECT ARGUMENT_NAME ARGNM, SEQUENCE SEQ, DATA_TYPE DATATYPE, IN_OUT INOUT, '' VALUE "
        # SQL += "FROM ALL_ARGUMENTS "
        # SQL += "where owner || '.' || nvl2(package_name,package_name || '.' ,'') || object_name like upper('%" + procName + "%')"
        # SQL += "and owner = '" + self.user.upper() + "' and in_out = '" + inout + "'"
        res = self.selectDataFrame(SQL)
        # inParams = dict()
        # outParams = dict()
        # for row in res:
        #     if row['INOUT'] == 'IN':
        #         inParams[row['ARGNM']] = row['DATATYPE']
        #     else:
        #         inParams[row['ARGNM']] = row['DATATYPE']
        #         # outParams[row['ARGNM']] = row['DATATYPE']
        return res

    # return 없는 procedure
    def call_procedure(self, SQL, param):
        try:

            self.cur.callproc(SQL, param)

        except Exception as ex:
            print("에러 : ", ex)

    # 새로 개발한 call proc
    def call_proc(self, procName, inParamsValue):
        inparams = self.get_args_type(procName, "IN")
        # if len(inParamsValue) != 0 and len(inparams) == 0:
        #     raise UserDefineError(f"""INVALID PROCEDURE(FUNCTION) OR NEED TO CHECK GRANT
        #                             procName : {procName}
        #                             param : {inParamsValue}""")
        # if len(inParamsValue) != len(inparams):
        #     raise UserDefineError(f"""CHECK PROCEDURE(FUNCTION)'s Parameter
        #                             procName : {procName}
        #                             param : {inParamsValue}""")
        outparams = self.get_args_type(procName, "OUT")

        outParamsType = []
        for row in outparams:
            dataType = row["DATATYPE"]
            if dataType == "VARCHAR2":
                cxType = oracledb.STRING
            elif dataType == "REF CURSOR":
                cxType = oracledb.CURSOR
            elif dataType == "CLOB":
                cxType = oracledb.CLOB
            elif dataType == "NUMBER":
                cxType = oracledb.NUMBER
            elif dataType == "CHAR":
                cxType = oracledb.CHAR

            outParamsType.append(self.cur.var(cxType))

        fparam = inParamsValue + outParamsType

        self.cur.callproc(procName, fparam)

        res = []
        for fIdx in range(len(inParamsValue), len(fparam)):
            resValue = fparam[fIdx].getvalue()
            resValue.rowfactory = self.makeDictFactory4SP(resValue)
            res.append(resValue.fetchall())

        return res

    # # 새로 개발한 call proc
    # def call_proc(self, procName, inParamsValue):
    #     inparams = self.get_args_type(procName, "IN")
    #     # if len(inParamsValue) != 0 and len(inparams) == 0:
    #     #     raise UserDefineError(f"""INVALID PROCEDURE(FUNCTION) OR NEED TO CHECK GRANT
    #     #                             procName : {procName}
    #     #                             param : {inParamsValue}""")
    #     # if len(inParamsValue) != len(inparams):
    #     #     raise UserDefineError(f"""CHECK PROCEDURE(FUNCTION)'s Parameter
    #     #                             procName : {procName}
    #     #                             param : {inParamsValue}""")
    #     outparams = self.get_args_type(procName, "OUT")

    #     outParamsType = []
    #     clobIndices = []  # CLOB 데이터가 있는 인덱스를 저장할 리스트

    #     for idx, row in enumerate(outparams):  # idx 변수를 사용하여 인덱스 추적
    #         dataType = row["DATATYPE"]
    #         if dataType == "VARCHAR2":
    #             cxType = cx_Oracle.STRING
    #         elif dataType == "REF CURSOR":
    #             cxType = cx_Oracle.CURSOR
    #         elif dataType == "CLOB":
    #             cxType = cx_Oracle.CLOB
    #             clobIndices.append(len(inParamsValue) + idx)  # CLOB 데이터가 있는 인덱스 추가
    #         elif dataType == "NUMBER":
    #             cxType = cx_Oracle.NUMBER
    #         elif dataType == "CHAR":
    #             cxType = cx_Oracle.CHAR

    #         outParamsType.append(self.cur.var(cxType))
    #     fparam = inParamsValue + outParamsType  # 원본
    #     self.cur.callproc(procName, fparam)  # 원본

    #     res = []
    #     for fIdx in range(len(inParamsValue), len(fparam)):
    #         if fIdx in clobIndices:  # CLOB 데이터 처리
    #             clob_obj = fparam[fIdx]  # cx_Oracle.LOB 객체 생성
    #             resValue = clob_obj.read()  # CLOB 데이터 읽기
    #         else:
    #             resValue = fparam[fIdx]

    #         res.append(resValue)

    #     return res

    # 기존 호선 코드
    # res = []
    # for fIdx in range(len(inParamsValue), len(fparam)):
    #     resValue = fparam[fIdx].getvalue()
    #     resValue.rowfactory = self.makeDictFactory4SP(resValue)
    #     res.append(resValue.fetchall())

    # return res

    # res = []
    # for fIdx in range(len(inParamsValue), len(fparam)):
    #     # resValue = fparam[fIdx].getvalue()
    #     resValue = (
    #         fparam[fIdx].getvalue()
    #         if isinstance(fparam[fIdx], cx_Oracle.LOB)
    #         else fparam[fIdx]
    #     )

    #     if isinstance(resValue, cx_Oracle.LOB):  # CLOB 데이터 처리
    #         resValueData = ""
    #         chunk_size = 4096  # 조절 가능한 청크 크기
    #         chunk = resValue.read(chunk_size)
    #         while chunk:
    #             resValueData += chunk.decode("utf-8")
    #             chunk = resValue.read(chunk_size)
    #         resValue = resValueData

    #     # resValue.rowfactory = self.makeDictFactory4SP(resValue)  # 수정 필요
    #     res.append(resValue)  # 수정된 부분

    # return res

    # res = []
    # for fIdx in range(len(inParamsValue), len(fparam)):
    #     resValue = fparam[fIdx]

    #     if isinstance(resValue, cx_Oracle.Var):
    #         resValue = resValue.getvalue()

    #         if isinstance(resValue, cx_Oracle.LOB):
    #             resValue = self.handle_lob(resValue)

    #         if isinstance(resValue, tuple):
    #             resValue = tuple(
    #                 v.getvalue() if isinstance(v, cx_Oracle.LOB) else v
    #                 for v in resValue
    #             )
    #             resValue = resValue[0] if len(resValue) > 0 else None

    #     res.append(resValue)

    # return res

    # res = []
    # for fIdx in range(len(inParamsValue), len(fparam)):
    #     resValue = fparam[fIdx]

    #     if isinstance(resValue, cx_Oracle.LOB):  # cx_Oracle.LOB 여기서 처리
    #         resValue = self.handle_lob(resValue)
    #     elif isinstance(resValue, cx_Oracle.Var):  # cx_Oracle.Var인 경우 getvalue() 호출
    #         resValue = resValue.getvalue()
    #     elif isinstance(
    #         resValue, cx_Oracle.Cursor
    #     ):  # cx_Oracle.Cursor인 경우 fetchone() 호출
    #         resValue = resValue.fetchone()
    #         resValue = resValue[0] if resValue else None

    #     print(f"resValue: {resValue}")  # 수정된 부분

    #     res.append(resValue)

    # return res

    # res = []
    # for fIdx in range(len(inParamsValue), len(fparam)):
    #     # resValue = fparam[fIdx].getvalue()
    #     resValue = fparam[fIdx]
    #     if isinstance(
    #         resValue, cx_Oracle.LOB
    #     ):  # cx_Oracle.CLOB 객체는 cx_Oracle.LOB 클래스를 상속받음
    #         try:  # CLOB 데이터 읽을 때 무한로딩 현상이 발생하여 추가 - 2023.07.07 Joyh
    #             temp = resValue.read(1024)  # 한번에 1024 바이트 씩 읽어옴
    #             clob_data = []
    #             while temp:
    #                 clob_data.append(temp)
    #                 temp = resValue.read(1024)
    #             resValue = "".join(clob_data)
    #             # # CLOB 데이터를 문자열로 변환하여 반환
    #             # resValue = resValue.read()
    #         except cx_Oracle.DatabaseError:
    #             # CLOB 데이터 읽기에 실패한 경우 또는 None인 경우
    #             resValue = None
    #         if resValue is not None:
    #             if isinstance(resValue, cx_Oracle.LOB):  # CLOB type 에러 방지
    #                 resValue = resValue.getvalue()  # cx_Oracle.LOB 객체를 문자열로 변환

    #     if isinstance(resValue, cx_Oracle.LOB):
    #         # cx_Oracle.LOB 여기서 처리
    #         resValue = self.handle_lob(resValue)

    #     # resValue가 cx_Oracle.LOB 객체인 경우에만 rowfactory를 설정하는 부분을 수정
    #     else:  #  resValue가 cx_Oracle.LOB가 아닌 경우 resValue를 리스트로 변환하여 저장
    #         resValue = resValue.fetchall()
    #         # resValue.rowfactory = self.makeDictFactory4SP(resValue)
    #     res.append(resValue)
    #     # res.append(resValue.fetchall())

    # return res

    def handle_lob(self, lob):
        if isinstance(lob, oracledb.CLOB):
            return lob.read().decode("utf-8")
        elif isinstance(lob, oracledb.BLOB):
            return lob.read()
        else:
            return None

    # for idx in range(len(inParamsName)+len(outParamsName)):
    #     argnm = params[]
    #     datatype = paramRow['DATATYPE']
    #     inout = paramRow['INOUT']
    #     if inout == 'IN':
    #         fparam.append(argnm)

    # res = self.cur.callproc(procName,fparam)
    # for inPrams

    # self.cur.callproc(SQL,param)

    # member 이름 or Key 값   대문자로 했을 때 동작한다.
    def call_proc_obj(self, procName, obj):
        inparams = self.get_args_type_df(procName, "IN")
        # if len(inParamsValue) != 0 and len(inparams) == 0:
        #     raise UserDefineError(f"""INVALID PROCEDURE(FUNCTION) OR NEED TO CHECK GRANT
        #                             procName : {procName}
        #                             param : {inParamsValue}""")
        # if len(inParamsValue) != len(inparams):
        #     raise UserDefineError(f"""CHECK PROCEDURE(FUNCTION)'s Parameter
        #                             procName : {procName}
        #                             param : {inParamsValue}""")
        outparams = self.get_args_type(procName, "OUT")

        outParamsType = []
        for row in outparams:
            dataType = row["DATATYPE"]
            if dataType == "VARCHAR2":
                cxType = oracledb.STRING
            elif dataType == "REF CURSOR":
                cxType = oracledb.CURSOR
            elif dataType == "CLOB":
                cxType = oracledb.CLOB
            elif dataType == "NUMBER":
                cxType = oracledb.NUMBER
            elif dataType == "CHAR":
                cxType = oracledb.CHAR
            outParamsType.append(self.cur.var(cxType))

        inParamsValue = []
        if type(obj) == dict:
            for argNm in inparams["ARGNM"]:
                inParamsValue.append(obj.get(argNm.lower()))
        else:
            for argNm in inparams["ARGNM"]:
                inParamsValue.append(getattr(obj, argNm.lower(), None))

        fparam = inParamsValue + outParamsType

        self.cur.callproc(procName, fparam)

        res = []
        for fIdx in range(len(inParamsValue), len(fparam)):
            resValue = fparam[fIdx].getvalue()
            resValue.rowfactory = self.makeDictFactory4SP(resValue)
            res.append(resValue.fetchall())

        return res

        # for idx in range(len(inParamsName)+len(outParamsName)):
        #     argnm = params[]
        #     datatype = paramRow['DATATYPE']
        #     inout = paramRow['INOUT']
        #     if inout == 'IN':
        #         fparam.append(argnm)

        # res = self.cur.callproc(procName,fparam)
        # for inPrams

        # self.cur.callproc(SQL,param)

    # dict []를 cursor 형태로 변환 (oracle In Ref Cursor 사용하기 위함)
    def make_temp(self, param):
        SQL = ""
        i = 0
        for p in param:
            j = 0
            SQL += " SELECT '"
            for k in p.keys():
                SQL += p[k] + "' " + k
                if j < len(p) - 1:
                    SQL += ", '"
                j = j + 1
            SQL += " FROM DUAL "
            if i < len(param) - 1:
                SQL += " UNION "
            i = i + 1
        self.cur.execute(SQL)
        res = self.cur
        return res

    def insertquery(self, tableName, object_):
        # key error인 경우 에러메세지 return 해야 함.
        SQL = (
            "SELECT COLUMN_NAME, DATA_TYPE FROM COLS WHERE TABLE_NAME = UPPER('"
            + tableName.upper()
            + "') order by column_id"
        )
        column = self.select(SQL)
        SQL = "INSERT INTO " + tableName + "("
        firstColumnTag = True
        for c in column:
            if c["COLUMN_NAME"] in object_.__dict__:
                if object_.__dict__[c["COLUMN_NAME"]] != None:
                    if firstColumnTag == True:
                        SQL += c["COLUMN_NAME"]
                        firstColumnTag = False
                    else:
                        SQL += ", " + c["COLUMN_NAME"]
        SQL += ") VALUES("
        firstColumnTag = True
        for c in column:
            if c["COLUMN_NAME"] in object_.__dict__:
                if object_.__dict__[c["COLUMN_NAME"]] != None:
                    if c["DATA_TYPE"] == "VARCHAR2":
                        if firstColumnTag == True:
                            SQL += (
                                "'"
                                + str(object_.__dict__[c["COLUMN_NAME"]]).replace(
                                    "'", "''"
                                )
                                + "'"
                            )
                            firstColumnTag = False
                        else:
                            SQL += (
                                ", '"
                                + str(object_.__dict__[c["COLUMN_NAME"]]).replace(
                                    "'", "''"
                                )
                                + "'"
                            )
                    if c["DATA_TYPE"] == "NUMBER":
                        if firstColumnTag == True:
                            SQL += str(object_.__dict__[c["COLUMN_NAME"]])
                            firstColumnTag = False
                        else:
                            SQL += ", " + str(object_.__dict__[c["COLUMN_NAME"]])
                    if c["DATA_TYPE"] == "CLOB":
                        if firstColumnTag == True:
                            # if len(str(object_.__dict__[c["COLUMN_NAME"]])) > 4000:
                            for i in range(
                                0,
                                len(
                                    str(object_.__dict__[c["COLUMN_NAME"]]).replace(
                                        "'", "''"
                                    )
                                ),
                                4000,
                            ):
                                SQL += (
                                    "TO_CLOB('"
                                    + str(
                                        object_.__dict__[c["COLUMN_NAME"]][i : i + 4000]
                                    ).replace("'", "''")
                                    + "') || "
                                )
                            SQL = SQL[:-4]
                            # else:
                        else:
                            SQL += ", "
                            if len(str(object_.__dict__[c["COLUMN_NAME"]])) == 0:
                                SQL += "''"
                                continue
                            for i in range(
                                0,
                                len(
                                    str(object_.__dict__[c["COLUMN_NAME"]]).replace(
                                        "'", "''"
                                    )
                                ),
                                4000,
                            ):
                                SQL += (
                                    "TO_CLOB('"
                                    + str(
                                        object_.__dict__[c["COLUMN_NAME"]][i : i + 4000]
                                    ).replace("'", "''")
                                    + "') || "
                                )
                            SQL = SQL[:-4]

        SQL += ")"
        self.execute(SQL)