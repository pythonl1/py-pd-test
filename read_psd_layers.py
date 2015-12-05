# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals, print_function, division
import warnings

from psd_tools.constants import TaggedBlock, SectionDivider, BlendMode
from PIL.ImageOps import posterize
from PIL.ImageEnhance import Brightness
from symbol import if_stmt
from engineData import getFontAndColorDict


def group_layers(decoded_data):
    """
    Returns a nested dict with PSD layer group information.
    """
    layer_records = decoded_data.layer_and_mask_data.layers.layer_records

    root = dict(layers=[])
    group_stack = [root]
    font_sizeTuple = None
    text_data = {}

    
    filterFX = {
                'enabled' : '',
                'validAtPositon' : '',
                'filterMaskEnable' : '',
                'filterMaskLinked' : '',
                'filterMaskExtendWithWhite' : '',
                'filterFXlist' : [{
                                   'name' : '',
                                   'blendOptions' : {
                                                     'opacity' : {'value' : '', 'units' : ''},
                                                     'mode' : '',
                                                     'enabled' : '',
                                                     },
                                   'hasoptions' : '',
                                   'foregroundColor' : {
                                                       'red' : '',
                                                       'green' : '',
                                                       'blue' : ''
                                                        },
                                    'backgroundColor' : {
                                                         'red' : '',
                                                         'green' : '',
                                                         'blue' : ''
                                                         },
                                    'filter' : { 'radius': ''},
                                    'filterID' : ''
                                   
                                   }],
                }
    
    propDict = {'FontSet':'', 'Text':'', 'FontType':'', 'FontTypeA':'', 'FontSize':'', 'A':'', 'R':'', 'G':'', 'B':''}

    for index, layer in reversed(list(enumerate(layer_records))):
        current_group = group_stack[-1]

        blocks = dict(layer.tagged_blocks)
                
        
        name = blocks.get(TaggedBlock.UNICODE_LAYER_NAME, layer.name)
        layer_id = blocks.get(TaggedBlock.LAYER_ID)
        divider = blocks.get(
            TaggedBlock.SECTION_DIVIDER_SETTING,
            blocks.get(TaggedBlock.NESTED_SECTION_DIVIDER_SETTING),
        )

        levels = blocks.get(TaggedBlock.LEVELS)
        curves = blocks.get(TaggedBlock.CURVES)
        exposure = blocks.get(TaggedBlock.EXPOSURE)
        vibrance = blocks.get(TaggedBlock.VIBRANCE)
        hue_Saturation_4 = blocks.get(TaggedBlock.HUE_SATURATION_4)
        hue_saturation_5 = blocks.get(TaggedBlock.HUE_SATURATION_5)
        color_balance = blocks.get(TaggedBlock.COLOR_BALANCE)
        black_and_white = blocks.get(TaggedBlock.BLACK_AND_WHITE)
        photo_filter = blocks.get(TaggedBlock.PHOTO_FILTER)
        channel_mixer = blocks.get(TaggedBlock.CHANNEL_MIXER)
        invert = blocks.get(TaggedBlock.INVERT)
        posterize = blocks.get(TaggedBlock.POSTERIZE)
        threshold = blocks.get(TaggedBlock.THRESHOLD)
        selective_color = blocks.get(TaggedBlock.SELECTIVE_COLOR)
        
        
        reference_point = blocks.get(TaggedBlock.REFERENCE_POINT)
        animation_effects = blocks.get(TaggedBlock.ANIMATION_EFFECTS)
        annotations = blocks.get(TaggedBlock.ANNOTATIONS)
        blend_clipping_elements = blocks.get(TaggedBlock.BLEND_CLIPPING_ELEMENTS)
        blend_interior_elements = blocks.get(TaggedBlock.BLEND_INTERIOR_ELEMENTS)
        Brightness = blocks.get(TaggedBlock.BRIGHTNESS_AND_CONTRAST)
        channel_blending_restrictions_setting = blocks.get(TaggedBlock.CHANNEL_BLENDING_RESTRICTIONS_SETTING)
        content_generator_extra_Data = blocks.get(TaggedBlock.CONTENT_GENERATOR_EXTRA_DATA)
        effects_layer = blocks.get(TaggedBlock.EFFECTS_LAYER)
        filter_Effects1 = blocks.get(TaggedBlock.FILTER_EFFECTS1)
        filter_Effects2 = blocks.get(TaggedBlock.FILTER_EFFECTS2)
        filter_mask = blocks.get(TaggedBlock.FILTER_MASK)
        foreign_effect_ID = blocks.get(TaggedBlock.FOREIGN_EFFECT_ID)
        layer_res = blocks.get(TaggedBlock.LAYER)
        layer_res_16 = blocks.get(TaggedBlock.LAYER_16)
        layer_res_32 = blocks.get(TaggedBlock.LAYER_32)
        layer_mask_as_global_mask = blocks.get(TaggedBlock.LAYER_MASK_AS_GLOBAL_MASK)
        layer_name_source_setting = blocks.get(TaggedBlock.LAYER_NAME_SOURCE_SETTING)
        layer_version = blocks.get(TaggedBlock.LAYER_VERSION)
        linked_layer_1 = blocks.get(TaggedBlock.LINKED_LAYER1)
        linked_layer_2 = blocks.get(TaggedBlock.LINKED_LAYER2)
        linked_layer_3 = blocks.get(TaggedBlock.LINKED_LAYER3)
        metadata_setting = blocks.get(TaggedBlock.METADATA_SETTING)
        object_based_effects_layer_info = blocks.get(TaggedBlock.OBJECT_BASED_EFFECTS_LAYER_INFO)
        pattern_data = blocks.get(TaggedBlock.PATTERN_DATA)
        pattern_fill_setting = blocks.get(TaggedBlock.PATTERN_FILL_SETTING)
        pattern_1 = blocks.get(TaggedBlock.PATTERNS1)
        pattern_2 = blocks.get(TaggedBlock.PATTERNS2)
        pattern_3 = blocks.get(TaggedBlock.PATTERNS3)
        placed_layer_data = blocks.get(TaggedBlock.PLACED_LAYER_DATA)
        placed_layer_obsolete_1 = blocks.get(TaggedBlock.PLACED_LAYER_OBSOLETE1)
        placed_layer_obsolete_2 = blocks.get(TaggedBlock.PLACED_LAYER_OBSOLETE2)
        protected_setting = blocks.get(TaggedBlock.PROTECTED_SETTING)
        saving_merged_transparency = blocks.get(TaggedBlock.SAVING_MERGED_TRANSPARENCY)
        saving_merged_transparency_16 = blocks.get(TaggedBlock.SAVING_MERGED_TRANSPARENCY16)
        saving_merged_transparency_32 = blocks.get(TaggedBlock.SAVING_MERGED_TRANSPARENCY32)
        sheet_color_setting = blocks.get(TaggedBlock.SHEET_COLOR_SETTING)
        smart_object_placed_layer_data = blocks.get(TaggedBlock.SMART_OBJECT_PLACED_LAYER_DATA)
        solid_color_sheet_setting = blocks.get(TaggedBlock.SOLID_COLOR_SHEET_SETTING)
        transparency_shapes_layer = blocks.get(TaggedBlock.TRANSPARENCY_SHAPES_LAYER)



        type_tool_info = blocks.get(TaggedBlock.TYPE_TOOL_INFO)
        type_tool_object_setting = blocks.get(TaggedBlock.TYPE_TOOL_OBJECT_SETTING)
        
        
            
        
        if (type_tool_object_setting != None):
            # text tranform data
            transform_data = {'xx' : type_tool_object_setting.xx,
                         'xy' : type_tool_object_setting.xy,
                         'yx' : type_tool_object_setting.yx,
                         'yy' : type_tool_object_setting.yy,
                         'tx' : type_tool_object_setting.tx,
                         'ty' : type_tool_object_setting.ty
                         }
            # layer type
            if (blocks.get(b'TySh').text_data.classID == b'TxLr') :
                LayerType = 'Text Layer'
                print (LayerType)
                
            text_data_list = type_tool_object_setting.text_data.items
            textDataTuple = [tup[1] for tup in text_data_list]
            
            # text key
            textKey = textDataTuple[0].value
            
            # to get the dict with font name and size
            textDataTuplekey = [tup[1] for tup in text_data_list]
            textDataTuple.reverse()
            font_s = textDataTuple[0].value
            font_det = getFontAndColorDict(propDict, font_s)
            f =open ('text.json', 'a')
            f.write(str(font_s))
            f.close()
            propDict = {'FontSet':'', 'Text':'', 'FontType':'', 'FontTypeA':'', 'FontSize':'', 'A':'', 'R':'', 'G':'', 'B':''}
            
            # boundingBox values for text data
            #boundingbox_data = str(textDataTuple[2].items)
            
            # to get bounds for the text data
            #bounds_data = str(textDataTuple[3].items)
            
            # to get the orientation of the text 
            if textDataTuple[5].value == b'Hrzn' :
                Orientation_data = 'Horizontal'
            text_data = {'TextKey' : textKey,
                    #'boundingBox' : boundingbox_data,
                    #'bounds' : bounds_data,
                    'textShape' : [{
                                    'orientation' : Orientation_data,
                                    'transform' : transform_data,
                                    }],
                    'textStyleRange' : [{
                                         'textstyle' : font_det,
                                         }] 
                    }
        else:
            text_data = None
            
            
        text_engine_data = blocks.get(TaggedBlock.TEXT_ENGINE_DATA)

        path_name = blocks.get(TaggedBlock.UNICODE_PATH_NAME)
        user_mask = blocks.get(TaggedBlock.USER_MASK)
        using_aligned_rendering = blocks.get(TaggedBlock.USING_ALIGNED_RENDERING)
        vector_mask_as_global_mask = blocks.get(TaggedBlock.VECTOR_MASK_AS_GLOBAL_MASK)
        vector_mask_Setting_1 = blocks.get(TaggedBlock.VECTOR_MASK_SETTING1)
        vector_mask_Setting_2 = blocks.get(TaggedBlock.VECTOR_MASK_SETTING2)
        vector_origination_data = blocks.get(TaggedBlock.VECTOR_ORIGINATION_DATA)
        vector_stroke_content_data = blocks.get(TaggedBlock.VECTOR_STROKE_CONTENT_DATA)
        vector_stroke_data = blocks.get(TaggedBlock.VECTOR_STROKE_DATA)
        
        
        
        
        visible = layer.flags.visible
        opacity = layer.opacity
        blend_mode = layer.blend_mode
        mask_data = layer.mask_data        
        channels = layer.channels

        if divider is not None:
            # group information
            if divider.type in [SectionDivider.CLOSED_FOLDER, SectionDivider.OPEN_FOLDER]:
                # group begins
                group = dict(
                    id=layer_id,
                    index=index,
                    name=name,
                    layers=[],
                    closed=divider.type == SectionDivider.CLOSED_FOLDER,

                    blend_mode=blend_mode,
                    visible=visible,
                    mask_data=mask_data,
                    channels=channels,
                    


                    opacity=opacity,
                    levels=levels,
                    curves=curves,
                    exposure=exposure,
                    vibrance=vibrance,
                    hue_Saturation_4=hue_Saturation_4,
                    hue_saturation_5=hue_saturation_5,
                    color_balance=color_balance,
                    black_and_white=black_and_white,
                    photo_filter=photo_filter,
                    channel_mixer=channel_mixer,
                    invert=invert,
                    posterize=posterize,
                    threshold=threshold,
                    selective_color=selective_color,
                    
                    reference_point=str(reference_point),
                    animation_effects=str(animation_effects),
                    annotations=str(annotations),
                    blend_clipping_elements=str(blend_clipping_elements),
                    blend_interior_elements=str(blend_interior_elements),
                    Brightness=str(Brightness),
                    channel_blending_restrictions_setting=str(channel_blending_restrictions_setting),
                    content_generator_extra_Data=str(content_generator_extra_Data),
                    effects_layer=str(effects_layer),
                    filter_Effects1=str(filter_Effects1),
                    filter_Effects2=str(filter_Effects2),
                    filter_mask=str(filter_mask),
                    foreign_effect_ID=str(foreign_effect_ID),
                    layer_res=str(layer_res),
                    layer_res_16=str(layer_res_16),
                    layer_res_32=str(layer_res_32),
                    layer_mask_as_global_mask=str(layer_mask_as_global_mask),
                    layer_name_source_setting=str(layer_name_source_setting),
                    layer_version=str(layer_version),
                    linked_layer_1=str(linked_layer_1),
                    linked_layer_2=str(linked_layer_2),
                    linked_layer_3=str(linked_layer_3),
                    metadata_setting=str(str(metadata_setting)),
                    object_based_effects_layer_info=str(object_based_effects_layer_info),
                    pattern_data=str(pattern_data),
                    pattern_fill_setting=str(pattern_fill_setting),
                    pattern_1=str(pattern_1),
                    pattern_2=str(pattern_2),
                    pattern_3=str(pattern_3),
                    placed_layer_data=str(placed_layer_data),
                    placed_layer_obsolete_1=str(placed_layer_obsolete_1),
                    placed_layer_obsolete_2=str(placed_layer_obsolete_2),
                    protected_setting=str(protected_setting),
                    saving_merged_transparency=str(saving_merged_transparency),
                    saving_merged_transparency_16=str(saving_merged_transparency_16),
                    saving_merged_transparency_32=str(saving_merged_transparency_32),
                    sheet_color_setting=str(sheet_color_setting),
                    smart_object_placed_layer_data=str(smart_object_placed_layer_data),
                    solid_color_sheet_setting=str(solid_color_sheet_setting),
                    transparency_shapes_layer=str(transparency_shapes_layer),

                    path_name=str(path_name),
                    user_mask=str(user_mask),
                    using_aligned_rendering=str(using_aligned_rendering),
                    vector_mask_as_global_mask=str(vector_mask_as_global_mask),
                    vector_mask_Setting_1=str(vector_mask_Setting_1),
                    vector_mask_Setting_2=str(vector_mask_Setting_2),
                    vector_origination_data=str(vector_origination_data),
                    vector_stroke_content_data=str(vector_stroke_content_data),
                    vector_stroke_data=str(vector_stroke_data),
                )
                group_stack.append(group)
                current_group['layers'].append(group)

            elif divider.type == SectionDivider.BOUNDING_SECTION_DIVIDER:
                # group ends

                if len(group_stack) == 1:
                    # This means that there is a BOUNDING_SECTION_DIVIDER
                    # without an OPEN_FOLDER before it. Create a new group
                    # and move layers to this new group in this case.

                    # Assume the first layer is a group
                    # and convert it to a group:
                    layers = group_stack[0]['layers']
                    group = layers[0]

                    # group doesn't have coords:
                    for key in 'top', 'left', 'bottom', 'right':
                        if key in group:
                            del group[key]

                    group['layers'] = layers[1:]
                    group['closed'] = False

                    # replace moved layers with newly created group:
                    group_stack[0]['layers'] = [group]

                else:
                    finished_group = group_stack.pop()
                    assert finished_group is not root

            else:
                warnings.warn("invalid state")
        else:
            # layer with image

            current_group['layers'].append(dict(
                id=layer_id,
                index=index,
                name=name,

                top=layer.top,
                left=layer.left,
                bottom=layer.bottom,
                right=layer.right,

                blend_mode=blend_mode,
                visible=visible,
                opacity=opacity,
                mask_data=mask_data,
                channels=channels,
                
                    
                levels=levels,
                curves=curves,
                exposure=exposure,
                vibrance=vibrance,
                hue_Saturation_4=hue_Saturation_4,
                hue_saturation_5=hue_saturation_5,
                color_balance=color_balance,
                black_and_white=black_and_white,
                photo_filter=photo_filter,
                channel_mixer=channel_mixer,
                invert=invert,
                posterize=posterize,
                threshold=threshold,
                selective_color=selective_color,
                
                reference_point=str(reference_point),
                animation_effects=str(animation_effects),
                annotations=str(annotations),
                blend_clipping_elements=str(blend_clipping_elements),
                blend_interior_elements=str(blend_interior_elements),
                Brightness=str(Brightness),
                channel_blending_restrictions_setting=str(channel_blending_restrictions_setting),
                content_generator_extra_Data=str(content_generator_extra_Data),
                effects_layer=str(effects_layer),
                filter_Effects1=str(filter_Effects1),
                filter_Effects2=str(filter_Effects2),
                filter_mask=str(filter_mask),
                foreign_effect_ID=str(foreign_effect_ID),
                layer_res=str(layer_res),
                layer_res_16=str(layer_res_16),
                layer_res_32=str(layer_res_32),
                layer_mask_as_global_mask=str(layer_mask_as_global_mask),
                layer_name_source_setting=str(layer_name_source_setting),
                layer_version=str(layer_version),
                linked_layer_1=str(linked_layer_1),
                linked_layer_2=str(linked_layer_2),
                linked_layer_3=str(linked_layer_3),
                metadata_setting=str(str(metadata_setting)),
                object_based_effects_layer_info=str(object_based_effects_layer_info),
                pattern_data=str(pattern_data),
                pattern_fill_setting=str(pattern_fill_setting),
                pattern_1=str(pattern_1),
                pattern_2=str(pattern_2),
                pattern_3=str(pattern_3),
                placed_layer_data=str(placed_layer_data),
                placed_layer_obsolete_1=str(placed_layer_obsolete_1),
                placed_layer_obsolete_2=str(placed_layer_obsolete_2),
                protected_setting=str(protected_setting),
                saving_merged_transparency=str(saving_merged_transparency),
                saving_merged_transparency_16=str(saving_merged_transparency_16),
                saving_merged_transparency_32=str(saving_merged_transparency_32),
                sheet_color_setting=str(sheet_color_setting),
                smart_object_placed_layer_data=str(smart_object_placed_layer_data),
                solid_color_sheet_setting=str(solid_color_sheet_setting),
                text_engine_data=str(text_engine_data),
                transparency_shapes_layer=str(transparency_shapes_layer),
                type_tool_info=str(type_tool_info),
                # type_tool_object_setting = str(type_tool_object_setting),
                
                text = text_data,
                
                path_name=str(path_name),
                user_mask=str(user_mask),
                using_aligned_rendering=str(using_aligned_rendering),
                vector_mask_as_global_mask=str(vector_mask_as_global_mask),
                vector_mask_Setting_1=str(vector_mask_Setting_1),
                vector_mask_Setting_2=str(vector_mask_Setting_2),
                vector_origination_data=str(vector_origination_data),
                vector_stroke_content_data=str(vector_stroke_content_data),
                vector_stroke_data=str(vector_stroke_data),
            ))

    return root['layers']
