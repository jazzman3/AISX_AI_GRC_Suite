import importlib.util,os,tempfile,pytest
from fastapi.testclient import TestClient
spec=importlib.util.spec_from_file_location('grc','shared/app.py');mod=importlib.util.module_from_spec(spec);os.environ['DB_PATH']='/tmp/aisx_default_test.db';spec.loader.exec_module(mod)
@pytest.fixture(params=list(mod.MODULES))
def client(request,monkeypatch,tmp_path):
    monkeypatch.setenv('ADMIN_PASSWORD','test-password-with-very-long-length')
    monkeypatch.setenv('SEED_DEMO','0')
    app=mod.build_app(request.param,str(tmp_path / f'{request.param}.db'))
    return request.param,TestClient(app),('aisx-admin','test-password-with-very-long-length')
def test_health(client):
    key,c,auth=client; assert c.get('/health').json()['module']==key
def test_authenticated(client):
    _,c,auth=client; assert c.get('/api/records').status_code==401;assert c.get('/api/records',auth=auth).status_code==200
    assert c.get('/',auth=auth).status_code==200
def test_create_and_audit(client):
    key,c,auth=client;cfg=mod.MODULES[key];vals=dict(zip(cfg['fields'],cfg['sample'][0]));r=c.post('/api/records',json={'values':vals},auth=auth)
    assert r.status_code==201,r.text;rid=r.json()['id'];assert len(c.get('/api/records',auth=auth).json())==1
    assert c.get('/api/audit',auth=auth).json()[0]['record_id']==rid
    assert c.get('/api/summary',auth=auth).json()['values'][0]==1
    assert c.get('/api/export.csv',auth=auth).status_code==200
def test_validation_and_update(client):
    key,c,auth=client;cfg=mod.MODULES[key];vals=dict(zip(cfg['fields'],cfg['sample'][0]));assert c.post('/api/records',json={'values':{}},auth=auth).status_code==422
    created=c.post('/api/records',json={'values':vals},auth=auth).json();field=cfg['fields'][1];assert c.patch('/api/records/'+str(created['id']),json={'values':{field:'Updated Owner'}},auth=auth).status_code==200
    assert c.patch('/api/records/999',json={'values':{}},auth=auth).status_code==404
