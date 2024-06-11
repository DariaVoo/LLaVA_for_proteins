import argparse
import copy
import os
from pathlib import Path

from Bio import SeqIO
import json
from tqdm import tqdm


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--src_path', type=str, help='path to src .xml')
    parser.add_argument('--result_path', type=str, help='path to result file .json')
    parser.add_argument('--count', nargs='?', type=int, const=0, help='max count records to preproc')
    args = parser.parse_args()

    max_record = args.count if args.count else None

    seq_records = []
    count_not_function = 0
    total = 0
    with open(args.src_path) as input_handle:
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
            if max_record:
                if total > max_record:
                    break

    print("Count no function proteins:\t", count_not_function)
    print("Count proteins with functions:\t", len(seq_records))
    path = Path(args.result_path)
    os.makedirs(path.parent.absolute(), exist_ok=True)
    with open(args.result_path, "w", encoding="utf-8") as file:
        json.dump(seq_records, fp=file, ensure_ascii=False, indent=4)

