import os
import argparse
from tqdm import tqdm
from utils.util import parse_config, redirect_path


def args_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input_label_path', type=str, help='Directory to load user defined label')
    parser.add_argument('-c', '--config_path', type=str, help='Location parse configuration file')
    parser.add_argument('-o', '--output_label_dir', type=str, help='Directory to save converted label')
    parser.add_argument('-t', '--tgt_label_type', type=str, default='',
                        help='Dataset name to convert [kitti, coco, voc, mot]')
    return parser.parse_args()


def main(args):
    args.input_label_path = args.input_label_path.rstrip("/")
    args.output_label_dir = args.output_label_dir.rstrip("/")

    # parsing configuration file
    config = parse_config(args.config_path)
    assert config is not None, 'Invalid configuration file'

    # import parser module
    parser \
        = (getattr(__import__(f'label_parser.{config["ext"]}_parser',
                              fromlist=["label_parser"]), 'parser')
           (config))
    assert parser is not None, f"Not found {config['ext']}_parser"

    # import converter module
    converter \
        = (getattr(__import__(f'format_converter.{args.tgt_label_type.lower()}_converter',
                              fromlist=["format_converter"]), 'converter')
           (True if len(config['extra']) else False, args.output_label_dir))
    assert converter is not None, f"Not found {args.tgt_label_type.lower()}_converter"

    # modify input path
    is_file, src_labels = redirect_path(args.input_label_path)

    # parsing input label and convert to default label format
    if not is_file:
        parsed_user_label = []
        for src_label in tqdm(src_labels, desc="annotations parsing", leave=True):
            parsed_user_label += parser.parse(f'{args.input_label_path}/{src_label}', p_bar_need=False)
    else:
        parsed_user_label = parser.parse(src_labels, p_bar_need=True)

    # converting default label format to want
    converter.convert(parsed_user_label)

    # save converted label
    if not os.path.exists(args.output_label_dir):
        os.makedirs(args.output_label_dir)
    converter.save()


if __name__ == '__main__':
    args = args_parser()
    main(args)
    print('done.')
