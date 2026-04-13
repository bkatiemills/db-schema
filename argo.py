# usage: python argo.py
# creates empty collections in the argo db called argoMeta and argo with schema validation enforcement and defined indexes

from pymongo import MongoClient
import sys

client = MongoClient('mongodb://database/argo')
db = client.argo

metacollection = 'argoMeta'
datacollection = 'argo'

db[metacollection].drop()
db.create_collection(metacollection)
db[datacollection].drop()
db.create_collection(datacollection)

argo_vars = ["bbp470","bbp532","bbp700","bbp700_2","bisulfide","cdom","chla","cndc","cndx","cp660","down_irradiance380","down_irradiance412","down_irradiance442","down_irradiance443","down_irradiance490","down_irradiance555","down_irradiance670","downwelling_par","doxy","doxy2","doxy3","molar_doxy","nitrate","ph_in_situ_total","pressure","salinity","salinity_sfile","temperature","temperature_sfile","turbidity","up_radiance412","up_radiance443","up_radiance490","up_radiance555"]
argo_measurements = argo_vars + [x+'_std' for x in argo_vars] + [x+'_med' for x in argo_vars]
argo_measurements += [x + '_argoqc' for x in argo_measurements]

argoMetaSchema = {
    "bsonType": "object",
    "required": ["_id", "data_type"],
    "properties":{
        "_id": {
            "bsonType": "string"
        },
        "data_type": {
            "bsonType": "string"
        },
        "data_center": {
            "bsonType": "string"
        },
        "instrument": {
            "bsonType": "string"
        },
        "pi_name": {
            "bsonType": "array",
            "items": {
                "bsonType": "string"
            }
        },
        "platform": {
            "bsonType": "string"
        },
        "platform_type": {
            "bsonType": "string"
        },
        "fleetmonitoring": {
            "bsonType": "string"
        },
        "oceanops": {
            "bsonType": "string"
        },
        "positioning_system": {
            "bsonType": "string"
        },
        "wmo_inst_type": {
            "bsonType": "string"
        }
    }
}

argoSchema = {
    "bsonType": "object",
    "required": ["_id","metadata","geolocation","basin","timestamp","data", "date_updated_argovis", "source", "cycle_number"],
    "properties": {
        "_id": {
            "bsonType": "string"
        },
        "metadata": {
            "bsonType": "array",
            "items": {
                "bsonType": "string"
            }
        },
        "geolocation": {
            "bsonType": "object",
            "required": ["type", "coordinates"],
            "properties": {
                "type":{
                    "enum": ["Point"]
                },
                "coordinates":{
                    "bsonType": "array",
                    "minItems": 2,
                    "maxItems": 2,
                    "items": {
                        "bsonType": ["double", "int"]
                    }
                }
            }
        },
        "basin": {
            "bsonType": "int"
        },
        "timestamp": {
            "bsonType": ["date", "null"]
        },
        "data": {
            "bsonType": "array",
            "items": {
                "bsonType": "array",
                "items": {
                    "bsonType": ["double", "int", "string", "null"]
                }
            }
        },
        "data_info": {
            "bsonType": "array",
            "items": {
                "bsonType": "array",
                "items": {
                    "bsonType": ["string", "array"]
                }
            }
        },
        "date_updated_argovis": {
            "bsonType": "date"
        },
        "source": {
            "bsonType": "array",
            "items": {
                "bsonType": "object",
                "required": ["source"],
                "properties": {
                    "source": {
                        "bsonType": "array",
                        "items": {
                            "bsonType": "string"
                        }
                    },
                    "url": {
                        "bsonType": "string",
                    },
                    "date_updated": {
                        "bsonType": "date",
                    }
                }
            }
        },
        "data_warning": {
            "bsonType": "array",
            "items": {
                "bsonType": "string",
                "enum": ["degenerate_levels", "missing_basin", "missing_location", "missing_timestamp"]
            }
        },
        "cycle_number": {
            "bsonType": "int"
        },
        "geolocation_argoqc": {
            "bsonType": "int"
        },
        "profile_direction": {
            "bsonType": "string"
        },
        "timestamp_argoqc": {
            "bsonType": "int"
        },
        "vertical_sampling_scheme": {
            "bsonType": "string"
        },
        "bgc_mismatches":{
	    "bsonType": "object"
        }
    }
}

db.command('collMod',metacollection, validator={"$jsonSchema": argoMetaSchema}, validationLevel='strict')
db[metacollection].create_index([("data_center", 1)])
db[metacollection].create_index([("platform", 1)])
db[metacollection].create_index([("platform_type", 1)])

db.command('collMod',datacollection, validator={"$jsonSchema": argoSchema}, validationLevel='strict')
db[datacollection].create_index([("metadata", 1)])
db[datacollection].create_index([("timestamp", -1), ("geolocation", "2dsphere")])
db[datacollection].create_index([("timestamp", -1)])
db[datacollection].create_index([("geolocation", "2dsphere")])
db[datacollection].create_index([("source.source", 1)])
db[datacollection].create_index([("geolocation.coordinates", "2d"), ("timestamp", -1)])
db[datacollection].create_index([("geolocation_argoqc", 1)])
