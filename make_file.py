from mxnet import gluon
import mxnet as mx
# import boto3
import numpy as np
import json
from gluoncv import model_zoo, data, utils
from gluoncv.utils import export_block

net = model_zoo.get_model('ssd_512_mobilenet1.0_voc', pretrained=True)

export_block('new_ssd_512_mobilenet1.0_voc', net, preprocess=True, layout='HWC')

