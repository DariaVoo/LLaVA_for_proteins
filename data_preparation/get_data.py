import copy
from Bio import SeqIO
import json
from tqdm import tqdm


if __name__ == '__main__':
    src_path = "/Users//PycharmProjects/LLaVA_for_proteins/data/uniprot_sprot.xml"
    jsonFilePath = "/Users//PycharmProjects/LLaVA_for_proteins/data/protein_data_mini_200k.json"

    seq_records = []
    count_not_function = 0
    total = 0
    with open(src_path) as input_handle:
        for record in tqdm(SeqIO.parse(input_handle, "uniprot-xml")):
            seq = str(record.seq)
            sample = {}
            if "comment_function" in record.annotations.keys():
                description = record.annotations["comment_function"]
                sample["id"] = record.id
                sample["sequence"] = seq
                sample["protein_function"] = description
                seq_records.append(copy.deepcopy(sample))
            else:
                count_not_function += 1

            total += 1
            if total > 200000:
                break

    print("Count no function proteins:\t", count_not_function)
    print("Count all:\t", len(seq_records))
    with open(jsonFilePath, "w", encoding="utf-8") as file:
        json.dump(seq_records, fp=file, ensure_ascii=False, indent=4)

