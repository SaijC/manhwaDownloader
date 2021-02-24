import os
from pathlib import Path

# Paths
CONSTPATH = CONSTANTSPATH = os.path.dirname(__file__)
ROOTPATH = Path(CONSTANTSPATH).parent
OUTPUTPATH = os.path.join(ROOTPATH, 'outputs')


GREENLIST = ['jpg', 'gif']

REMOVEILLEGALCHARS = '[^\w\-_\. ]'

SITETEMPLATEDICT = {
    'manytoon': {
        'gatherImgTags': ('img', {'class': 'wp-manga-chapter-img'}),
        'gatherRawLink': 'src',
        'nextImgTags': ('a', {'class': 'btn next_page'}),
        'nextRawLink': 'href'

    },
    'webtoonXYZ': {
        'gatherImgTags': ('img', {'class': 'wp-manga-chapter-img'}),
        'gatherRawLink': 'data-src',
        'nextImgTags': ('a', {'class': 'btn next_page'}),
        'nextRawLink': 'href'
    }
}