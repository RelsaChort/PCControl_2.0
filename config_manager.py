import json
import os
import copy

class ConfigManager:
    #names
    SECTION_SERVER = 'server'
    KEY_HOST = 'host'
    KEY_PORT = 'port'
    
    SECTION_TG = 'tg'
    KEY_TG_ID = 'tg_id'
    KEY_TG_API = 'api'
    
    #const
    DEFAULT_HOST = '192.168.1.69'
    DEFAULT_PORT = '4000'
    DEFAULT_TG_ID = '1570105921'
    DEFAULT_TG_API = ''
    JSON_NAME = 'pccontrol_config.json'
    TEMP_NAME = f"{JSON_NAME}.tmp"
    
    #cache
    _data = None
    
    _DEFAULT_DICT = {
                    SECTION_SERVER:
                        {
                            KEY_HOST: DEFAULT_HOST,
                            KEY_PORT: DEFAULT_PORT
                        },
                        SECTION_TG:
                        {
                            KEY_TG_API: DEFAULT_TG_API,
                            KEY_TG_ID: DEFAULT_TG_ID
                        }
                    }
    
    @classmethod
    def init(cls):
        if cls._data is None:
            try:
                cls._cache()
            except (FileNotFoundError, json.JSONDecodeError):
                cls._data = copy.deepcopy(cls._DEFAULT_DICT)
                cls._writer()
        if cls._check_config(cls._DEFAULT_DICT, cls._data):
            cls._writer()
            
    @classmethod
    def _check_config(cls, default: dict, config: dict):
        changes = False
        for key, value in default.items():
            if key not in config or not isinstance(config[key], type(value)):
                c_value = copy.deepcopy(value)
                config[key] = c_value
                changes = True
                continue
            
            if isinstance(value, dict):
                if cls._check_config(value, config[key]):
                    changes = True
                    
        return changes
    @classmethod
    def _cache(cls):
        with open(cls.JSON_NAME, 'r', encoding='utf-8') as cnfg:
            cls._data = json.load(cnfg)
            
    @classmethod
    def _writer(cls):
        with open(cls.TEMP_NAME, 'w', encoding='utf-8') as cnfg:
            json.dump(cls._data, cnfg, ensure_ascii=False, indent=4)
        os.replace(cls.TEMP_NAME, cls.JSON_NAME)
    
    #get
    @classmethod
    def _get(cls, section, key) -> str: #universal func
        cls.init()
        return cls._data[section][key]

    @classmethod
    def get_port(cls) -> str:
        return cls._get(cls.SECTION_SERVER, cls.KEY_PORT)

    @classmethod
    def get_host(cls) -> str:
        return cls._get(cls.SECTION_SERVER, cls.KEY_HOST)

    @classmethod
    def get_id(cls) -> str:
        return cls._get(cls.SECTION_TG, cls.KEY_TG_ID)
        
    @classmethod
    def get_api(cls) -> str:
        return cls._get(cls.SECTION_TG, cls.KEY_TG_API)
        
    #set
    @classmethod
    def _set(cls, section, key, value): #universal func
        cls.init()
        cls._data[section][key] = value
        cls._writer()
        
        
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