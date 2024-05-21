#!/bin/bash

# IMPORTANT: this is the training script for the original LLaVA, NOT FOR LLaVA V1.5!

# Uncomment and set the following variables correspondingly to run this script:

# MODEL_VERSION=vicuna-v1-3-7b
# MODEL_VERSION=llama-2-7b-chat

########### DO NOT CHANGE ###########
########### USE THIS FOR BOTH ###########
PROMPT_VERSION=plain
########### DO NOT CHANGE ###########

deepspeed llava/train/train.py \
  --data_path="/Users//PycharmProjects/hse/data_protein/protein_data_mini_200k.json"
  --vision_tower_host="facebookresearch/esm:main"
  --vision_tower="esm2_t6_8M_UR50D"
  --tune_mm_mlp_adapter=True
  --mm_vision_select_layer=-2
  --mm_use_im_start_end=False
  --mm_use_im_patch_token=False
  --bf16=False
  --output_dir=./checkpoints/llava-protein
  --num_train_epochs=1
  --per_device_train_batch_size=16
  --per_device_eval_batch_size=4
  --gradient_accumulation_steps=1
  --evaluation_strategy="no"
  --save_strategy="steps"
  --save_steps=24000
  --save_total_limit=1
  --learning_rate=2e-3
  --weight_decay=0.
  --warmup_ratio=0.03
  --lr_scheduler_type="cosine"
  --logging_steps=1
  --tf32=False
  --model_max_length=2048
  --gradient_checkpointing=False
  --dataloader_num_workers=1
  --lazy_preprocess=False
