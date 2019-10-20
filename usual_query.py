# -*- coding: utf-8 -*-
from setting import tablename_to_fields, action_to_tablename, request_contain_key
from database.operate import connector
from django.http import FileResponse
import time
import json
import csv
# from django.utils.six.moves import range
from django.http import StreamingHttpResponse
from django.http import HttpResponse
from datetime import datetime


class Echo(object):
    """
    An object that implements just the write method of the file-like
    interface.
    """

    def write(self, value):
        """Write the value by returning it, instead of storing in a buffer."""
        return value


class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.__str__()
        return json.JSONEncoder.default(self, obj)


class Query(object):
    """docstring for Query"""

    def __init__(self):
        self.key_to_type = {field: k for k, v in request_contain_key.items() for field in v}

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
            if key in {"action"}:
                result[key] = value
            elif key in self.key_to_type:
                result[self.key_to_type.get(key)][key] = value
            else:
                result["where"][key] = value
        return result

    def get_where(self, table, query):
        fields = tablename_to_fields[table]
        # sql_where = "where "
        in_conditions = []
        out_conditions = []
        others_conditions = []
        for key, value in query.items():
            if(key.find("in_out_") == 0):
                key = key[7:]
                key = tablename_to_fields[table]["transform"].get(key, key)
                if key not in fields:
                    print("fields not exists this key：", key)
                    continue
                field = fields[key]
                in_conditions.append(
                    "in_" + key + " " + field["joiner"] + " '" + value + "'")
                out_conditions.append(
                    "out_" + key + " " + field["joiner"] + " '" + value + "'")
            else:
                key = tablename_to_fields[table]["transform"].get(key, key)
                if key not in fields:
                    print("fields not exists this key：", key)
                    continue
                field = fields[key]
                if(field["type"] in ["varchar"]):
                    others_conditions.append(
                        key + " " + field["joiner"] + " '" + value + "'")
                else:
                    others_conditions.append(
                        key + " " + field["joiner"] + " " + value + "")
            # where_conditions.append("")
        sql_where = self.__combination_where_condition(
            in_conditions, out_conditions, others_conditions)
        return sql_where

    def __combination_where_condition(self, in_conditions, out_conditions, others):
        sql_where = ' where '
        in_where = ''
        out_where = ''
        other_where = ''
        all_where = ''
        if in_conditions:
            in_where = " ( " + " and ".join(in_conditions) + " ) "
            all_where += in_where
        if out_conditions:
            out_where = " ( " + " and ".join(in_conditions) + " ) "
            if all_where:
                all_where += " or "
            all_where += out_where
        if others:
            other_where = " ( " + " and ".join(others) + " ) "
            if all_where:
                all_where = " ( " + all_where + " ) " + " and " + other_where
            else:
                all_where = other_where
        if all_where:
            sql_where += all_where
        else:
            sql_where = ''
        return sql_where

    def get_page(self, query):
        sql_limit = " limit "
        sql_limit += str((int(query["pageIndex"]) - 1) * int(query["pageSize"])) + \
            "," + str(query["pageSize"])
        return sql_limit

    def get_sort(self):

        return ""

    def get_table(self, action):
        return action_to_tablename[action]

    def join_sql(self, query):
        data_sql = "select * from " + self.get_table(query["action"]) + self.get_where(self.get_table(query["action"]), query["where"]) + \
            self.get_sort() + self.get_page(query["page"]) + ";"
        count_sql = "select count(*) from " + self.get_table(query["action"]) + self.get_where(self.get_table(query["action"]), query["where"]) + ";"
        return {
            "data_sql": data_sql,
            "count_sql": count_sql,
        }

    def export(self, query, rows):
        def trans_dict_to_xml(data_dict):
            # 字典转换为xml字符串
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
        print(http_args)
        sqls = self.join_sql(http_args)
        conn = connector("edges")
        data_sql = sqls["data_sql"]
        print(data_sql)
        sql_result = conn.execute_and_fetch(data_sql)
        count_sql = sqls["count_sql"]
        print(count_sql)
        conn.close()
        print(sql_result[:1])
        result = {
            "data": list(sql_result),
            "itemcount": 1000,
            "time": 0
        }
        # 这个地方可以再讨论，到底是返回response还是数据。
        if("export" in http_args["export"] and http_args["export"]["export"] is True):
            response = self.export(http_args["export"], result["data"])
        else:
            response = HttpResponse(json.dumps(result, indent=4, cls=DateEncoder), content_type="application/json")
        return response
