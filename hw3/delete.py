from flask import redirect, request, url_for, render_template
from flask.views import MethodView
import gbmodel

class Delete(MethodView):
    def get(self,ID):
        model=gbmodel.get_model()
        model.delete(ID)
        return redirect(url_for('entries'))

        
