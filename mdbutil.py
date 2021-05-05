#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
author    : Bilery Zoo(bilery.zoo@gmail.com)
create_ts : 2020-01-01
program   : *_* MySQL handle utility *_*
"""


# import os
import sys
from lib import logutil
from lib import baseutil

logger = logutil.LOG().formatted_logger()
# logger = logutil.LOG(filename=os.path.dirname(os.path.abspath(__file__)) + "/log").logger()

c_flag = False

try:
    import _mysql_connector
except ImportError:
    logger.warning('Import "_mysql_connector" failed, fall back to strictly use "mysql.connector"...')
else:
    c_flag = True
finally:
    import mysql.connector

DBException = _mysql_connector.MySQLInterfaceError if c_flag else mysql.connector.errors.Error


class MDB(object):
    def __init__(self, use_c_api=False, charset="utf8", use_unicode=False, is_utf8mb4=False, autocommit=False, **kwargs):
        self.use_c_api = use_c_api
        self.charset = charset
        self.use_unicode = use_unicode
        self.is_utf8mb4 = is_utf8mb4
        self.autocommit = autocommit
        self.kwargs = kwargs

        self.con = self.mdb_con()

    def __enter__(self):
        return self.con

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.con.close()

    def mdb_con(self):
        """
        Get MySQL connection.
        """
        if self.use_c_api and c_flag:
            con = _mysql_connector.MySQL()
            con.connect(**self.kwargs)
            con.set_character_set(self.charset)
            con.use_unicode(self.use_unicode)
            con.autocommit(self.autocommit)
            charset = "utf8mb4" if self.is_utf8mb4 else self.charset
            con.query("SET NAMES {charset};".format(charset=charset))
            con.query("SET CHARACTER SET {charset};".format(charset=charset))
            con.query("SET character_set_connection={charset};".format(charset=charset))
            con.commit()
            return con
        if self.use_c_api and not c_flag:
            logger.warning('Get "_mysql_connector" failed, fall back to strictly use "mysql.connector"...')
        return mysql.connector.connect(charset=self.charset, use_unicode=self.use_unicode, autocommit=self.autocommit,
                                       **self.kwargs)


def generate_insert(table, items, database='', is_escape_string=False, con=None, charset="utf-8"):
    """
    Generate INSERT statement of SQL DML.
    """
    destination = "`%s`.`%s`" % (database, table) if database else "`%s`" % table
    sql_l = "INSERT INTO %s (" % destination
    sql_r = ") VALUES ("
    for column in items:
        data = items[column]
        if data == 0 or data:
            if is_escape_string:
                assert c_flag and con
                data = con.escape_string(str(data)).decode(charset)
            sql_l += "`{key}`, ".format(key=column)
            sql_r += "'{value}', ".format(value=data)
    sql = sql_l[0:-2] + sql_r[0:-2] + ");"
    return sql

# def generate_insert_sub(_key_list):
#     statement_l = '('
#     statement_r = '('
#     for _ in _key_list:
#         statement_l = statement_l + '`' + _ + "`, "
#         statement_r = statement_r + "'%s', "
#     return statement_l[:-2] + ") VALUES " + statement_r[:-2] + ')'

def generate_insert_sub(_key_list, _value_list):
    statement_l = '('
    statement_r = '('
    for (_, __) in zip(_key_list, _value_list):
        sub = "'" + __ + "', " if __ is not None else "NULL, "
        statement_l = statement_l + '`' + _ + "`, "
        statement_r = statement_r + sub
    return statement_l[:-2] + ") VALUES " + statement_r[:-2] + ')'

def generate_update_set(_key_list, _value_list):
    statement = 'SET '
    for (_, __) in zip(_key_list, _value_list):
        sub = "'" + __ + "', " if __ is not None else "NULL, "
        statement = statement + "`" + _ + "` = " + sub
    return statement[:-2]

def generate_where(items, alias=''):
    """
    Generate WHERE statement of SQL.
    """
    alias += '.' if alias else ''
    statement = "WHERE"
    for column in items:
        statement += " {alias}`{column}` {value} AND".format(alias=alias, column=column, value=items[column])
    return statement[:-4]

def generate_group_by(columns, alias=''):
    """
    Generate GROUP BY statement of SQL.
    """
    alias += '.' if alias else ''
    statement = "GROUP BY"
    for column in columns:
        statement += " {alias}`{column}`,".format(alias=alias, column=column)
    return statement[:-1]

# @logutil.Log.log(logger=logger)
def execute_sql_quiet(con, sql, use_c_api=False, is_commit=True, is_count=False, is_close=False, is_exit=False,
                      is_raise=True, is_info=False):
    """
    Execute SQL(DDL, DML, DCL etc) in quiet mode(with no return).
    """
    cur = con.cursor() if not use_c_api else None
    try:
        if use_c_api: con.query(sql)
        else: cur.execute(sql)
    except DBException as E:
        con.rollback()
        if is_exit: sys.exit(E)
        if is_raise: raise
    else:
        cnt = con.affected_rows() if use_c_api else cur.rowcount
        if is_commit: con.commit()
        if is_count: return cnt
    finally:
        if is_close:
            if not use_c_api: cur.close()
            con.close()
        if is_info:
            logger.info(baseutil.combine_lines_str(sql))

# @logutil.Log.log(logger=logger)
def execute_sql_return(con, sql, use_c_api=False, dictionary=True, is_free=True, is_close=False, is_exit=False, is_raise=True,
                       is_info=False, **kwargs):
    """
    Execute SQL(DQL) in return mode(with return).
    """
    cur = con.cursor(dictionary=dictionary, **kwargs) if not use_c_api else None
    try:
        if use_c_api:
            con.query(sql)
        else:
            cur.execute(sql)
    except DBException as E:
        con.rollback()
        if is_exit:
            sys.exit(E)
        if is_raise:
            raise
    else:
        if use_c_api:
            column_list = []
            if dictionary:
                columns = con.fetch_fields()
                for column in columns:
                    column_list.append(column[4])
            row_tuple = con.fetch_row()
            while row_tuple:
                if dictionary:
                    row_zip = zip(column_list, row_tuple)
                    row = {}
                    for sub in row_zip:
                        row[sub[0]] = sub[1]
                    yield row
                else:
                    yield row_tuple
                row_tuple = con.fetch_row()
        else:
            for row in cur:
                if dictionary:
                    baseutil.str_dict_value(row)
                    yield baseutil.str_dict_key(row)
                else:
                    yield row
    finally:
        if is_free:
            if use_c_api: con.free_result()
            else: cur.close()
        if is_close:
            if use_c_api: con.free_result()
            else: cur.close()
            con.close()
        if is_info:
            logger.info(baseutil.combine_lines_str(sql))

# @logutil.Log.log(logger=logger)
def check_dql_existence(con, sql, use_c_api=False, is_exit=False, is_raise=True, is_free=True, is_close=False, is_info=False):
    """
    Check whether SQL(DQL) query has result to return or not.
    """
    cur = con.cursor(raw=True) if not use_c_api else None
    try:
        if use_c_api:
            con.raw(True)
            con.query(sql)
        else:
            cur.execute(sql)
    except DBException as E:
        con.rollback()
        if is_exit: sys.exit(E)
        if is_raise: raise
    else:
        if use_c_api: return True if con.fetch_row() else False
        else: return True if cur.fetchone() else False
    finally:
        if is_free:
            if use_c_api: con.free_result()
            else: cur.close()
        if is_close:
            if use_c_api: con.free_result()
            else: cur.close()
            con.close()
        if is_info: logger.info(baseutil.combine_lines_str(sql))


if __name__ == "__main__":
    CON = {
        "con": {
            "host": "localhost",
            "port": 3306,
            "user": "root",
            "password": "1024",
            "database": "information_schema",
        },
        "charset": "utf8",
        "use_unicode": True,
        "autocommit": False,
    }
    con_c = MDB(**CON["con"]).mdb_con()
    # con_p = MDB(use_c_api=False, **CON["con"]).mdb_con()
    # print(con_c)
    # items = {
    #     "col1": "= 1",
    #     "col2": "> 2",
    # }
    # print(generate_insert(table="tab", database="dbs", items=items))
    # print(generate_where(items, "_tmp"))
    # print(generate_group_by(items.keys(), "_tmp"))
    # print(execute_sql_quiet(con_c, "CREATE DATABASE `mdbutil`;"))
    # print(execute_sql_quiet(con_p, "DROP DATABASE `mdbutil`;", use_c_api=False))
    sql_t = 'SELECT `TABLE_NAME` FROM `information_schema`.`TABLES` LIMIT 2;'
    sql_f = 'SELECT `TABLE_NAME`, `CREATE_TIME` FROM `information_schema`.`TABLES` WHERE `TABLE_NAME` = "I" LIMIT 2;'
    # print(check_dql_existence(con_p, sql_f, use_c_api=False))
    # print(check_dql_existence(con_c, sql_t))
    # for r in execute_sql_return(con_p, sql_t, use_c_api=False, is_info=False, dictionary=True):
    #     print(r)
    # for r in execute_sql_return(con_c, sql_t, use_c_api=False, is_info=False, dictionary=False):
    #     print(r)
    # print(execute_sql_return(con_c, sql_f, use_c_api=False, is_info=False, dictionary=False).next())
    print(generate_update_set(['a', 'b'], ['a', None]))
    print(generate_insert_sub(['a', 'b'], ['b', None]))
