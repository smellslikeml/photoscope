from utils import *
import config as cfg
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

client = Elasticsearch()
index_name = 'testing'
data_dir = '/path/to/images'

# Initialize elasticsearch classes
idx = Index(index_name, cfg.index_file, cfg.data, client)
doc = Document(data_dir, cfg.data, index_name)

# Create an index
print('Creating index ', index_name)
idx.createIndex()

print('Creating documents..')
doc.run()

print('Bulk indexing..')
idx.bulkIndex()

print('Done!')
