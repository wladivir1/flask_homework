import flask
from flask import request

from app import get_app
from views import AdsView
from config_db import SessionLocal


app = get_app()

@app.before_request
def before_request():
    session = SessionLocal()
    request.session = session
 
@app.after_request   
def after_request(response: flask.Response):
    request.session.close()
    return response


ads_view = AdsView.as_view('ads_view')

app.add_url_rule('/ads/', view_func=ads_view, methods=['GET', 'POST'])
app.add_url_rule('/ads/<int:ad_id>', view_func=ads_view, methods=['GET', 'PATCH', 'DELETE'])


if __name__ == '__main__':
    app.run(debug=True)
