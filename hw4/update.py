from flask import redirect, request, url_for, render_template
from flask.views import MethodView
import gbmodel


class Update(MethodView):
    def get(self,ID):
        model=gbmodel.get_model()
        print("cheching",ID)
        entries= [dict(ID=row[0],name=row[1], service=row[2], location=row[3], operating_hours=row[4], phone_number=row[5], review=row[6] ) for row in model.fetch(ID)]
        
        print("etryyy:",entries)
        print("entry id",entries.ID)
        return render_template('update.html',entries=entries)
    def post(self,ID):
        
        model = gbmodel.get_model()
        model.update(ID,request.form['name'], request.form['service'], request.form['location'], request.form['operating_hours'], request.form['phone_number'], request.form['review'])
        return redirect(url_for('entries'))

   
        
    