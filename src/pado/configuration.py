import json
import logging
from pathlib import Path
from typing import Set

import appdirs

REGISTERED_PADOS_JSON_FIELD = 'registered_pados'
CONFIG_FILENAME: str = 'config.json'
PADO_CONFIG_NAME = 'pado'
CONFIG_DIR = Path(appdirs.user_config_dir(appname=PADO_CONFIG_NAME))


def register_pado_in_known_pados(filename):
    config = get_pado_config_file()
    if not config.exists():
        # Make sure folder exists
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        logging.debug(f"Config file does not exist: {config}")
        data = {REGISTERED_PADOS_JSON_FIELD: {str(Path(filename).absolute())}}
        logging.debug(data)
        with config.open('w') as f:
            logging.debug(f"Created config: {config}")
            json.dump(data, f, ensure_ascii=False, indent=4, default=serialize_sets)
    register_filename_in_central_storage(config, filename)


def register_filename_in_central_storage(config, filename):
    configuration = read_configuration_from_file(config)
    configuration[REGISTERED_PADOS_JSON_FIELD].add(str(Path(filename).absolute()))
    write_configuration_to_central_storage(config, configuration)
    logging.debug(f"After registering {filename}, config file contains: {configuration}")


def read_configuration_from_file(config):
    with config.open('r') as f:
        logging.debug(f"Config file exists: {config}")
        configuration = json.load(f)  # now 'configuration' can safely be imported from this module
        logging.debug(f"config file contains: {configuration}")
        configuration[REGISTERED_PADOS_JSON_FIELD] = set(configuration[REGISTERED_PADOS_JSON_FIELD])
    return configuration


def write_configuration_to_central_storage(config, configuration):
    with config.open('w') as f1:
        json.dump(configuration, f1, ensure_ascii=False, indent=4, default=serialize_sets)


def get_pado_config_file():
    return CONFIG_DIR / CONFIG_FILENAME


def serialize_sets(obj):
    if isinstance(obj, set):
        return list(obj)

    raise TypeError


def read_known_pados_from_config() -> Set[str]:
    config = CONFIG_DIR / CONFIG_FILENAME
    if not config.exists():
        logging.debug(f"Config file does not exist: {config}")
        return set()
    configuration = read_configuration_from_file(config)
    known_pados = configuration[REGISTERED_PADOS_JSON_FIELD]
    return known_pados


def pretty_print_known_pados(known_pados):
    if len(known_pados) == 0:
        print("No known pados. Register them by running or registering explicitly")
    else:
        print("Known pados:")
        for pado in known_pados:
            print(f"\t{pado}")
