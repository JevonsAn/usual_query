from setting import tablename_to_fields, action_to_tablename
from mysql import conn


class Query(object):
    """docstring for Query"""

    def __init__(self):
        pass

    def arg_parse(request):
        result = {
            "page": {},
            "sort": {},
            "action": "",
            "export": {},
            "where": {}
        }
        return result

    def get_where():
        pass

    def get_page():
        pass

    def get_sort():
        pass

    def join_sql():
        pass

    def export():
        pass

    def search(request):
        a = self.arg_parse(request)
        sql = self.join_sql(a)
        conn()
        exe
        conn.close()
        result = {
            "data": [],
            "itemcount": [],
            "time": 0
        }
        "export"
        return result
