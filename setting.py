# -*- coding: utf-8 -*-
action_to_tablename = {
    "all": "edge_table",
    "ip": "node_table",
    "single": "edge_table",
    "router_link": "router_edge_table",
    "router_node": "router_node_table",
    "router_appear": "router_edge_table",
    "equal_router": "node_table",
    "pop_topo_link": "pop_edge_table",
    "pop_topo_node": "pop_edge_table",
}

action_transform_fields = {
    "single": {
        "ip": "in_out_ip",
    }
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
    },
    "node_table": {
        "fields": {
            "ip": {
                "type": "varchar",
                "joiner": "="
            },
            "asn": {
                "type": "int",
                "joiner": "="
            },
            "country": {
                "type": "varchar",
                "joiner": "="
            },
            "city": {
                "type": "varchar",
                "joiner": "="
            },
        },
        "transform":
            {

        }
    },
    "router_node_table": {
        "fields": {
            "ip": {
                "type": "varchar",
                "joiner": "="
            },
            "asn": {
                "type": "int",
                "joiner": "="
            },
            "country": {
                "type": "varchar",
                "joiner": "="
            },
            "city": {
                "type": "varchar",
                "joiner": "="
            },
            "is_as_boundary": {
                "type": "char",
                "joiner": "="
            },
            "is_country_boundary": {
                "type": "char",
                "joiner": "="
            }
        },
        "transform":
            {

        }
    },
    "router_edge_table": {
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
            "is_as_boundary": {
                "type": "char",
                "joiner": "="
            },
            "is_country_boundary": {
                "type": "char",
                "joiner": "="
            }
        },
        "transform":
            {

        }
    },
    "pop_edge_table": {
        "fields": {
            "in_pop_id": {
                "type": "varchar",
                "joiner": "="
            },
            "out_pop_id": {
                "type": "varchar",
                "joiner": "="
            },
            "num": {
                "type": "int",
                "joiner": "="
            },
        },
        "transform":
            {

        }
    },
    "pop_node_table": {
        "fields": {
            "pop_id": {
                "type": "varchar",
                "joiner": "="
            },
            "geo": {
                "type": "varchar",
                "joiner": "="
            },
            "num": {
                "type": "int",
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
