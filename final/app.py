from google.cloud import translate_v2 as translate
from flask import Flask, redirect, render_template, request
from datetime import datetime
from flask import jsonify
import six
import json
from google.cloud import translate_v2 as translate
from googleapiclient.discovery import build


import logging
import os
import json

from google.cloud import vision
from google.cloud import datastore
from google.cloud import storage

CLOUD_STORAGE_BUCKET = ("vkarinje")

app = Flask(__name__)
#https://cloud.google.com/translate/docs/basic/translating-text#translate_translate_text-python
#https://cloud.google.com/translate/docs/languages -The list of standard languages is dispalyed here.I am choosing Hindi(hi) as my target language

def translateFunction(text):
      translate_client = translate.Client()     
      response = translate_client.translate(text, target_language= 'hi')
      return response["translatedText"]

@app.route("/")
def uploadpage():
    #creating a cloud datastore client
    datastore_client = datastore.Client()
    
    #fetch information from Datastore about every object uploaded
    query = datastore_client.query(kind="Picture")
    image_entities = list(return_times(1))

    #Passing the object_entities as a parameter to the Jinja2 HTML template that is returned
    return render_template("index.html", image_entities=image_entities)
def return_times(limit):

    datastore_client = datastore.Client()
    query = datastore_client.query(kind='Picture')
    query.order = ['-timestamp']

    times = query.fetch(limit=limit)

    return times


@app.route("/success", methods=["GET", "POST"])
def result_page():
    image = request.files["file"]

    #Cloud Storage client creation
    storage_client = storage.Client()

    # Accessing the bucket the files will be uploaded into
    bucket = storage_client.get_bucket("vkarinje")

    # Create a new blob and upload the file's content.
    blob = bucket.blob(image.filename)
    blob.upload_from_string(image.read(), content_type=image.content_type)

    # Making the blob publicly visible
    blob.make_public()

    # Creation of a Cloud Vision client.
    vision_client = vision.ImageAnnotatorClient()

    # Detection of faces if any faces found in uploaded files
    source_uri = "gs://{}/{}".format(CLOUD_STORAGE_BUCKET, blob.name)
    loadedimage = vision.Image(source=vision.ImageSource(gcs_image_uri=source_uri))
    faces = vision_client.face_detection(image=loadedimage).face_annotations

    # Finding out what the object is about
    response = vision_client.web_detection(image=loadedimage)
    annotations = response.web_detection
    object_detection = annotations.web_entities
    object_detected = ""


    if len(object_detection) > 0:
        object_detected = object_detection[0].description
    else:
        object_detected = "The object uploaded has not been detected"

   #translating the text detected into target langugae
    translation_of_text_detected = translateFunction(object_detected)

    #detection of logos in the object uploaded
    response = vision_client.logo_detection(image=loadedimage)
    logos = response.logo_annotations
    logo = ""
    if len(logos) > 0:
        logo = logos[0].description
    else:
        logo = "No Logos Present in the object uploaded"

   
    # If the object uploaded has any face detected in it find the likelihood of being surprised as determined by Google's Machine Learning algorithm.
    if len(faces) > 0:
        face = faces[0]

        # detect the possibility of surprised face
        likelihoods = [
            "Unknown",
            "Very Unlikely",
            "Unlikely",
            "Possible",
            "Likely",
            "Very Likely",
        ]
        surprised_face = likelihoods[face.surprise_likelihood]
    else:
        surprised_face = "Could not detect expression"
    
    #detection of all other labels in the object uploaded"

    response = vision_client.label_detection(image=loadedimage)
    labels = response.label_annotations
    label = ""
    if labels:
        if len(labels) < 5:
            for j in labels:
                label = label + ", " + j.description
        else:
            for i in range(5):
                label = label + ", " + labels[i].description
        label = label[1:]
    else:
        label = "There are no labels found in the object uploaded"

    #If the Object uploaded represents a famous place detect the place   
    response = vision_client.landmark_detection(image=loadedimage)
    landmarks = response.landmark_annotations
    landmark = ""
    if len(landmarks) > 0:
        for i in landmarks:
            landmark = landmark + ", " + i.description
        landmark = landmark[1:]
    else:
        landmark = "No place found for this object uploaded"

    # convert the text if any found in the object that is uploaded
    response = vision_client.text_detection(image=loadedimage)
    texts = response.text_annotations[:10]
    text_found = ""
    if texts:
        for text in texts:
            entity_annotation = text 
            description_string = str(entity_annotation.description)
            text_found = text_found + " " + text.description
    else:
        text_found = "There is no text found in the object that you uploaded"
    #if text found translate the text into my target language    
    translation_of_text = translateFunction(text_found)
      
    # Creation of  a Cloud Datastore client.
    datastore_client = datastore.Client()

    # current date / time.
    current_datetime = datetime.now()

    
    kind = "Picture"

    
    name = blob.name

    # Creation of  the Cloud Datastore key for the new entity.
    key = datastore_client.key(kind, name)
    entity = datastore.Entity(key)
    entity["blob_name"] = blob.name
    entity["image_public_url"] = blob.public_url
    entity["timestamp"] = current_datetime
    entity['object_detected'] = object_detected
    entity['translated_label_detected'] = translation_of_text_detected
    entity["expression"] = surprised_face
    entity['logo'] = logo 
    entity['label'] = label
    entity['text'] = text_found
    entity['translated_text'] = translation_of_text
    entity['place_detected'] = landmark



    
    datastore_client.put(entity)

    
    return redirect("/")

@app.errorhandler(500)
def server_error(e):
    logging.exception("There was an error for the request made.")
    return (
        """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(
            e
        ),
        500,
    )


if __name__ == "__main__":
     app.run(host="127.0.0.1", port=5000, debug=True)














  
 












