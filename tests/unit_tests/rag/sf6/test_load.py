from rag.sf6.load import Load

def test_execute():
    content = Load().execute()
    assert 'Luke' in content.decode()
