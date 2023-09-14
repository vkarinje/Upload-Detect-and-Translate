from flask import redirect, request, url_for, render_template
from flask.views import MethodView
import gbmodel

class Sign(MethodView):
    def get(self):
        return render_template('sign.html')

    def post(self):
        """
        Accepts POST requests, and processes the form;
        Redirect to index when completed.
        """
        model = gbmodel.get_model()
        model.insert(request.form['name'], request.form['service'], request.form['location'], request.form['operating_hours'], request.form['phone_number'], request.form['review'])
        return redirect(url_for('index'))