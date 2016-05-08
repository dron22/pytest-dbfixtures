
import re
import elasticsearch as es_module
from pytest_dbfixtures import factories


def test_elastic_process(elasticsearch_proc):
    """Simple test for starting elasticsearch_proc."""
    assert elasticsearch_proc.running() is True


def test_elasticsarch(elasticsearch):
    """Tests if elasticsearch fixtures connects to process."""
    assert elasticsearch.cluster.health()['status'] == 'green'


elasticsearch_proc_random = factories.elasticsearch_proc(port='?')
elasticsearch_random = factories.elasticsearch('elasticsearch_proc_random')


def test_random_port(elasticsearch_random):
    """Tests if elasticsearch fixture can be started on random port"""
    assert elasticsearch_random.cluster.health()['status'] == 'green'


def test_index_creation(elasticsearch):
    """Tests if index creation via elasticsearch fixture succeeds"""
    name = 'mytestindex'
    elasticsearch.indices.create(index=name)
    assert name in elasticsearch.indices.get_settings().keys()


def test_index_type(elasticsearch_proc):
    """Tests if index creation via elasticsearch fixture succeeds"""
    cmd = elasticsearch_proc.command
    index_store_type = re.findall(r'--index\.store\.type=(.*?)(?:--|\n)', cmd)
    hosts = '%s:%s' % (elasticsearch_proc.host, elasticsearch_proc.port)
    client = es_module.Elasticsearch(hosts=hosts)
    es_version = client.info()['version']['number']

    if int(es_version[0]) < 2:
        assert index_store_type[0].strip() == 'memory'
