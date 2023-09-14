
from flask import render_template
from flask.views import MethodView
import gbmodel

class Entries(MethodView):
    def get(self):
        model = gbmodel.get_model()
        entries = [dict(ID=row[0],name=row[1], service=row[2], location=row[3], operating_hours=row[4], phone_number=row[5], review=row[6] ) for row in model.select()]
        
        return render_template('entries.html',entries=entries)