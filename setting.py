# -*- coding: utf-8 -*-
action_to_tablename = {
    "all": "edge_table"
}

tablename_to_fields = {
    "edge_table": {
        "fields": {
            "in_ip": {
                "type": "varchar",
                "joiner": "="
            },
            "out_ip": {
                "type": "varchar",
                "joiner": "="
            },
            "in_asn": {
                "type": "int",
                "joiner": "="
            },
            "in_country": {
                "type": "varchar",
                "joiner": "="
            },
            "in_city": {
                "type": "varchar",
                "joiner": "="
            },
            "out_asn": {
                "type": "int",
                "joiner": "="
            },
            "out_country": {
                "type": "varchar",
                "joiner": "="
            },
            "out_city": {
                "type": "varchar",
                "joiner": "="
            },
        },
        "transform":
            {

        }
    }
}

request_contain_key = {
    "page": ["pageIndex", "pageSize"],
    "sort": ["sortOrder", "sortField"],
    # "action": ["action"],
    "export": ["export_type", "export", "export_limit"],
    "where": []
}
