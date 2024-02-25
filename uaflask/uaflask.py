from app import create_app, db
from config import env
import sqlalchemy as sa
import sqlalchemy.orm as sao
import ssl
# from app.models import Users

app = create_app()

@app.shell_context_processor #flask shell에 미리 등록
def make_shell_context():
    return {'db': db, 'sa': sa, 'sao': sao}

if __name__ == "__main__":
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ssl_context.load_cert_chain(certfile=env('CERTFILE'), keyfile=env('KEYFILE'))
    app.run(host=env('HOST'), port=env('PORT'), ssl_context=ssl_context)
