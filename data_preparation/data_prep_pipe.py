import argparse
import json
import os

from sklearn.model_selection import train_test_split

from convert_mol_data_to_llava_format import convert_mol_data_to_llava_format


def merge_jsons(dir_, save_file):
    result = []
    for file_ in os.listdir(dir_):
        if file_.endswith(".json"):
            with open(os.path.join(dir_, file_), 'r') as f:
                result.extend(json.load(f))

    with open(save_file, 'w') as output_file:
        json.dump(result, output_file)
    print(f"Files from {dir_} merged to {save_file}")
    print(f"Total samples in {save_file}:\t{len(result)}")


def write_test_train(train_, test_, result_dir, file_name_):
    test_dir = os.path.join(result_dir, "test")
    train_dir = os.path.join(result_dir, "train")
    os.makedirs(test_dir, exist_ok=True)
    os.makedirs(train_dir, exist_ok=True)
    path_train = os.path.join(train_dir, file_name_)
    path_test = os.path.join(test_dir, file_name_)

    with open(path_train, "w", encoding="utf-8") as file:
        json.dump(train_, fp=file, ensure_ascii=False, indent=4)
    print(f"Train count samples: {len(train)}\nSaved to {path_train}")
    with open(path_test, "w", encoding="utf-8") as file:
        json.dump(test_, fp=file, ensure_ascii=False, indent=4)
    print(f"Test count samples: {len(test)}\nSaved to {path_test}\n")
    return train_dir, test_dir


def write_llava_format(data_, result_dir, file_name_):
    llava_dir = os.path.join(result_dir, "llava_format")
    os.makedirs(llava_dir, exist_ok=True)
    path_ = os.path.join(llava_dir, file_name_)

    with open(path_, "w", encoding="utf-8") as file:
        json.dump(data_, fp=file, ensure_ascii=False, indent=4)
    print(f"Llava format count samples: {len(data_)}\nSaved to {path_}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--src_dir', type=str, help='path to src .xml')
    parser.add_argument('--result_dir', type=str, help='path to result file .json')
    parser.add_argument('--count', nargs='?', type=int, const=0, help='max count records to preproc')
    parser.add_argument('--percent_test', nargs='?', type=float, const=0.05, help='Percent of test')

    args = parser.parse_args()

    for file_name in os.listdir(args.src_dir):
        if file_name.endswith(".json") and file_name != 'protein_design.json':
            print(f"Start prepare file {file_name}")
            try:
                file_path = os.path.join(args.src_dir, file_name)
                with open(file_path) as f:
                    data = json.load(f)

                llava_format = convert_mol_data_to_llava_format(data, args.count)
                write_llava_format(llava_format, args.result_dir, file_name)
                train, test = train_test_split(llava_format, test_size=args.percent_test, random_state=56, shuffle=True)
                train_dir, test_dir = write_test_train(train, test, args.result_dir, file_name)
            except Exception as e:
                raise Exception(f"Wrong data. Use protein data only.")

    merge_jsons(train_dir, os.path.join(args.result_dir, "train.json"))
    merge_jsons(test_dir, os.path.join(args.result_dir, "test.json"))
