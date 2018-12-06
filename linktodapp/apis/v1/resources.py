from flask import jsonify,request,current_app,url_for
from flask.views import MethodView

from linktodapp.apis.v1 import api_v1

class IndexAPI(MethodView):
    def get(self):
        return jsonify({
            "api_version":"1.0",
            "api_base_url":"api.linktodapp.com/v1"
        })

api_v1.add_url_rule('/', view_func=IndexAPI.as_view('index'), methods=['GET'])