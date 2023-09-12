# userDFlabel_cvt
- convert user defined label to known dataset label(etc. KITTI, COCO)
- read configuration YAML file and parse user defined label architecture
## updates
### September 2023
- [x] add kitti converter
- [x] organize base, template data and code
- [x] initialize repository
## requirements
- pyquaternion
- pyyaml
## support dataset label
- KITTI
## how to use

### arguments
- --input_label_path :  
- --config_path :
- --output_label_dir :
- --tgt_label_type :
```commandline
python main.py --input_label_path --config_path --output_label_dir --tgt_label_type 
```
