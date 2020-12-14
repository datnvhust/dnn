""" 
A script for feature extraction.

Used many modified and intact code blocks from 
'https://github.com/jeffrey-palmerino/BugLocalizationDNN'
"""

from util import *
from joblib import Parallel, delayed, cpu_count
import csv
import os
from datasets import DATASET
from datetime import datetime


def extract(i, br, bug_reports, java_src_dict):
    """ Extracts features for 50 wrong(randomly chosen) files for each
        right(buggy) file for the given bug report.
    
    Arguments:
        i {integer} -- Index for printing information
        br {dictionary} -- Given bug report 
        bug_reports {list of dictionaries} -- All bug reports
        java_src_dict {dictionary} -- A dictionary of java source codes
    """
    print("Bug report :", i + 1, len(bug_reports))
    br_id = br["id"]
    br_date = br["report_time"]
    br_files = br["files"]
    br_raw_text = br["raw_text"]
    features = []
    for java_file in br_files:
        java_file = os.path.normpath(java_file)
        print(java_file)
        try:
            # Source code of the java file
            src = java_src_dict[java_file]

            # rVSM Text Similarity
            rvsm = cosine_sim(br_raw_text, src)

            # Class Name Similarity
            cns = class_name_similarity(br_raw_text, src)

            # Previous Reports
            prev_reports = previous_reports(java_file, br_date, bug_reports)

            # Collaborative Filter Score
            cfs = collaborative_filtering_score(br_raw_text, prev_reports)

            # Bug Fixing Recency
            bfr = bug_fixing_recency(br, prev_reports)

            # Bug Fixing Frequency
            bff = len(prev_reports)

            features.append([br_id, java_file, rvsm, cfs, cns, bfr, bff, 1])

            for java_file, rvsm, cns in top_k_wrong_files(
                br_files, br_raw_text, java_src_dict
            ):
                features.append([br_id, java_file, rvsm, cfs, cns, bfr, bff, 0])

        except:
            print("Ex")
            pass

    return features


def extract_features():
    """Clones the git repository and parallelizes the feature extraction process
    """
    time = datetime.now()
    print(time)
    # Clone git repo to a local folder
    git_clone(
        # repo_url="https://github.com/eclipse/eclipse.platform.ui.git",
        repo_url=DATASET.repo_url,
        clone_folder="../data/",
    )

    # Read bug reports from tab separated file
    # bug_reports = tsv2dict("../data/Eclipse_Platform_UI.txt")
    bug_reports = tsv2dict(DATASET.bug_repo)
    print("bug_reports", len(bug_reports))

    # Read all java source files
    # java_src_dict = get_all_source_code("../data/eclipse.platform.ui/bundles/")
    java_src_dict = get_all_source_code(DATASET.src)
    print("java_src_dict", len(java_src_dict))
    # Use all CPUs except one to speed up extraction and avoid computer lagging
    batches = Parallel(n_jobs=cpu_count() - 1)(
        delayed(extract)(i, br, bug_reports, java_src_dict)
        for i, br in enumerate(bug_reports)
    )

    print("batches", (batches))

    # Flatten features
    features = [row for batch in batches for row in batch]
    print(len(features))

    # Save features to a csv file
    features_path = os.path.normpath(DATASET.features)
    with open(features_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "report_id",
                "file",
                "rVSM_similarity",
                "collab_filter",
                "classname_similarity",
                "bug_recency",
                "bug_frequency",
                "match",
            ]
        )
        for row in features:
            writer.writerow(row)
    print(datetime.now() - time, DATASET.name) # dependency speed network, configuration computer
    # slowly processing speed, partly due to extract features for source in for bug ( m * n )

# Keep time while extracting features
with CodeTimer("Feature extraction"):
    extract_features()
