import io
import app as module

def test_home():
    client=module.app.test_client()
    assert client.get('/').status_code == 200

def test_pin_required():
    client=module.app.test_client()
    r=client.post('/api/upload', data={'pin':'wrong','files':(io.BytesIO(b'x'),'a.jpg')}, content_type='multipart/form-data')
    assert r.status_code == 401
