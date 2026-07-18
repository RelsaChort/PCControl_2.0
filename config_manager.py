import json
import os

class ConfigManager:
    #standart names

    SECTION_SERVER = 'server'
    KEY_HOST = 'host'
    KEY_PORT = 'port'
    
    SECTION_TG = 'tg'
    KEY_TG_ID = 'id'
    KEY_TG_API = 'api'
    
    #standart const
    DEFAULT_HOST = '192.168.1.69'
    DEFAULT_PORT = '4000'
    DEFAULT_TG_ID = '1570105921'
    DEFAULT_TG_API = ''
    JSON_NAME = 'pccontrol_config.json'
    TEMP_NAME = f"{JSON_NAME}.tmp"
    
    #cache
    _data = None
    
    @classmethod
    def init(cls):
        if not cls._data:
            try:
                with open(cls.JSON_NAME, 'r', encoding='utf-8') as cnfg:
                    cls._data = json.load(cnfg)
            except Exception as E:
                cls._data = {
                        cls.SECTION_SERVER:
                            {
                                cls.KEY_HOST: cls.DEFAULT_HOST,
                                cls.KEY_PORT: cls.DEFAULT_PORT
                            },
                        cls.SECTION_TG:
                            {
                                cls.KEY_TG_API: cls.DEFAULT_TG_API,
                                cls.KEY_TG_ID: cls.DEFAULT_TG_ID
                            }
                        }
                with open(cls.TEMP_NAME, 'w', encoding='utf-8') as cnfg:
                    json.dump(cls._data, cnfg, ensure_ascii=False, indent=4)
                os.replace(cls.TEMP_NAME, cls.JSON_NAME)
    #get
    @classmethod
    def _get(cls, section, key) -> str: #universal func
        if cls._data:
            value = cls._data[section][key]
            return value
        else:
            cls.init()
            value = cls._data[section][key]
            return value
    @classmethod
    def get_port(cls) -> str:
        port = cls._get(cls.SECTION_SERVER, cls.KEY_PORT)
        return port
    @classmethod
    def get_host(cls) -> str:
        host = cls._get(cls.SECTION_SERVER, cls.KEY_HOST)
        return host
    @classmethod
    def get_id(cls) -> str:
        id = cls._get(cls.SECTION_TG, cls.KEY_TG_ID)
        return id
    @classmethod
    def get_api(cls) -> str:
        api = cls._get(cls.SECTION_TG, cls.KEY_TG_API)
        return api
        
    #set
    @classmethod
    def _set(cls, section, key, value): #universal func
        with open(cls.JSON_NAME, 'r', encoding='utf-8') as cnfg:
            data = json.load(cnfg)
        
        data[section][key] = value
        
        with open(cls.TEMP_NAME, 'w', encoding='utf-8') as cnfg:
            json.dump(data, cnfg, ensure_ascii=False, indent=4)
        os.replace(cls.TEMP_NAME, cls.JSON_NAME)
        cls._data[section][key] = value
        
    @classmethod
    def set_host(cls, host: str):
        cls._set(cls.SECTION_SERVER, cls.KEY_HOST, host)
    @classmethod
    def set_port(cls, port: str):
        cls._set(cls.SECTION_SERVER, cls.KEY_PORT, port)
    @classmethod
    def set_tg_id(cls, id: str):
        cls._set(cls.SECTION_TG, cls.KEY_TG_ID, id)
    @classmethod
    def set_api(cls, api: str):
        cls._set(cls.SECTION_TG, cls.KEY_TG_API, api)