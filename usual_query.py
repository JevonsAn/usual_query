from setting import tablename_to_fields, action_to_tablename, request_contain_key
from mysql import conn
from django.http import FileResponse
import time
import json
import csv
# from django.utils.six.moves import range
from django.http import StreamingHttpResponse
from django.http import HttpResponse

class Echo(object):
    """
    An object that implements just the write method of the file-like
    interface.
    """
    def write(self, value):
        """Write the value by returning it, instead of storing in a buffer."""
        return value

class Query(object):
    """docstring for Query"""

    def __init__(self):
        self.key_to_type = {v: k for k, v in request_contain_key.items()}

    def arg_parse(self, request):
        queryDict = {}
        result = {
            "page": {},
            "sort": {},
            "action": "",
            "export": {},
            "where": {}
        }
        if request.method == 'GET':
            queryDict = request.GET
        else:
            queryDict = request.POST

        for key, value in queryDict.items():
            if(self.key_to_type.get(key)):
                result[self.key_to_type.get(key)][key] = value
            else:
                result["where"][key] = value
        return result

    def get_where(self, table, query):
        fields = tablename_to_fields[table]
        sql_where = "where "
        in_conditions = []
        out_conditions = []
        others_conditions = []
        for key, value in query.items():
            if(key.find("in_out_") == 0):
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
        sql_where = self.__combination_where_condition(
            in_conditions, out_conditions, others_conditions)
        return sql_where

    def __combination_where_condition(self, in_conditions, out_conditions, others):
        sql_where = ' where '
        if(in_conditions != []):
            sql_where += "("+" and ".join(in_conditions)+") or "
            sql_where += "("+" and ".join(out_conditions)+")"
        sql_where += " and ".join(others)
        return sql_where

    def get_page(self, query):
        sql_limit = " limit "
        sql_limit += str( (int(query["pageIndex"])-1) * int(query["pageSize"]) ) + \
            "," + str(query["pageSize"])
        return sql_limit

    def get_sort(self ):
        
        return ""
    
    def get_table(self,action):
        
        return action_to_tablename[action]

    def join_sql(self ,query):
        sql = "select * from " + self.get_table(query["action"]) + self.get_where( self.get_table(query["action"]) , query["where"] ) + \
            self.get_sort() + self.get_page(query["page"])
        return sql

    def export(self, query, rows):
        def trans_dict_to_xml(data_dict):
            #字典转换为xml字符串
            xml_data = []
            for k in data_dict.keys():  # 遍历字典排序后的key
                v = data_dict.get(k)  # 取出字典中key对应的value
                xml_data.append('<{key}>{value}</{key}>'.format(key=k, value=v))
            xml = ''.join(xml_data)
            xml = '<xml>{}</xml>'.format(xml)
            return xml

        def trans_dict_to_csv(data_dict):
            """A view that streams a large CSV file."""
            # Generate a sequence of rows. The range is based on the maximum number of
            # rows that can be handled by a single sheet in most spreadsheet
            # applications.
            return data_dict

        def trans_dict_to_json(data_dict):
            json_data = json.dumps(data_dict)
            return json_data
        t = time.time()

        if("json" == query["export"]):
            data = trans_dict_to_json(rows)
            response = FileResponse(data)
            response['Content-Type'] = 'application/json'
            response['Content-Disposition'] = 'attachment;filename=' + \
                int(round(t * 1000000)) + '.json'
        if("xml" in query["export"]):
            data = trans_dict_to_xml(rows)
            response = FileResponse(data)
            response['Content-Type'] = 'application/xml'
            response['Content-Disposition'] = 'attachment;filename=' + \
                int(round(t * 1000000)) + '.xml'
        if("csv" in query["export"]):
            pseudo_buffer = Echo()
            writer = csv.writer(pseudo_buffer)
            response = StreamingHttpResponse((writer.writerow(row) for row in rows),
                                             content_type="text/csv")
            response['Content-Disposition'] = 'attachment;filename=' + \
                int(round(t * 1000000)) + '.csv'
        return response

    def search(self, request):
        http_args = self.arg_parse(request)
        sql = self.join_sql(http_args)
        conn()
        exe()
        conn.close()
        result = {
            "data": [],
            "itemcount": [],
            "time": 0
        }
        # 这个地方可以再讨论，到底是返回response还是数据。
        if("export" in http_args["export"] and http_args["export"]["export"] == True ):
            response = self.export(http_args["export"], result["data"])
        else:
            response = HttpResponse(result, content_type="application/json")
        return response
