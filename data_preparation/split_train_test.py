import argparse
import json
import os

from sklearn.model_selection import train_test_split

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--src_path', type=str, help='path to src .json')
    parser.add_argument('--result_dir', type=str, help='path to result directory')
    parser.add_argument('--percent_test', nargs='?', type=float, const=0.05, help='Percent of test')
    args = parser.parse_args()

    name_data = os.path.basename(args.src_path)
    os.makedirs(args.result_dir, exist_ok=True)
    path_train = os.path.join(args.result_dir, f"train_{name_data}")
    path_test = os.path.join(args.result_dir, f"test_{name_data}")

    with open(args.src_path) as f:
        data_all = json.load(f)

    train, test = train_test_split(data_all, test_size=args.percent_test, random_state=56, shuffle=True)

    with open(path_train, "w", encoding="utf-8") as file:
        json.dump(train, fp=file, ensure_ascii=False, indent=4)
    print(f"Saved to {path_train}")
    with open(path_test, "w", encoding="utf-8") as file:
        json.dump(test, fp=file, ensure_ascii=False, indent=4)
    print(f"Saved to {path_test}")
