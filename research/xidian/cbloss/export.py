# Copyright 2021 Huawei Technologies Co., Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ============================================================================

"""Export checkpoint file into air, mindir models"""
import os
import numpy as np
import mindspore as ms
import mindspore.nn as nn
from mindspore import Tensor, export, context
from model_utils.config import config
from model_utils.moxing_adapter import moxing_wrapper
from model_utils.device_adapter import get_device_id
from models.Resnet import resnet34


def modelarts_pre_process():
    '''modelarts pre process function.'''
    config.file_name = os.path.join(config.output_path, config.file_name)


@moxing_wrapper(pre_process=modelarts_pre_process)
def run_export():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    context.set_context(mode=context.GRAPH_MODE, device_target=config.device_target)
    if config.device_target == "Ascend":
        context.set_context(device_id=get_device_id())
    current_dir = os.path.dirname(os.path.abspath(__file__))
    model = resnet34(num_classes=config.num_classes)
    weight_path = os.path.join(current_dir, config.model_root, config.ckpt_file)
    model_dict = ms.load_checkpoint(weight_path)     
    ms.load_param_into_net(model,model_dict)   
    input_arr = Tensor(np.ones([config.batch_size, 3, config.image_height, config.image_width]), ms.float32)
    export(model, input_arr, file_name=config.file_name, file_format=config.file_format)



if __name__ == '__main__':
    run_export()
