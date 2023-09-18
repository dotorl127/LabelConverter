import os
import argparse

import yaml
from tqdm import tqdm


def args_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input_label_path', type=str, help='Directory to load user defined label')
    parser.add_argument('-c', '--config_path', type=str, help='Location parse configuration file')
    parser.add_argument('-o', '--output_label_dir', type=str, help='Directory to save converted label')
    parser.add_argument('-t', '--tgt_label_type', type=str, default='',
                        help='Dataset name to convert (kitti, coco, ...)')
    return parser.parse_args()


def config_validation(config):
    """
    if need add configuration file validation code
    """
    if config['ext'] == 'text' and not config['split']:
        return None

    return config


def parse_config(yaml_path):
    assert os.path.exists(yaml_path), 'Not found configuration YAML file'

    with open(yaml_path, 'r') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)

    return config


def redirect_path(path):
    is_file, src_labels = False, None

    if os.path.isfile(path):
        src_labels = path
        is_file = True
    elif os.path.isdir(path):
        src_labels = os.listdir(path)

    return is_file, src_labels


def main(args):
    args.input_label_path = args.input_label_path.rstrip("/")
    args.output_label_dir = args.output_label_dir.rstrip("/")

    config = parse_config(args.config_path)
    assert config is not None, 'Invalid configuration file'

    parser = getattr(
        __import__(f'label_parser.{config["ext"]}_parser', fromlist=["label_parser"]), 'parser')(config)
    assert parser is not None, "Not found parser"

    converter = getattr(
        __import__(f'format_converter.{args.tgt_label_type}_converter',
                   fromlist=["format_converter"]), 'converter')(True if len(config['extra']) else False,
                                                                True if config["file_name"] else False)
    assert converter is not None, "Not found converter"

    is_file, src_labels = redirect_path(args.input_label_path)

    if not is_file:
        parsed_user_label = []
        for src_label in tqdm(src_labels, desc="annotations parsing"):
            parsed_user_label += parser.parse(f'{args.input_label_path}/{src_label}', p_bar_need=False)
        converter.convert(parsed_user_label, args.output_label_dir)
    else:
        parsed_user_label = parser.parse(src_labels, p_bar_need=True)
        converter.convert(parsed_user_label, args.output_label_dir)


if __name__ == '__main__':
    args = args_parser()
    main(args)
    print('done.')
