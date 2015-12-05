from __future__ import absolute_import
from __future__ import unicode_literals
import base64
import engineData
import json
from layer_effects import layer_effects_details
import os
import os.path
from psd_tools import PSDImage
import psd_tools.decoder
import psd_tools.reader
from psd_tools.user_api import pil_support
import random
import read_psd_layers
from sys import argv
import time

DATA_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'specsFiles')
path = '../specsFiles/06_list.psd';

def full_name(filename):
    return os.path.join(DATA_PATH, filename)

def load_psd(filename):
    with open(filename, 'rb') as f:
        return psd_tools.reader.parse(f, encoding='utf8')

def decode_psd(filename):
    return psd_tools.decoder.parse(load_psd(filename))

raw_data = decode_psd(path)
layers = read_psd_layers.group_layers(raw_data)
headers = raw_data.header

def psd_traverse(layers):
    for layer in layers:
        layer['blend_mode'] = str(layer['blend_mode'])[2:-1]


        timestamp = str(int(time.time()))
        layer_image_path = path + timestamp + ".png"

        if layer['mask_data']:
            layer['mask_data'] = {
                'top': layer['mask_data'].top,
                'left': layer['mask_data'].left,
                'bottom': layer['mask_data'].bottom,
                "right": layer['mask_data'].right,
                'background_color': layer['mask_data'].background_color,
                'flags': {'pos_relative_to_layer': layer['mask_data'].flags.pos_relative_to_layer,
                    'mask_disabled': layer['mask_data'].flags.mask_disabled,
                    'invert_mask': layer['mask_data'].flags.invert_mask,
                    'user_mask_from_render': layer['mask_data'].flags.user_mask_from_render,
                    'parameters_applied': layer['mask_data'].flags.parameters_applied, }

                }

        while os.path.isfile(layer_image_path):
            layer_image_path = path + timestamp + str(random.randint(0, 1000)) + ".png"

        try:
            layer_image = pil_support.extract_layer_image(raw_data, layer['index'])
            layer_image.save(layer_image_path)

            with open(layer_image_path, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read())
                layer['image'] = str(encoded_string)[2:-1]
                
            os.remove(layer_image_path)
        except:
            pass

        if 'layers' in layer:
            psd_traverse(layer['layers'])
        else:
            pass

psd_traverse(layers)


psd_info = {}
psd_info['header'] = {}
if headers.number_of_channels is not None:
    psd_info['header']['number_of_channels'] = headers.number_of_channels
if headers.height is not None:
    psd_info['header']['height'] = headers.height
if headers.width is not None:
    psd_info['header']['width'] = headers.width
if headers.depth is not None:
    psd_info['header']['depth'] = headers.depth
if headers.color_mode is not None:
    psd_info['header']['color_mode'] = headers.color_mode
psd_info['layers'] = layers;
psd_final_data = []
psd_final_data.append(psd_info)

#os.remove(path + argv[1])

print (json.dumps(psd_info))