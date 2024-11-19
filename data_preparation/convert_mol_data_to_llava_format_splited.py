import argparse
import copy
import os
from pathlib import Path
import json

# Example LLAVA format
#     ll = {
#         "id": "000000000113",
#         "image": "coco/train2017/000000000113.jpg",
#         "conversations": [
#             {
#                 "from": "human",
#                 "value": "What is this photo about'?\n<image>"
#             },
#             {
#                 "from": "gpt",
#                 "value": "The image depicts a man and a woman standing together near a large cake displayed on a dining table. The woman is cutting into the cake with a knife, while the man attentively stands behind her. They are surrounded by several cups placed on the table, which are likely to be used to serve drinks to celebrate the occasion.\n\nThere are two chairs in the scene, one of which is placed near the table and the other chair is positioned further back. It seems that the individuals are in the midst of an event or a celebration, as they happily cut the cake together."
#             }
#         ]
#     }

def convert_mol_data_to_llava_format_splited(data, max_cont=None):
    seq_records_train, seq_records_test = [], []
    split_types = set()
    for record in data:
        sample = {"id": record["metadata"]["protein_accession"],
                  "image": record["input"].strip("`\n"),
                  "conversations": []}
        sample["conversations"].append({
            "from": "human",
            "value": f"{record['instruction']}\n<image>"})
        sample["conversations"].append({
            "from": "gpt",
            "value": record["output"]})

        split_types.add(record['metadata']['split'])
        if record['metadata']['split'] == "train":
            seq_records_train.append(copy.deepcopy(sample))
        else:
            seq_records_test.append(copy.deepcopy(sample))

        if max_cont:
            if len(seq_records_train) > max_cont:
                break
    print("Count data:\t", len(seq_records_train))
    print(f"Split types {split_types}")
    return seq_records_train, seq_records_test


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--src_path', type=str, help='path to src .json')
    parser.add_argument('--result_dir', type=str, help='path to result file .json')
    parser.add_argument('--count', nargs='?', type=int, const=0, help='max count records to preproc')
    args = parser.parse_args()

    max_record = args.count if args.count else None
    with open(args.src_path) as f:
        data_all = json.load(f)

    train, test = convert_mol_data_to_llava_format(data_all, max_record)

    name_data = os.path.basename(args.src_path)
    os.makedirs(args.result_dir, exist_ok=True)
    path_train = os.path.join(args.result_dir, f"train_{name_data}")
    path_test = os.path.join(args.result_dir, f"test_{name_data}")

    with open(path_train, "w", encoding="utf-8") as file:
        json.dump(train, fp=file, ensure_ascii=False, indent=4)
    print(f"Train count samples: {len(train)}\nSaved to {path_train}\n")
    with open(path_test, "w", encoding="utf-8") as file:
        json.dump(test, fp=file, ensure_ascii=False, indent=4)
    print(f"Test count samples: {len(test)}\nSaved to {path_test}")
