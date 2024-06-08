import copy
from Bio import SeqIO
import json
from tqdm import tqdm

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

if __name__ == '__main__':
    src_path = "/Users//PycharmProjects/LLaVA_for_proteins/data/uniprot_sprot.xml"
    jsonFilePath = "/Users//PycharmProjects/LLaVA_for_proteins/data/protein_data_mini_2k_llava.json"

    seq_records = []
    count_not_function = 0
    total = 0
    with open(src_path) as input_handle:
        for record in tqdm(SeqIO.parse(input_handle, "uniprot-xml")):
            seq = str(record.seq)
            sample = {}
            if "comment_function" in record.annotations.keys():
                description = record.annotations["comment_function"]
                description = "\n".join(description)
                sample["id"] = record.id
                sample["image"] = seq
                sample["conversations"] = []
                sample["conversations"].append({
                    "from": "human",
                    "value": "Describe the function of this protein\n<image>"})
                sample["conversations"].append({
                    "from": "gpt",
                    "value": description})

                seq_records.append(copy.deepcopy(sample))
            else:
                count_not_function += 1

            total += 1
            if total > 2000:
                break

    print("Count no function proteins:\t", count_not_function)
    print("Count all:\t", len(seq_records))
    with open(jsonFilePath, "w", encoding="utf-8") as file:
        json.dump(seq_records, fp=file, ensure_ascii=False, indent=4)

