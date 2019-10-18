action_to_tablename = {
    "all": "edge_table"
}

tablename_to_fields = {
    "edge_table": {
        "fields": {
            "in_ip": {
                "type": "varchar",
                "joiner": "链接入接口IP地址"
            },
            "out_ip": {
                "type": "varchar",
                "joiner": "链接出接口IP地址"
            },
            "is_dest": {
                "type": "char",
                "joiner": "出接口是否是目标IP地址"
            },
            "star": {
                "type": "int",
                "joiner": "链接经过匿名跳数"
            },
            "latency": {
                "type": "float",
                "joiner": "链接时延"
            },
            "freq": {
                "type": "int",
                "joiner": "发现频率"
            },
            "ttl": {
                "type": "int",
                "joiner": "链接在traceroute中的最小ttl"
            },
            "monitor": {
                "type": "varchar",
                "joiner": "最小ttl对应的监测点名称"
            },
            "first_seen": {
                "type": "timestamp",
                "joiner": "第一次发现链接时间"
            },
            "last_seen": {
                "type": "timestamp",
                "joiner": "最后一次发现链接时间"
            },
            "in_asn": {
                "type": "int",
                "joiner": "as号"
            },
            "in_country": {
                "type": "varchar",
                "joiner": "入IP城市"
            },
            "in_region": {
                "type": "varchar",
                "joiner": "入IP地区"
            },
            "in_city": {
                "type": "varchar",
                "joiner": "入IP城市"
            },
            "in_longitude": {
                "type": "varchar",
                "joiner": "入IP经度"
            },
            "in_latitude": {
                "type": "varchar",
                "joiner": "入IP纬度"
            },
            "in_whois": {
                "type": "varchar",
                "joiner": "入IPwhois"
            },
            "in_domain": {
                "type": "varchar",
                "joiner": "入IP自治域"
            },
            "out_asn": {
                "type": "int",
                "joiner": "as号"
            },
            "out_country": {
                "type": "varchar",
                "joiner": "出IP城市"
            },
            "out_region": {
                "type": "varchar",
                "joiner": "出IP地区"
            },
            "out_city": {
                "type": "varchar",
                "joiner": "出IP城市"
            },
            "out_longitude": {
                "type": "varchar",
                "joiner": "出IP经度"
            },
            "out_latitude": {
                "type": "varchar",
                "joiner": "出IP纬度"
            },
            "out_whois": {
                "type": "varchar",
                "joiner": "出IPwhois"
            },
            "out_domain": {
                "type": "varchar",
                "joiner": "出IP自治域"
            },
            "is_as_boundary": {
                "type": "char",
                "joiner": "是否as边界"
            },
            "is_country_boundary": {
                "type": "char",
                "joiner": "是否国家边界"
            },
            "bandwidth": {
                "type": "varchar",
                "joiner": "链路容量"
            },
            "type": {
                "type": "int",
                "joiner": "探测类型"
            },
            "misc": {
                "type": "longtext",
                "joiner": "存储非traceout探测属性"
            },
            "updated_by": {
                "type": "longtext",
                "joiner": "NULL"
            }
        },
        "transform":
            {

        }
    }
}
