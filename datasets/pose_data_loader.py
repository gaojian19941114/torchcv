#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Donny You(donnyyou@163.com)
# Class for the Pose Data Loader.


from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
from torch.utils import data

from datasets.pose.cpm_data_loader import CPMDataLoader
from datasets.pose.op_data_loader import OPDataLoader
import datasets.tools.pil_aug_transforms as pil_aug_trans
import datasets.tools.cv2_aug_transforms as cv2_aug_trans
import datasets.tools.transforms as trans
from datasets.tools.collate_functions import CollateFunctions
from utils.tools.logger import Logger as Log


class PoseDataLoader(object):

    def __init__(self, configer):
        self.configer = configer

        if self.configer.get('data', 'image_tool') == 'pil':
            self.aug_train_transform = pil_aug_trans.PILAugCompose(self.configer, split='train')
        elif self.configer.get('data', 'image_tool') == 'cv2':
            self.aug_train_transform = cv2_aug_trans.CV2AugCompose(self.configer, split='train')
        else:
            Log.error('Not support {} image tool.'.format(self.configer.get('data', 'image_tool')))
            exit(1)

        if self.configer.get('data', 'image_tool') == 'pil':
            self.aug_val_transform = pil_aug_trans.PILAugCompose(self.configer, split='val')
        elif self.configer.get('data', 'image_tool') == 'cv2':
            self.aug_val_transform = cv2_aug_trans.CV2AugCompose(self.configer, split='val')
        else:
            Log.error('Not support {} image tool.'.format(self.configer.get('data', 'image_tool')))
            exit(1)

        self.img_transform = trans.Compose([
            trans.ToTensor(),
            trans.Normalize(div_value=self.configer.get('normalize', 'div_value'),
                            mean=self.configer.get('normalize', 'mean'),
                            std=self.configer.get('normalize', 'std')), ])

    def get_trainloader(self):
        if self.configer.get('method') == 'conv_pose_machine':
            trainloader = data.DataLoader(
                CPMDataLoader(root_dir=os.path.join(self.configer.get('data', 'data_dir'), 'train'),
                              aug_transform=self.aug_train_transform,
                              img_transform=self.img_transform,
                              configer=self.configer),
                batch_size=self.configer.get('train', 'batch_size'), shuffle=True,
                num_workers=self.configer.get('data', 'workers'), pin_memory=True,
                collate_fn=lambda *args: CollateFunctions.default_collate(
                    *args, data_keys=['img', 'heatmap']
                )
            )

            return trainloader

        elif self.configer.get('method') == 'open_pose':
            trainloader = data.DataLoader(
                OPDataLoader(root_dir=os.path.join(self.configer.get('data', 'data_dir'), 'train'),
                             aug_transform=self.aug_train_transform,
                             img_transform=self.img_transform,
                             configer=self.configer),
                batch_size=self.configer.get('train', 'batch_size'), shuffle=True,
                num_workers=self.configer.get('data', 'workers'), pin_memory=True,
                collate_fn=lambda *args: CollateFunctions.default_collate(
                    *args, data_keys=['img', 'maskmap', 'heatmap', 'vecmap']
                )
            )

            return trainloader

        else:
            Log.error('Method: {} loader is invalid.'.format(self.configer.get('method')))
            return None

    def get_valloader(self):
        if self.configer.get('method') == 'conv_pose_machine':
            valloader = data.DataLoader(
                CPMDataLoader(root_dir=os.path.join(self.configer.get('data', 'data_dir'), 'val'),
                              aug_transform=self.aug_val_transform,
                              img_transform=self.img_transform,
                              configer=self.configer),
                batch_size=self.configer.get('val', 'batch_size'), shuffle=False,
                num_workers=self.configer.get('data', 'workers'), pin_memory=True,
                collate_fn=lambda *args: CollateFunctions.default_collate(
                    *args, data_keys=['img', 'heatmap']
                )
            )

            return valloader

        elif self.configer.get('method') == 'open_pose':
            valloader = data.DataLoader(
                OPDataLoader(root_dir=os.path.join(self.configer.get('data', 'data_dir'), 'val'),
                             aug_transform=self.aug_val_transform,
                             img_transform=self.img_transform,
                             configer=self.configer),
                batch_size=self.configer.get('val', 'batch_size'), shuffle=False,
                collate_fn=lambda *args: CollateFunctions.default_collate(
                    *args, data_keys=['img', 'maskmap', 'heatmap', 'vecmap']
                )
            )

            return valloader

        else:
            Log.error('Method: {} loader is invalid.'.format(self.configer.get('method')))
            return None


if __name__ == "__main__":
    # Test data loader.
    pass