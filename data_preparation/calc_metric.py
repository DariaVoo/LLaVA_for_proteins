import argparse
import os
import json
from ignite.metrics import RougeL


def create_id_map(dir_):
    result = []
    for file_ in os.listdir(dir_):
        if file_.endswith(".json"):
            with open(os.path.join(dir_, file_), 'r') as f:
                result.extend(json.load(f))

    id2domain_map = {}
    for sample in result:
        id = sample["metadata"]["protein_accession"]
        domain = sample["metadata"]["task"]
        output = sample["metadata"]["output"]
        id2domain_map[id] = (domain, output)
    return id2domain_map


def calc_metrics(args):
    with open(args.answers_path, 'r') as fp:
        answers = json.load(fp)
    id_map = create_id_map(args.data_dir)
    # по question_id определить к какой задаче относится
    by_domain = {}
    for sample in answers:
        dom, ref_out = id_map[sample["question_id"]]
        res_ans = sample["text"]
        if dom not in by_domain:
            by_domain[dom] = {"y": [], "y_pred": []}
        by_domain[dom]["y"].append(ref_out.split())
        by_domain[dom]["y_pred"].append(res_ans.split())

    # посчитать метрику по каждому домену задач
    m = RougeL(multiref="best")
    for domain in by_domain:
        m.update(by_domain[domain])
    print(m.compute())


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", type=str, default="data/")
    parser.add_argument("--answers-path", type=str, default="answer.jsonl")
    args = parser.parse_args()

    calc_metrics(args)
