from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from flask import Flask, request, jsonify, redirect, Response
import json
import uuid
import time

# Connect to our local MongoDB
client = MongoClient('mongodb://localhost:27017/')

# Choose database
db = client['InfoSys']

# Choose collections
students = db['Students']
users = db['Users']

# Initiate Flask App
app = Flask(__name__)

users_sessions = {}

def create_session(username):
    user_uuid = str(uuid.uuid1())
    users_sessions[user_uuid] = (username, time.time())
    return user_uuid  

def is_session_valid(user_uuid):
    return user_uuid in users_sessions

# ΕΡΩΤΗΜΑ 1: Δημιουργία χρήστη
@app.route('/createUser', methods=['POST'])
def create_user():
    # Request JSON data
    data = None 
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("bad json content",status=500,mimetype='application/json')
    if data == None:
        return Response("bad request",status=500,mimetype='application/json')
    if not "username" in data or not "password" in data:
        return Response("Information incomplete",status=500,mimetype="application/json")

    """
    Το συγκεκριμένο endpoint θα δέχεται στο body του request του χρήστη ένα json της μορφής: 

    {
        "usename": "some username", 
        "password": "a very secure password"
    }

    * Θα πρέπει να εισαχθεί ένας νέος χρήστης στο σύστημα, ο οποίος θα εισάγεται στο collection Users (μέσω της μεταβλητής users). 
    * Η εισαγωγή του νέου χρήστη, θα γίνεται μόνο στη περίπτωση που δεν υπάρχει ήδη κάποιος χρήστης με το ίδιο username. 
    * Αν γίνει εισαγωγή του χρήστη στη ΒΔ, να επιστρέφεται μήνυμα με status code 200. 
    * Διαφορετικά, να επιστρέφεται μήνυμα λάθους, με status code 400.
    """

    if users.find({"username":data["username"]}).count() == 0 :
        user = {"username": data['username'], "password": data['password']}
        users.insert_one(user)
        return Response(data['username']+" was added to the MongoDB",status=200,mimetype='application/json') 
    else:
        return Response("A user with the given username already exists",status=400,mimetype='application/json')
    

# ΕΡΩΤΗΜΑ 2: Login στο σύστημα
@app.route('/login', methods=['POST'])
def login():
    # Request JSON data
    data = None 
    try:
        data = json.loads(request.data)
    except Exception as e:
        return Response("bad json content",status=500,mimetype='application/json')
    if data == None:
        return Response("bad request",status=500,mimetype='application/json')
    if not "username" in data or not "password" in data:
        return Response("Information incomplete",status=500,mimetype="application/json")

    """
        Να καλεστεί η συνάρτηση create_session() (!!! Η ΣΥΝΑΡΤΗΣΗ create_session() ΕΙΝΑΙ ΗΔΗ ΥΛΟΠΟΙΗΜΕΝΗ) 
        με παράμετρο το username μόνο στη περίπτωση που τα στοιχεία που έχουν δοθεί είναι σωστά, δηλαδή:
        * το data['username] είναι ίσο με το username που είναι στη ΒΔ (να γίνει αναζήτηση στο collection Users) ΚΑΙ
        * το data['password'] είναι ίσο με το password του συγκεκριμένου χρήστη.
        * Η συνάρτηση create_session() θα επιστρέφει ένα string το οποίο θα πρέπει να αναθέσετε σε μία μεταβλητή που θα ονομάζεται user_uuid.
        
        * Αν γίνει αυθεντικοποίηση του χρήστη, να επιστρέφεται μήνυμα με status code 200. 
        * Διαφορετικά, να επιστρέφεται μήνυμα λάθους με status code 400.
    """

    if users.count_documents({"$and": [{"username":data["username"]}, {"password":data["password"]}]}) == 1 :
        user_uuid = create_session(data['username'])
        res = {"uuid": user_uuid, "username": data['username']}
        return Response(json.dumps(res),status=200, mimetype='application/json')
    else:
        return Response("Wrong username or password.",status=400,mimetype='application/json') 


# ΕΡΩΤΗΜΑ 3: Επιστροφή φοιτητή βάσει email 
@app.route('/getStudent', methods=['GET'])
def get_student():

    """
        Στα headers του request ο χρήστης θα πρέπει να περνάει το uuid το οποίο έχει λάβει κατά την είσοδό του στο σύστημα. 
            Π.Χ: uuid = request.headers.get['authorization']
        Για τον έλεγχο του uuid να καλεστεί η συνάρτηση is_session_valid() (!!! Η ΣΥΝΑΡΤΗΣΗ is_session_valid() ΕΙΝΑΙ ΗΔΗ ΥΛΟΠΟΙΗΜΕΝΗ) με παράμετρο το uuid. 
            * Αν η συνάρτηση επιστρέψει False ο χρήστης δεν έχει αυθεντικοποιηθεί. Σε αυτή τη περίπτωση να επιστρέφεται ανάλογο μήνυμα με response code 401. 
            * Αν η συνάρτηση επιστρέψει True, ο χρήστης έχει αυθεντικοποιηθεί. 

        Το συγκεκριμένο endpoint θα δέχεται σαν argument το email του φοιτητή και θα επιστρέφει τα δεδομένα του. 
        Να περάσετε τα δεδομένα του φοιτητή σε ένα dictionary που θα ονομάζεται student.
        
        Σε περίπτωση που δε βρεθεί κάποιος φοιτητής, να επιστρέφεται ανάλογο μήνυμα.
    """

    uuid = request.headers.get('authorization')

    if is_session_valid(uuid) :

        email = request.args.get('email')

        if email == None:
            return Response("Bad request", status=500, mimetype='application/json')
        student = students.find_one({"email":email})
        if student !=None:

            if students.count_documents({"$and": [{"email":email}, {"address": {'$exists': False}}, {"gender": {'$exists': False}}]}) == 1 :
                student = {'name':student["name"],'email':student["email"], 'yearOfBirth':student["yearOfBirth"]}
                return Response(json.dumps(student), status=200, mimetype='application/json')
            if students.count_documents({"$and": [{"email":email}, {"address": {'$exists': True}}, {"gender": {'$exists': False}}]}) == 1 :
                student = {'name':student["name"],'email':student["email"], 'yearOfBirth':student["yearOfBirth"],'address':student["address"]}
                return Response(json.dumps(student), status=200, mimetype='application/json')
            if students.count_documents({"$and": [{"email":email}, {"address": {'$exists': False}}, {"gender": {'$exists': True}}]}) == 1 :
                student = {'name':student["name"],'email':student["email"], 'yearOfBirth':student["yearOfBirth"],'gender':student["gender"]}
                return Response(json.dumps(student), status=200, mimetype='application/json')
            if students.count_documents({"$and": [{"email":email}, {"address": {'$exists': True}}, {"gender": {'$exists': True}}]}) == 1 :
                student = {'name':student["name"],'email':student["email"], 'yearOfBirth':student["yearOfBirth"],'address':student["address"],'gender':student["gender"]}
                return Response(json.dumps(student), status=200, mimetype='application/json')

        return Response('No student found with that email',status=500,mimetype='application/json')
    else:
        return Response("Wrong uuid.",status=401,mimetype='application/json')


# ΕΡΩΤΗΜΑ 4: Επιστροφή όλων των φοιτητών που είναι 30 ετών
@app.route('/getStudents/thirties', methods=['GET'])
def get_students_thirty():
    """
        Στα headers του request ο χρήστης θα πρέπει να περνάει το uuid το οποίο έχει λάβει κατά την είσοδό του στο σύστημα. 
            Π.Χ: uuid = request.headers.get['authorization']
        Για τον έλεγχο του uuid να καλεστεί η συνάρτηση is_session_valid() (!!! Η ΣΥΝΑΡΤΗΣΗ is_session_valid() ΕΙΝΑΙ ΗΔΗ ΥΛΟΠΟΙΗΜΕΝΗ) με παράμετρο το uuid. 
            * Αν η συνάρτηση επιστρέψει False ο χρήστης δεν έχει αυθεντικοποιηθεί. Σε αυτή τη περίπτωση να επιστρέφεται ανάλογο μήνυμα με response code 401. 
            * Αν η συνάρτηση επιστρέψει True, ο χρήστης έχει αυθεντικοποιηθεί. 
        
        Το συγκεκριμένο endpoint θα πρέπει να επιστρέφει τη λίστα των φοιτητών οι οποίοι είναι 30 ετών.
        Να περάσετε τα δεδομένα των φοιτητών σε μία λίστα που θα ονομάζεται students.
        
        Σε περίπτωση που δε βρεθεί κάποιος φοιτητής, να επιστρέφεται ανάλογο μήνυμα και όχι κενή λίστα.
    """

    uuid = request.headers.get('authorization')

    if is_session_valid(uuid) :
        
        query = {"yearOfBirth": 1991}
        iterable = students.find(query)

        output = []
        """
        Δεν ονόμασα την λίστα students γιατί μου βγάζει αυτό το error :
        UnboundLocalError: local variable 'students' referenced before assignment
        """

        for student in iterable:
            student['_id'] = None 
            output.append(student)

        if output != []:
            return Response(json.dumps(output), status=200, mimetype='application/json')
        return Response('No student found thas is exactly 30 years old',status=500,mimetype='application/json')
    else:
        return Response("Wrong uuid.",status=401,mimetype='application/json')

# ΕΡΩΤΗΜΑ 5: Επιστροφή όλων των φοιτητών που είναι τουλάχιστον 30 ετών
@app.route('/getStudents/oldies', methods=['GET'])
def get_students_oldy():
    """
        Στα headers του request ο χρήστης θα πρέπει να περνάει και το uuid το οποίο έχει λάβει κατά την είσοδό του στο σύστημα. 
            Π.Χ: uuid = request.headers.get['authorization']
        Για τον έλεγχο του uuid να καλεστεί η συνάρτηση is_session_valid() (!!! Η ΣΥΝΑΡΤΗΣΗ is_session_valid() ΕΙΝΑΙ ΗΔΗ ΥΛΟΠΟΙΗΜΕΝΗ) με παράμετρο το uuid. 
            * Αν η συνάρτηση επιστρέψει False ο χρήστης δεν έχει αυθεντικοποιηθεί. Σε αυτή τη περίπτωση να επιστρέφεται ανάλογο μήνυμα με response code 401. 
            * Αν η συνάρτηση επιστρέψει True, ο χρήστης έχει αυθεντικοποιηθεί. 
        
        Το συγκεκριμένο endpoint θα πρέπει να επιστρέφει τη λίστα των φοιτητών οι οποίοι είναι 30 ετών και άνω.
        Να περάσετε τα δεδομένα των φοιτητών σε μία λίστα που θα ονομάζεται students.
        
        Σε περίπτωση που δε βρεθεί κάποιος φοιτητής, να επιστρέφεται ανάλογο μήνυμα και όχι κενή λίστα.
    """

    uuid = request.headers.get('authorization')

    if is_session_valid(uuid) :
        
        query = {"yearOfBirth": {'$lt': 1991}}
        iterable = students.find(query)

        output = []
        """
        Δεν ονόμασα την λίστα students γιατί μου βγάζει αυτό το error :
        UnboundLocalError: local variable 'students' referenced before assignment
        """

        for student in iterable:
            student['_id'] = None 
            output.append(student)

        if output != []:
            return Response(json.dumps(output), status=200, mimetype='application/json')
        return Response('No student found thas is at least 30 years old',status=500,mimetype='application/json')
    else:
        return Response("Wrong uuid.",status=401,mimetype='application/json')


# Εκτέλεση flask service σε debug mode, στην port 5000. 
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)