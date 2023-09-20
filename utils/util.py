import os
import yaml


def config_validation(config):
    """
    if need add configuration file validation code
    """
    if not config['split_key']:
        return None

    return config


def parse_config(yaml_path):
    assert os.path.exists(yaml_path), 'Not found configuration YAML file'

    with open(yaml_path, 'r') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)

    config = config_validation(config)

    return config


def redirect_path(path):
    is_file, src_labels = False, None

    if os.path.isfile(path):
        src_labels = path
        is_file = True
    elif os.path.isdir(path):
        src_labels = os.listdir(path)

    return is_file, src_labels
