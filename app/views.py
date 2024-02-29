import os
from typing import Type

from flask import request, jsonify
from flask.views import MethodView
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError

from model import Ads
from app import get_app
from schema import CreateAds, UpdateAds
 
  
app = get_app()

class HttpError(Exception):
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.massage = message

@app.errorhandler(HttpError)        
def error_handler(error: HttpError):
    response = jsonify({"error": error.massage}) 
    response.status_code = error.status_code
    
    return response

def getAds(ad_id: int):
    ad = request.session.query(Ads).filter(Ads.id == ad_id).first()
    if ad is None:
        raise HttpError(404, 'Ad not found')
    
    return ad

def validate_json(json_data: dict,
                  schema_class: Type[CreateAds]|Type[UpdateAds]):
    try:
        return schema_class(**json_data).dict(exclude_unset=True)
    except ValidationError as e:
        error = e.errors()[0]
        error.pop('ctx', None)
        
        raise HttpError(400, error)


class AdsView(MethodView):
    def get(self, ad_id: int):
        
        return jsonify(getAds(ad_id).dict)
 
    def patch(self, ad_id: int):
        data = validate_json(request.json, UpdateAds)
        getAds(ad_id).title = data['title']
        getAds(ad_id).description = data['description']
        request.session.commit()
        
        return jsonify({'message': 'Ad updated successfully'})
    
    def delete(self, ad_id: int):
        request.session.delete(getAds(ad_id))
        request.session.commit()
        
        return jsonify({'message': 'Ad deleted successfully'})
    
    def post(self):
        data = validate_json(request.json, CreateAds)
        ad = Ads(title=data['title'],
                 description=data['description'], 
                 owner_id=data['owner_id'])
        request.session.add(ad)
        request.session.commit()
        
        return jsonify(ad.dict) 
        

