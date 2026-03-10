import configparser
import os

def load_config():
    """Hàm load config từ file config.ini nằm ở thư mục gốc."""
    # Xác định đường dẫn thư mục gốc (nơi đặt config.ini)
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    CONFIG_PATH = os.path.join(BASE_DIR, 'config.ini')

    # Khởi tạo và đọc file config
    config = configparser.ConfigParser()
    config.read(CONFIG_PATH)

    return config

def get_composio_api_key():
    """Trả về giá trị COMPOSIO API key từ file config.ini"""
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    CONFIG_PATH = os.path.join(BASE_DIR, 'config.ini')

    config = configparser.ConfigParser()
    config.read(CONFIG_PATH)

    return config['DEFAULT'].get('COMPOSIO_API_KEY', 'No COMPOSIO API Key')

def get_composio_organization_api_key():
    """Trả về giá trị COMPOSIO_ORGANIZATION_API key từ file config.ini"""
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    CONFIG_PATH = os.path.join(BASE_DIR, 'config.ini')

    config = configparser.ConfigParser()
    config.read(CONFIG_PATH)

    return config['DEFAULT'].get('COMPOSIO_ORGANIZATION_API_KEY', 'No COMPOSIO ORGANIZATION API Key')

def get_openai_key():
    """Trả về giá trị OPENAI_API key từ file config.ini"""
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    CONFIG_PATH = os.path.join(BASE_DIR, 'config.ini')

    config = configparser.ConfigParser()
    config.read(CONFIG_PATH)

    return config['DEFAULT'].get('OPENAI_API_KEY', 'No OPENAI API Key')
