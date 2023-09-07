import os
import argparse
import yaml
from tqdm import tqdm
import waymo_open_dataset as waymo
import nuscenes as nusc

from parser import txt_parser, json_parsor
from format_converter import kitti_converter, nusc_converter, waymo_converter


def args_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_label_dir', type=str, help='Directory to load user defined label')
    parser.add_argument('--output_label_dir', type=str, help='Directory to save converted label')
    parser.add_argument('--tgt_label_type', type=str, default='', help='Dataset name to convert (kitti, nuscenes, waymo)')
    return parser.parse_args()


def config_validation(config):
    if config['ext'] == 'text' and not config['split']:
        return None

    # TODO: if need add configuration file validation code

    return config


def parse_config(yaml_path):
    assert os.path.exists(yaml_path), 'Not found configuration YAML file'

    with open(yaml_path, 'r') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    config = config_validation(config)

    return config


def convert(args):
    config = parse_config('config/config.yaml')
    assert config is not None, 'Invalid configuration file'

    parser = getattr(f'{config["ext"]}_parser', 'Parser')(config)
    converter = getattr(f'{args.tgt_label_type}_converter', 'convert')
    saver = getattr(f'{args.tgt_label_type}_converter', 'save')

    src_labels = os.listdir(args.input_label_dir)
    for src_label in tqdm(src_labels):
        parsed_label = parser.parse(f'{args.input_label_dir}/{src_label}')

        # TODO: convert to each dataset type
        converted_label = converter(parsed_label)

        # TODO: save correctly each dataset type
        saver(f'{args.output_label_dir.rstrip("/")}/{src_label}', converted_label)


if __name__ == '__main__':
    args = args_parser()
    convert(args)
    print('done.')
