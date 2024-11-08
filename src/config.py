import os
import sys

from dotenv import load_dotenv
from pathlib import Path


ENV_PATH = Path(__file__).parent.parent / '.env'


load_dotenv(dotenv_path=ENV_PATH)


def get_env_variables(keys: [str]) -> dict[str, str|None]:

  variables: dict[str, str|None] = {}
  missing_keys: list[str] = []

  for key in keys:
    variable: str = os.environ.get(key)
    variables[key] = variable if variable else missing_keys.append(key)
  
  if missing_keys:
    sys.exit(f"Missing environment variables: {', '.join(missing_keys)}")
  
  return variables


env_variables: [str] = get_env_variables([
  # Discord
  'BOT_TOKEN',
  'BOT_PUBLIC_KEY',
  'BOT_PERMISSIONS',
])


if __name__ == '__main__':
  for key, value in env_variables.items():
    print(f'{key}: {value}')