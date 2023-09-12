# userDFlabel_cvt
- convert user defined label to known dataset label(etc. KITTI, COCO)
- read configuration YAML file and parse user defined label architecture

## updates
### September 2023
- [x] add kitti, coco converter
- [x] organize base, template data and code
- [x] initialize repository

## support dataset label
- [KITTI](https://www.cvlibs.net/datasets/kitti/eval_object.php?obj_benchmark=3d)
- [COCO](https://cocodataset.org/#download)

## requirements
```commandline
pip install pyquaternion pyyaml tqdm
```

## how to use
### arguments
```text
--input_label_path : user defined label location
--config_path : user defined label's configuration YAML file for parse
--output_label_dir : output directory for save converted label
--tgt_label_type : dataset/label type for convert user defined label(current support [KITTI, COCO])
```

### command line
```commandline
python main.py --input_label_path {user defined label path} 
               --config_path {configuration YAML file path} 
               --output_label_dir {directory path output saved} 
               --tgt_label_type {type for convert} 
```
