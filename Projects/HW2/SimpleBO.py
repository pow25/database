import pymysql
import json

cnx = pymysql.connect(host='localhost',
                              user='dbuser',
                              password='dbuser',
                              db='lahman2017raw',
                              charset='utf8mb4',
                              cursorclass=pymysql.cursors.DictCursor)


def run_q(q, args, fetch=False):
    cursor = cnx.cursor()
    cursor.execute(q, args)
    if fetch:
        result = cursor.fetchall()
    else:
        result = None
    cnx.commit()
    return result

def template_to_where_clause(t):
    s = ""

    if t is None:
        return s

    for (k, v) in t.items():
        if s != "":
            s += " AND "
        s += k + "='" + v[0] + "'"

    if s != "":
        s = "WHERE " + s;

    return s


def find_by_template(table, template, fields=None):
    wc = template_to_where_clause(template)

    q = "select " + fields[0] + " from " + table + " " + wc
    result = run_q(q, None, True)
    return result





