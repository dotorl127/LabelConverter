import os
import argparse
import yaml
from tqdm import tqdm
import waymo_open_dataset as waymo
import nuscenes as nusc

from parser import txt_parser, json_parsor
from format_convert import kitti_converter as kic
from format_convert import nusc_converter as nuc
from format_convert import waymo_converter as wac


def args_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_label_dir', help='Directory to load user defined label')
    parser.add_argument('--output_label_dir', help='Directory to save converted label')
    parser.add_argument('--tgt_label_type', default='', help='Dataset name to convert (kitti, nuscenes, waymo)')
    return parser.parse_args()


def parse_config(yaml_path):
    assert os.path.exists(yaml_path), 'Not found configuration YAML file'

    with open(yaml_path, 'r') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    return config


def convert(args):
    config = parse_config('config/config.yaml')

    # TODO: load function via args.tgt_label_type

    src_labels = os.listdir(args.input_label_dir)
    for src_label in tqdm(src_labels):
        # TODO: convert to each dataset type
        converted_label = kic.converet(src_label)

        # TODO: save correctly each dataset type


if __name__ == '__main__':
    args = args_parser()
    convert(args)
    print('done.')
