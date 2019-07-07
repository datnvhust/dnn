from util import csv2dict, tsv2dict
import numpy as np
from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import train_test_split, KFold
from dnn_model import some_collections


samples = csv2dict("../data/features.csv")

rvsm_list = [float(sample["rVSM_similarity"]) for sample in samples]

sample_dict, bug_reports, bug_reports_files_dict = some_collections(samples, True)

topk_counters = [0] * 20
negative_total = 0
for bug_report in bug_reports:
    dnn_input = []
    corresponding_files = []
    bug_id = bug_report["id"]

    try:
        for temp_dict in sample_dict[bug_id]:
            key = list(temp_dict.keys())[0]
            value = list(temp_dict.values())[0]
            dnn_input.append(value)
            corresponding_files.append(key)
    except:
        negative_total += 1
        continue

    relevancy_list = np.array(dnn_input).ravel()

    for i in range(1, 21):
        max_indices = np.argpartition(relevancy_list, -i)[-i:]
        for corresponding_file in np.array(corresponding_files)[max_indices]:
            if str(corresponding_file) in bug_reports_files_dict[bug_id]:
                topk_counters[i - 1] += 1
                break

acc_dict = {}
for i, counter in enumerate(topk_counters):
    acc = counter / (len(bug_reports) - negative_total)
    acc_dict[i + 1] = round(acc, 3)

print(acc_dict)
