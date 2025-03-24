import argparse
import os
import json
import evaluate


def create_id_map(dir_):
    p_map_path = os.path.join(dir_, "id_map_all.json")
    if p_map_path in os.listdir(dir_):
        with open(p_map_path, "r", encoding="utf8") as fp:
            id2domain_map = json.load(fp)
        print(f"ID map loaded from {p_map_path}")
        return id2domain_map

    result = []
    for file_ in os.listdir(dir_):
        if file_.endswith(".json") and 'protein_design.json' not in file_ and "id_map_all.json" not in file_:
            print(f"load {file_}")
            with open(os.path.join(dir_, file_), 'r') as f:
                result.extend(json.load(f))

    id2domain_map = {}
    for sample in result:
        # if sample["metadata"]['split'] == "test":
        id = sample["metadata"]["protein_accession"]
        domain = sample["metadata"]["task"]
        output = sample["output"]
        id2domain_map[id] = (domain, output)

    with open(p_map_path, "w") as fp:
        json.dump(p_map_path, fp, ensure_ascii=False)
    return id2domain_map


def calc_metrics(args):
    with open(args.answers_path, 'r') as fp:
        answers = [json.loads(l) for l in fp]
    id_map = create_id_map(args.data_dir)
    # по question_id определить к какой задаче относится
    by_domain = {}
    for sample in answers:
        dom, ref_out = id_map[sample["question_id"]]
        res_ans = sample["text"]
        if dom not in by_domain:
            by_domain[dom] = {"y": [], "y_pred": []}
        by_domain[dom]["y"].append(ref_out)
        by_domain[dom]["y_pred"].append(res_ans)

    # посчитать метрику по каждому домену задач
    rouge = evaluate.load("rouge")
    for domain in by_domain:
        results = rouge.compute(predictions=by_domain[domain]['y_pred'],
                                references=by_domain[domain]['y'])
        print(f"Domain:\t{domain}\n{results}")
        print()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", type=str, default="data/")
    parser.add_argument("--answers-path", type=str, default="answer.jsonl")
    args = parser.parse_args()

    calc_metrics(args)
