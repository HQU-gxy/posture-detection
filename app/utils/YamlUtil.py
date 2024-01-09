import yaml
import json

import logging

logger = logging.getLogger(__name__)


class YamlUtil:

  @staticmethod
  def read_yaml(path):
    try:
      with open(path, encoding="utf-8") as f:
        result = f.read()
        result = yaml.load(result, Loader=yaml.FullLoader)
        return result
    except FileNotFoundError as e:
      logger.warning(e)

  @staticmethod
  def write_yaml(path, data):
    with open(path, "w", encoding="utf-8") as f:
      yaml.dump(data,
                f,
                Dumper=yaml.SafeDumper,
                sort_keys=False,
                allow_unicode=True)
