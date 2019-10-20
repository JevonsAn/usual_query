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


class CJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime("%Y-%m-%d")
        else:
            return json.JSONEncoder.default(self, obj)


class Query(object):
    """docstring for Query"""

    def __init__(self):
        self.key_to_type = {field: k for k,
                            v in request_contain_key.items() for field in v}

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

        fields = tablename_to_fields[table]["fields"]
        print("fields:\n", fields)
        # sql_where = "where "
        in_conditions = []
        out_conditions = []
        others_conditions = []
        for key, value in query.items():
            if(key.find("in_out_") == 0):
                key = key[7:]
                key = tablename_to_fields[table]["transform"].get(key, key)
                key = ("in_" + key, "out_" + key)
                if (key[0] not in fields) or (key[1] not in fields):
                        print("fields not exists this key：", key)
                        continue
                field = (fields[key[0]], fields[key[1]])

                if(field[0]["type"] in ["varchar"]):
                    in_conditions.append(
                        key[0] + " " + field[0]["joiner"] + " '" + value + "'")
                else:
                    in_conditions.append(
                        key[0] + " " + field[0]["joiner"] + " " + value + "")

                if(field[1]["type"] in ["varchar"]):
                    out_conditions.append(
                        key[1] + " " + field[1]["joiner"] + " '" + value + "'")
                else:
                    out_conditions.append(
                        key[1] + " " + field[1]["joiner"] + " " + value + "")
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
        print("sql_where:\n", sql_where)
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
            out_where = " ( " + " and ".join(out_conditions) + " ) "
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
        count_sql = "select count(*) from " + self.get_table(query["action"]) + self.get_where(
            self.get_table(query["action"]), query["where"]) + ";"
        return {
            "data_sql": data_sql,
            "count_sql": count_sql,
        }

    def export(self, query, rows):
        def trans_list_to_xml(data_list):
            # 字典转换为xml字符串
            xml_data = []
            for row in data_list:
                xml_row = []
                for k in row.keys():  # 遍历字典排序后的key
                    v = row.get(k)  # 取出字典中key对应的value
                    xml_row.append(
                        '<{key}>{value}</{key}>'.format(key=k, value=v))
                xml_row = ''.join(xml_row)
                xml_row = '<row>{}</row>'.format(xml_row)
                xml_data.append(xml_row)
            xml_data = '<xml>{}</xml>'.format(xml_data)
            return xml_data

        def trans_list_to_csv(data_list):
            """A view that streams a large CSV file."""
            # Generate a sequence of rows. The range is based on the maximum number of
            # rows that can be handled by a single sheet in most spreadsheet
            # applications.
            return data_list

        def trans_list_to_json(data_list):
            print("data_list:")
            print(data_list[:1])
            json_data = json.dumps(data_list, cls=CJsonEncoder)
            return json_data
        t = time.time()

        if("xml" == query["export_type"]):
            data = trans_list_to_xml(rows)
            response = FileResponse(data)
            response['Content-Type'] = 'application/xml'
            response['Content-Disposition'] = 'attachment;filename=' + \
                str(int(round(t * 1000000))) + '.xml'
        elif("csv" == query["export_type"]):
            pseudo_buffer = Echo()
            # rows = (["Row {}".format(idx), str(idx)] for idx in xrange(65536))
            writer = csv.writer(pseudo_buffer)
            response = StreamingHttpResponse((writer.writerow(row) for row in rows),
                                             content_type="text/csv")
            response['Content-Disposition'] = 'attachment;filename=' + \
                str(int(round(t * 1000000))) + '.csv'
        # if("json" == query["export_type"]):
        else:
            data = trans_list_to_json(rows)
            response = FileResponse(data)
            response['Content-Type'] = 'application/json'
            response['Content-Disposition'] = 'attachment;filename=' + \
                str(int(round(t * 1000000))) + '.json'
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
        count_result = conn.execute_and_fetch(count_sql)

        conn.close()
        print("count_result:", count_result)
        result = {
            "data": list(sql_result),
            "itemsCount": count_result[0]["count(*)"],
            "time": 0
        }
        # 这个地方可以再讨论，到底是返回response还是数据。
        if("export" in http_args["export"] and http_args["export"]["export"] == "true"):
            print("export is true")
            response = self.export(http_args["export"], result["data"])
        else:
            response = HttpResponse(json.dumps(
                result, indent=4, cls=DateEncoder), content_type="application/json")
        return response
