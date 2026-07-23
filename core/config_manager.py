import json
import os
import copy

class ConfigManager:
    """
    Класс для работы с конфигом проекта
    """
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
        """
        Проверяет наличие кеша, при отсуствии загружает стандартный
        """
        if cls._data is None:
            try:
                cls._cache()
            except (FileNotFoundError, json.JSONDecodeError):
                cls._data = copy.deepcopy(cls._DEFAULT_DICT)
                cls.save()
        if cls._check_config(cls._DEFAULT_DICT, cls._data):
            cls.save()
            
    @classmethod
    def _check_config(cls, default: dict, config: dict):
        """
        Проверяет наличие всех секций конфига
        
        Args:
            default (dict): стандартный конфиг
            config (dict): проверяемый конфиг
        
        Returns:
            bool: наличие изменений
        """
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
    def _validate_keys(cls, section, key):
        """
        Проверяет на ошибки в написании секций и ключей
        
        Args:
            section: секция конфига
            key: ключ секции
        """
        if section in cls._DEFAULT_DICT:
            if not key in cls._DEFAULT_DICT[section]:
                raise KeyError(f'key: "{key}" not found!')
        else:
            raise KeyError(f'section: "{section}" not found!')
                
    @classmethod
    def _cache(cls):
        """
        Загружает в кэш конфиг
        """
        with open(cls.JSON_NAME, 'r', encoding='utf-8') as cnfg:
            cls._data = json.load(cnfg)
            
    @classmethod
    def save(cls):
        """
        Записывает нынешний конфиг(кэш) в файл
        """
        with open(cls.TEMP_NAME, 'w', encoding='utf-8') as cnfg:
            json.dump(cls._data, cnfg, ensure_ascii=False, indent=4)
        os.replace(cls.TEMP_NAME, cls.JSON_NAME)
    
    #get
    @classmethod
    def _get(cls, section, key) -> str: #universal func
        """
        Запрос значения ключа в секции
        
        Args:
            section: секция конфига
            key: ключ секции
        
        Returns:
            str: значение ключа
        """
        cls.init()
        cls._validate_keys(section, key)
        return cls._data[section][key]

    @classmethod
    def get_port(cls) -> str:
        """
        Returns:
            str: порт ПК
        """
        return cls._get(cls.SECTION_SERVER, cls.KEY_PORT)

    @classmethod
    def get_host(cls) -> str:
        """
        Returns:
            str: хост ПК
        """
        return cls._get(cls.SECTION_SERVER, cls.KEY_HOST)

    @classmethod
    def get_id(cls) -> str:
        """
        Returns:
            str: айди пользователя в телеграме
        """
        return cls._get(cls.SECTION_TG, cls.KEY_TG_ID)
        
    @classmethod
    def get_api(cls) -> str:
        """
        Returns:
            str: API бота в тг
        """
        return cls._get(cls.SECTION_TG, cls.KEY_TG_API)
        
    #set
    @classmethod
    def set(cls, section, key, value): #universal func
        """
        Универсальная функция замены значения в конфиге
        Args:
            section: секция конфига
            key: ключ секции
        """
        cls.init()
        cls._validate_keys(section, key)
        cls._data[section][key] = value
        