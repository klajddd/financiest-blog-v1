import os
import random
import operator

from flask import Flask, render_template, request
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from models import *

app = Flask(__name__)

# pulling the DB from an environment variable called DATABASE_URL
engine = create_engine(os.getenv("DATABASE_URL"))

db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    total_concepts = db.execute(
        "select count(concept) from concepts").fetchall()
    return render_template("index.html", total_concepts=total_concepts[0][0])


@app.route("/references")
def references():
    return render_template("references.html")


@app.route("/hiddenallconcepts")
def all_concepts():
    concepts = Concepts.query.all()
    # concepts = db.execute("select * from concepts")
    return render_template("allconceptshidden.html", concepts=concepts)


@app.route("/mission")
def mission():
    return render_template("mission.html")


@app.route("/concept/<int:concept_id>")
def concept(concept_id):
    """List details about a single concept."""
    all_ids = db.execute("select id from concepts").fetchall()
    current_concept = db.execute(
        "select * from concepts WHERE id = :id", {"id": concept_id}).fetchone()
    next_concept = db.execute(
        "select * from concepts WHERE id = :id", {"id": random.choice(all_ids)[0]}).fetchone()
    return render_template("concept.html", current_concept=current_concept, next_concept=next_concept)


@app.route("/searchresult", methods=["GET"])
def searchresult():
    """Book a flight."""
    # Get form information.
    input_concept = request.args.get("name")
    concepts = db.execute("select * from concepts where lower(concept) like :input_concept",
                          {"input_concept": input_concept_type(input_concept.lower())})
    explanations = db.execute("select explanation from concepts where lower(explanation) like :input_concept", {
                              "input_concept": input_concept_type(input_concept.lower())})
    sorted_concepts = []
    for c in concepts:
        sorted_concepts.append(c)
    sorted_concepts.sort(key=operator.itemgetter(1))

    # if concept is not in the library; so if no results are found
    if concepts.rowcount < 1:
        # concepts = db.execute("select * from concepts")
        concepts = Concepts.query.all()
        explanations = db.execute("select explanation from concepts")
        sorted_concepts = []
        for c in concepts:
            sorted_concepts.append(c)
        sorted_concepts.sort(key=operator.itemgetter(1))

        return render_template("searchresultnoresult.html", input_concept=input_concept, concepts=sorted_concepts, explanations=explanations)
    else:
        return render_template("searchresult.html", input_concept=input_concept, concepts=sorted_concepts, explanations=explanations)


@app.route("/updateconcept")
def updateconcept():
    concepts = Concepts.query.all()
    # concepts = db.execute("select * from concepts")
    explanations = db.execute("select explanation from concepts")
    sorted_concepts = []
    for c in concepts:
        sorted_concepts.append(c)
    sorted_concepts.sort(key=operator.itemgetter(1))
    return render_template("updateconcept.html", concepts=sorted_concepts, explanations=explanations, selected_concept=None)


@app.route("/getData/<int:concept_id>")
def getData(concept_id):
    concepts = Concepts.query.all()
    # concepts = db.execute("select * from concepts")
    explanations = db.execute("select explanation from concepts")
    sorted_concepts = []
    for c in concepts:
        sorted_concepts.append(c)
    sorted_concepts.sort(key=operator.itemgetter(1))

    selected_concept = db.execute(
        "select * from concepts WHERE id = :id", {"id": concept_id}).fetchone()

    return render_template("updatetheconcept.html", concepts=sorted_concepts, explanations=explanations, selected_concept=selected_concept)


@app.route("/updatedone/<int:id>")
def updatedone(id):
    # Get form information.
    input_definition = request.args.get("conceptdefinition")

    db.execute("UPDATE concepts SET explanation = :input_explanation WHERE id = :input_id", {
               "input_explanation": input_definition, "input_id": id})
    db.commit()
    return render_template("updatedone.html")


@app.route("/uploadconcept")
def uploadconcept():
    return render_template("uploadconcept.html")


@app.route("/uploaddone")
def uploaddone():
    input_concept = request.args.get("name")  # Get form information.
    input_definition = request.args.get("conceptdefinition")

    concept = Concepts(concept=input_concept, explanation=input_definition)

    print('crated concept with title {} and explanation {}'.format(
        input_concept, input_definition))
    db.add(concept)

    # db.execute(
    #     "INSERT INTO concepts(concept, explanation) VALUES(:input_concept, :input_definition)",
    #     {"input_concept": input_concept, "input_definition": input_definition})

    db.commit()
    return render_template("uploaddone.html")


def input_concept_type(i):  # If user input concept is a str, add % around it
    if isinstance(i, str):
        return "%"+i+"%"
    else:
        return i
