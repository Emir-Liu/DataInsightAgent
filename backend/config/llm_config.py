
import os

CURRENT_LLM_MODEL = os.environ.get('CURRENT_LLM_MODEL_ENV')
DEFAULT_LLM_MODEL_API_KEY = os.environ.get('DEFAULT_LLM_MODEL_API_KEY_ENV')
DEFAULT_LLM_MODEL_API_BASE_URL = os.environ.get('DEFAULT_LLM_MODEL_API_BASE_URL_ENV')
DEFAULT_LLM_MODEL_MODEL_NAME = os.environ.get('DEFAULT_LLM_MODEL_MODEL_NAME_ENV')
DEFAULT_LLM_MODEL_MAX_LEN = int(os.environ.get('DEFAULT_LLM_MODEL_MAX_LEN_ENV'))
DEFAULT_LLM_API_MAX_TRY_NUM = int(os.environ.get('DEFAULT_LLM_API_MAX_TRY_NUM_ENV'))