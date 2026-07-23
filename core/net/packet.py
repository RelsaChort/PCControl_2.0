import json

class Packet:
    """
    
    """
    @staticmethod
    def dict_to_bytes(msg: dict) -> bytes:
        """
        Переводит словарь в байты для передачи между сокетами
        
        Args:
            msg (dict): пакет для передачи
        
        Returns:
            bytes: байты для передачи
        """
        bytes_msg = json.dumps(msg).encode('utf-8')
        return bytes_msg
    @staticmethod
    def bytes_to_dict(bytes_msg: bytes) -> dict:
        """
        Переводит пакет байтов в словарь
        
        Args:
            bytes_msg (bytes): полученные байты
            
        Returns:
            dict: полученный пакет в виде словаря
        """
        msg = bytes_msg.decode('utf-8')
        msg_json_dict = json.loads(msg)
        return msg_json_dict