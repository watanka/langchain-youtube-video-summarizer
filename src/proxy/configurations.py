import os
from logging import getLogger
from typing import Dict
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

logger = getLogger(__name__)

openai_api_key = os.getenv('OPENAI_API_KEY', '')


class ServiceConfigurations :
    services : Dict[str, str] = {}
    for environ in os.environ.keys() :
        if environ.endswith("_SERVICE") :
            url = f"http://{os.getenv(environ)}"
            services[environ.lower().replace('_service', '')] = url

