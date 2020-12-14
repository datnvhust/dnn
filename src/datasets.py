from collections import namedtuple
from pathlib import Path

# Dataset root directory
_DATASET_ROOT = Path('../data')

Dataset = namedtuple('Dataset', ['name', 'src', 'bug_repo', 'repo_url', 'features'])

# Source codes and bug repositories
aspectj = Dataset(
    'aspectj',
    _DATASET_ROOT / 'org.aspectj/',
    _DATASET_ROOT / 'AspectJ.txt',
    "https://github.com/eclipse/org.aspectj.git",
    _DATASET_ROOT / 'features2.csv'
)

eclipse = Dataset(
    'eclipse',
    _DATASET_ROOT / 'eclipse.platform.ui/bundles/',
    _DATASET_ROOT / 'Eclipse_Platform_UI.txt',
    "https://github.com/eclipse/eclipse.platform.ui.git",
    _DATASET_ROOT / 'features.csv'
)

swt = Dataset(
    'swt',
    _DATASET_ROOT / 'eclipse.platform.swt/',
    _DATASET_ROOT / 'SWT.txt',
    "https://github.com/eclipse/eclipse.platform.swt.git",
    _DATASET_ROOT / 'features_swt.csv'
)

tomcat = Dataset(
    'tomcat',
    _DATASET_ROOT / 'tomcat/',
    _DATASET_ROOT / 'Tomcat.txt',
    "https://github.com/apache/tomcat.git",
    _DATASET_ROOT / 'features_tomcat.csv'
)

### Current dataset in use. (change this name to change the dataset)
DATASET = tomcat

if __name__ == '__main__':
    print(DATASET.name, DATASET.src, DATASET.bug_repo)
