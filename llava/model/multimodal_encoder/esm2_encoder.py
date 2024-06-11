import torch
import torch.nn as nn

from transformers import EsmConfig


class ESMTower(nn.Module):
    def __init__(self, protein_model_host, protein_model_version, args, delay_load=False):
        super().__init__()

        self.vision_tower = None
        self.protein_processor = None
        self.is_loaded = False
        self.device = torch.device('cpu')
        self.dtype = torch.float32

        self.protein_model_host = protein_model_host
        self.protein_model_version = protein_model_version
        self.vision_tower_name = protein_model_version
        self.select_layer = args.mm_vision_select_layer
        self.select_feature = getattr(args, 'mm_vision_select_feature', 'patch')

        if not delay_load:
            self.load_model()
        elif getattr(args, 'unfreeze_mm_vision_tower', False):
            self.load_model()
        else:
            self.cfg_only = EsmConfig.from_pretrained(f'facebook/{self.vision_tower_name}')

        self.config = EsmConfig.from_pretrained(f'facebook/{self.vision_tower_name}')

    def load_model(self, device_map=None):
        if self.is_loaded:
            print('{} is already loaded, `load_model` called again, skipping.'.format(self.vision_tower_name))
            return

        self.vision_tower, self.protein_processor = torch.hub.load(self.protein_model_host, self.protein_model_version)
        if device_map is not None:
            self.vision_tower.to(device_map)
            self.device = device_map

        self.vision_tower.requires_grad_(False)

        self.is_loaded = True

    def feature_select(self, image_forward_outs):
        image_features = image_forward_outs.hidden_states[self.select_layer]
        if self.select_feature == 'patch':
            image_features = image_features[:, 1:]
        elif self.select_feature == 'cls_patch':
            image_features = image_features
        else:
            raise ValueError(f'Unexpected select feature: {self.select_feature}')
        return image_features

    @torch.no_grad()
    def forward(self, sequences):
        # todo
        if type(sequences) is list:
            image_features = []
            for seq in sequences:
                # todo .to(device=self.device, dtype=self.dtype)
                protein_forward_out = self.vision_tower(seq.unsqueeze(0))
                protein_feature = self.feature_select(protein_forward_out).to(seq.dtype)
                image_features.append(protein_feature)
        else:
            # todo .to(device=self.device, dtype=self.dtype)
            image_forward_outs = self.vision_tower(sequences)
            image_features = self.feature_select(image_forward_outs).to(sequences.dtype)

        return image_features

    @property
    def dummy_feature(self):
        return torch.zeros(1, self.hidden_size, device=self.device, dtype=self.dtype)

    # @property
    # def dtype(self):
    #     return self.vision_tower.dtype
    #
    # @property
    # def device(self):
    #     return self.vision_tower.device


    @property
    def hidden_size(self):
        return self.config.hidden_size

    @property
    def num_patches_per_side(self):
        return self.config.image_size // self.config.patch_size

    @property
    def num_patches(self):
        return (self.config.image_size // self.config.patch_size) ** 2
