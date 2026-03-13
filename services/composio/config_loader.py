import configparser
import os

def load_config():
    """Load config values from config.ini in the current folder."""
    # Resolve base directory (location of config.ini)
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    CONFIG_PATH = os.path.join(BASE_DIR, 'config.ini')

    # Initialize parser and read file
    config = configparser.ConfigParser()
    config.read(CONFIG_PATH)

    return config

def get_composio_api_key():
    """Return COMPOSIO API key from config.ini."""
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    CONFIG_PATH = os.path.join(BASE_DIR, 'config.ini')

    config = configparser.ConfigParser()
    config.read(CONFIG_PATH)

    return config['DEFAULT'].get('COMPOSIO_API_KEY', 'No COMPOSIO API Key')

def get_composio_organization_api_key():
    """Return COMPOSIO_ORGANIZATION_API_KEY from config.ini."""
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    CONFIG_PATH = os.path.join(BASE_DIR, 'config.ini')

    config = configparser.ConfigParser()
    config.read(CONFIG_PATH)

    return config['DEFAULT'].get('COMPOSIO_ORGANIZATION_API_KEY', 'No COMPOSIO ORGANIZATION API Key')

def get_openai_key():
    """Return OPENAI_API_KEY from config.ini."""
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    CONFIG_PATH = os.path.join(BASE_DIR, 'config.ini')

    config = configparser.ConfigParser()
    config.read(CONFIG_PATH)

    return config['DEFAULT'].get('OPENAI_API_KEY', 'No OPENAI API Key')
