import json
import os
import argparse

import yaml
from tqdm import tqdm


def args_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_label_path', type=str, help='Directory to load user defined label')
    parser.add_argument('--config_path', type=str, help='Location parse configuration file')
    parser.add_argument('--output_label_dir', type=str, help='Directory to save converted label')
    parser.add_argument('--tgt_label_type', type=str, default='',
                        help='Dataset name to convert (kitti, nuscenes, waymo)')
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
    config = config_validation(config)

    return config


def main(args):
    args.input_label_path = args.input_label_path.rstrip("/")
    args.output_label_dir = args.output_label_dir.rstrip("/")

    config = parse_config(args.config_path)
    assert config is not None, 'Invalid configuration file'

    parser = getattr(
        __import__(f'label_parser.{config["ext"]}_parser', fromlist=["label_parser"]), 'parser')(config)
    assert parser is not None, "Not found parser"

    converter = getattr(
        __import__(f'format_converter.{args.tgt_label_type}_converter', fromlist=["format_converter"]), 'Converter')
    assert converter is not None, "Not found converter"

    src_labels = None

    if os.path.isfile(args.input_label_path):
        src_labels = [args.input_label_path.split('/')[-1]]
        args.input_label_path = os.path.dirname(args.input_label_path)
    elif os.path.isdir(args.input_label_path):
        src_labels = os.listdir(args.input_label_path)
    assert src_labels is not None, 'Not found annotations file/directory'

    for src_label in tqdm(src_labels):
        parsed_user_label = parser.parse(f'{args.input_label_path}/{src_label}')
        print(parsed_user_label[0])
        converter.run(parsed_user_label, args.output_label_dir, src_label)


if __name__ == '__main__':
    args = args_parser()
    main(args)
    print('done.')
