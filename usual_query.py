from setting import tablename_to_fields, action_to_tablename, request_contain_key
from mysql import conn


class Query(object):
    """docstring for Query"""

    def __init__(self):
        self.key_to_type={v: k for k, v in request_contain_key.items()}
        

    def arg_parse(self,request):
        queryDict={}
        result = {
            "page": {},
            "sort": {},
            "action": "",
            "export": {},
            "where": {}
        }
        if request.method == 'GET':
            queryDict = request.GET
        else :
            queryDict = request.POST

        for key,value in queryDict.items():
            if(self.key_to_type.get(key)):
                result[self.key_to_type.get(key)][key]=value
            else:
                result["where"][key]=value
        return result

    def get_where(self ,table, query):
        fields = tablename_to_fields[table]
        sql_where = "where "
        in_conditions = []
        out_conditions = []
        others_conditions = []
        for key,value in query.items():
            if(key.find("in_out_")==0):
                key = key[7:]
                key = tablename_to_fields[table]["transform"].get(key, key)
                in_conditions.append(
                    "in_"+key + " " + field["joiner"] + " '"+value+"'")
                out_conditions.append(
                    "out_"+key + " " + field["joiner"] + " '"+value+"'")
            else:
                key = tablename_to_fields[table]["transform"].get(key, key)
                field = fields[key]
                if(field["type"] in ["str"]):
                    others_conditions.append(
                        key + " " + field["joiner"] + " '"+value+"'")
                else:
                    others_conditions.append(
                        key + " " + field["joiner"] + " "+value+"")
            # where_conditions.append("")
        sql_where=self.__combination_where_condition(
            in_conditions, out_conditions, others_conditions)
        return sql_where

    def __combination_where_condition(self, in_conditions, out_conditions, others):
        sql_where='where '
        if(in_conditions != []):
            sql_where += "("+" and ".join(in_conditions)+") or "
            sql_where += "("+" and ".join(out_conditions)+")"
        sql_where += " and ".join(others)
        return sql_where
    def get_page(self):
        pass

    def get_sort(self):
        pass

    def join_sql(self):
        pass

    def export(self):
        pass

    def search(self,request):
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
