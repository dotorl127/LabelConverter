# userDFlabel_cvt
- convert user defined label to known dataset label(etc. KITTI, COCO, VOC, MOT)
- read configuration YAML file and parse user defined format

## Updates
### October 2023
- [x] add voc, mot converter
- [x] refactoring parse, convert logic
- [x] default support format(kitti, coco, voc, mot) convert test complete
### September 2023
- [x] add kitti, coco converter
- [x] organize base, template data and code
- [x] initialize repository

## Support dataset label
- [KITTI](https://www.cvlibs.net/datasets/kitti/eval_object.php?obj_benchmark=3d)
- [COCO](https://cocodataset.org/#download)
- [VOC](http://host.robots.ox.ac.uk/pascal/VOC/voc2012/index.html)
- [MOT](https://motchallenge.net/data/MOT17/)

## Requirements
```commandline
pip install pyyaml tqdm xmltodict
```

## How to use
### Arguments
```text
-i, --input_label_path : user defined label location
-c, --config_path      : configuration YAML file for parse user defined format
-o, --output_label_dir : output directory for save converted label
-t, --tgt_label_type   : dataset/label type want to convert
                         current support [KITTI, COCO, VOC, MOT]
```

### Command line
```commandline
(example)$ python main.py -i ./somewhere/to/coco -c ./config/config_coco.yaml -o ./test_result/ -t kitti 
```

## How to custom
### Parser
- create parser module using [base_parser.py](./label_parser/base_parser.py) in [label_parser](./label_parser) directory.
- should coordinates format to x1, y1, x2, y2 using class function or custom function.
- create configuration YAML file correctly could parse user defined label in [config](./config) directory
  - incase text type like csv just write column number each attribute
  - incase json, xml or hierarchy exists write start to end node to reach attribute

### Converter
- create converter module using [template_converter.py](./format_converter/template_converter.py) in [format_converter](./format_converter) directory.
- should write code into class function named [convert](./format_converter/template_converter.py#L11), [save](./format_converter/template_converter.py#L18) for convert parsed label and saving output.
- if need convert coordinates format want from x1, y1, x2, y2
