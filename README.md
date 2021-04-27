# Ergasia_1_E17129_Sakellariou_Nikolaos

Το συγκεκριμένο project αφορά την πρώτη υποχρεωτική εργασία του μαθήματος «Πληροφοριακά Συστήματα» του τμήματος Ψηφιακών Συστημάτων του Πανεπιστημίου Πειραιώς.

Έχουν υλοποιηθεί συνολικά 9 endpoints, όπου για να ελεγχθεί η σωστή λειτουργία τους έχει δημιουργηθεί ένα container MongoDB το οποίο ονομάζεται mongodb και ακούει στη port 27017 του host και έχουν περαστεί τα δεδομένα που υπάρχουν στο αρχείο students.json σε ένα collection με όνομα Students στην βάση δεδομένων InfoSys. Και για την κλήση των endpoints χρησιμοποιήθηκε το Postman.

<h2>Πρώτο endpoint :</h2>

Το συγκεκριμένο endpoint δέχεται στο body του request του χρήστη ένα json της μορφής :

{
    "username": "some username", 
    "password": "a very secure password"
}

Γίνεται ένας έλεγχος αν υπάρχει ήδη κάποιος χρήστης με το ίδιο username στο collection Users, αν υπάρχει ήδη επιστρέφεται μήνυμα λάθους με status code 400, ενώ αν δεν υπάρχει κάποιος εγγεγραμμένος χρήστης με το ίδιο username, ο χρήστης προστίθεται στο collection και επιστρέφεται μήνυμα με status code 200.
Για τον έλεγχο της σωστής λειτουργίας του endpoint δημιουργήθηκε ένας χρήστης με username NickSak και password 20202021
Οπότε στο Postman στη θέση του url μπήκε : http://127.0.0.1:5000/createUser με method POST και στο body του request : 

{
    "username": "NickSak", 
    "password": "20202021"
}
Και επιστρέφεται μήνυμα : NickSak was added to the MongoDB
Αν προσπαθήσω πάλι να ξαναεισάγω χρήστη με το ίδιο username θα επιστραφεί μήνυμα : A user with the given username already exists

<h2>Δεύτερο endpoint :</h2>

Το συγκεκριμένο endpoint δέχεται στο body του request του χρήστη ένα json της μορφής :

{
    "username": "some username", 
    "password": "a very secure password"
}

Γίνεται ένας έλεγχος αν υπάρχει κάποιος χρήστης με το ίδιο username και password στο collection Users, αν δεν υπάρχει επιστρέφεται μήνυμα λάθους με status code 400, ενώ αν  υπάρχει καλείται η συνάρτηση create_session() με παράμετρο το username το οποίο επιστρέφει ένα String το οποίο είναι το uuid του χρήστη και θα τον βοηθάει να έχει πρόσβαση στα άλλα endpoints.Και τέλος, επιστρέφεται μήνυμα με status code 200.

Οπότε στο Postman στη θέση του url μπήκε : http://127.0.0.1:5000/login με method POST και στο body του request : 

{ "username": "NickSak", "password": "20202021" }

Και επιστρέφεται μήνυμα : 

{
    "uuid": "cd78359c-a76c-11eb-8e49-705a0f871404",
    "username": "NickSak"
}

<h2>Τρίτο endpoint :</h2>

Αφού ο χρήστης έχει κάνει login και έχει λάβει το uuid μπορεί να χρησιμοποιεί και τα άλλα endpoints.

Το συγκεκριμένο endpoint δέχεται στο body του request του χρήστη ένα json της μορφής :

{
    "email": "some email"
}

Και στα headers του request ο χρήστης θα πρέπει να περνάει το uuid σε μια παράμετρο authorization το οποίο έχει λάβει κατά την είσοδό του στο σύστημα.

Καλείται η συνάρτηση is_session_valid() για να γίνει έλεγχος αν το uuid είναι σωστό για να μπορέσει να αυθεντικοποιηθεί ο χρήστης. Αν η συνάρτηση επιστρέψει False ο χρήστης δεν έχει αυθεντικοποιηθεί και επιστρέφεται μήνυμα λάθους με response code 401. Αν η συνάρτηση επιστρέψει True, ο χρήστης έχει αυθεντικοποιηθεί.

Αφού ο χρήστης έχει αυθεντικοποιηθεί, γίνεται ένας έλεγχος αν υπάρχει το email που έδωσε μέσα από το body του request στο collection Students. Αν δεν υπάρχει κάποιος φοιτητής με αυτό το email επιστρέφεται μήνυμα λάθους με response code 500, ενώ αν υπάρχει γίνεται ένας επιπλέον έλεγχος για το αν ο φοιτητής έχει δηλώσει την κατοικία του ή το φύλλο του και επιστρέφεται μήνυμα με τα δεδομένα του φοιτητή.

Οπότε στο Postman στη θέση του url μπήκε : http://127.0.0.1:5000/getStudent με method GET και στα headers του request σε μια παράμετρο authorization έχει μπει ως value το uuid που λάβαμε μετά το login : cd78359c-a76c-11eb-8e49-705a0f871404
Και στο body του request : 

{ "email": "tannerwilson@ontagene.com" }

Και επιστρέφεται μήνυμα : 
{
    "name": "Tanner Wilson",
    "email": "tannerwilson@ontagene.com",
    "yearOfBirth": 1962,
    "address": [
        {
            "street": "Halsey Street",
            "city": "Greenwich",
            "postcode": 13832
        }
    ]
}

<h2>Τέταρτο endpoint :</h2>

Ισχύει ότι αναφέρθηκε και στο προηγούμενο endpoint, δηλαδή στα headers του request ο χρήστης θα πρέπει να περάσει το uuid σε μια παράμετρο authorization το οποίο έχει λάβει κατά την είσοδό του στο σύστημα.

Αφού ο χρήστης έχει αυθεντικοποιηθεί, γίνεται ένας έλεγχος αν υπάρχει κάποιος φοιτητής που έχει γεννηθεί το 1991. Αν δεν υπάρχει, επιστρέφεται αντίστοιχο μήνυμα που ενημερώνει τον χρήστη ότι δεν υπάρχει κανένας φοιτητής που έχει γεννηθεί το 1991, ενώ αν υπάρχει επιστρέφεται η λίστα με τα δεδομένα όλων των φοιτητών που γεννήθηκαν εκείνη την χρονιά.

Οπότε στο Postman στη θέση του url μπήκε : http://127.0.0.1:5000/getStudents/thirties με method GET και στα headers του request σε μια παράμετρο authorization έχει μπει ως value το uuid που λάβαμε μετά το login : cd78359c-a76c-11eb-8e49-705a0f871404
Και στο body του request δεν έχουμε δηλώσει τίποτα

Και επιστρέφεται μήνυμα : 

[
    {
        "_id": null,
        "name": "Browning Rasmussen",
        "email": "browningrasmussen@ontagene.com",
        "yearOfBirth": 1991,
        "address": [
            {
                "street": "Doone Court",
                "city": "Cuylerville",
                "postcode": 17331
            }
        ]
    },
    {
        "_id": null,
        "name": "Bennett Baker",
        "email": "bennettbaker@ontagene.com",
        "yearOfBirth": 1991,
        "gender": "male"
    }
]


<h2>Πέμπτο endpoint :</h2>

Αφού ο χρήστης έχει αυθεντικοποιηθεί, γίνεται ένας έλεγχος αν υπάρχει κάποιος φοιτητής που έχει γεννηθεί πριν το 1991. Αν δεν υπάρχει, επιστρέφεται αντίστοιχο μήνυμα που ενημερώνει τον χρήστη ότι δεν υπάρχει κανένας φοιτητής που έχει γεννηθεί πριν το 1991, ενώ αν υπάρχει επιστρέφεται η λίστα με τα δεδομένα όλων των φοιτητών που γεννήθηκαν πριν εκείνη την χρονιά.

Οπότε στο Postman στη θέση του url μπήκε : http://127.0.0.1:5000/getStudents/oldies με method GET και στα headers του request σε μια παράμετρο authorization έχει μπει ως value το uuid που λάβαμε μετά το login : cd78359c-a76c-11eb-8e49-705a0f871404
Και στο body του request δεν έχουμε δηλώσει τίποτα

Και επιστρέφεται μήνυμα η λίστα με τα δεδομένα όλων των φοιτητών που γεννήθηκαν πριν εκείνη την χρονιά.

<h2>Έκτο endpoint :</h2>

Το συγκεκριμένο endpoint δέχεται στο body του request του χρήστη ένα json της μορφής :

{
    "email": "some email"
}

Αφού ο χρήστης έχει αυθεντικοποιηθεί, γίνεται ένας έλεγχος αν υπάρχει το email που έδωσε μέσα από το body του request στο collection Students. Αν δεν υπάρχει κάποιος φοιτητής με αυτό το email επιστρέφεται μήνυμα λάθους με response code 500, ενώ αν υπάρχει γίνεται ένας επιπλέον έλεγχος για το αν ο φοιτητής έχει δηλώσει την κατοικία του. Αν δεν την έχει δηλώσει επιστρέφεται μήνυμα ότι δεν την έχει δηλώσει με response code 500, ενώ αν την έχει δηλώσει επιστρέφεται η κατοικία του.

Οπότε στο Postman στη θέση του url μπήκε : http://127.0.0.1:5000/getStudentAddress με method GET και στα headers του request σε μια παράμετρο authorization έχει μπει ως value το uuid που λάβαμε μετά το login : cd78359c-a76c-11eb-8e49-705a0f871404
Και στο body του request : 

{ "email": "tannerwilson@ontagene.com" }

Και επιστρέφεται μήνυμα : 

{
    "name": "Tanner Wilson",
    "street": "Halsey Street",
    "postcode": 13832
}

<h2>Έβδομο endpoint :</h2>

Το συγκεκριμένο endpoint δέχεται στο body του request του χρήστη ένα json της μορφής :

{
    "email": "some email"
}

Αφού ο χρήστης έχει αυθεντικοποιηθεί, γίνεται ένας έλεγχος αν υπάρχει το email που έδωσε μέσα από το body του request στο collection Students. Αν δεν υπάρχει κάποιος φοιτητής με αυτό το email επιστρέφεται μήνυμα λάθους με response code 500, ενώ αν υπάρχει διαγράφεται ο φοιτητής και επιστρέφεται μήνυμα με response code 200 που λέει ότι ο φοιτητής διαγράφηκε.

Οπότε στο Postman στη θέση του url μπήκε : http://127.0.0.1:5000/deleteStudent με method DELETE και στα headers του request σε μια παράμετρο authorization έχει μπει ως value το uuid που λάβαμε μετά το login : cd78359c-a76c-11eb-8e49-705a0f871404
Και στο body του request : 

{ "email": "latashathompson@ontagene.com" }

Και επιστρέφεται μήνυμα : Latasha Thompson was deleted.

Αν ξανακαλέσουμε το endpoint με το ίδιο email επιστρέφεται μήνυμα : No student found with that email.

<h2>Όγδοο endpoint :</h2>

Το συγκεκριμένο endpoint δέχεται στο body του request του χρήστη ένα json της μορφής :

{
    "email": "some email",
    "courses": [
        {"course 1": 10}, 
        {"course 2": 3 }, 
        {"course 3": 8}
     ]
}

Αφού ο χρήστης έχει αυθεντικοποιηθεί, γίνεται ένας έλεγχος αν υπάρχει το email που έδωσε μέσα από το body του request στο collection Students. Αν δεν υπάρχει κάποιος φοιτητής με αυτό το email επιστρέφεται μήνυμα λάθους με response code 500, ενώ αν υπάρχει θα προστεθεί η λίστα με τα courses του φοιτητή : 
students.update_one({'email': data['email']}, {'$set': {"courses": data['courses'] }})

Οπότε στο Postman στη θέση του url μπήκε : http://127.0.0.1:5000/addCourses με method PATCH και στα headers του request σε μια παράμετρο authorization έχει μπει ως value το uuid που λάβαμε μετά το login : cd78359c-a76c-11eb-8e49-705a0f871404
Και στο body του request : 

{
    "email": "velazquezreilly@ontagene.com",
    "courses": [
        {"course 1": 10}, 
        {"course 2": 3 }, 
        {"course 3": 8}
    ]
} 

Και επιστρέφεται μήνυμα : Courses were added to the student Velazquez Reilly

Αν ανοίξουμε το command prompt και χρησιμοποιήσουμε την εντολή docker exec -it mongodb mongo για να χρησιμοποιήσουμε το mongo shell και αφού με την εντολή use InfoSys έχουμε πρόσβαση στην βάση δεδομένων InfoSys, και χρησιμοποιήσουμε την εντολή : db.Students.find({"email":"velazquezreilly@ontagene.com"})
Θα μας βγάλει ως αποτέλεσμα : { "_id" : ObjectId("5e99d0127a781a4aac69dad5"), "name" : "Velazquez Reilly", "email" : "velazquezreilly@ontagene.com", "yearOfBirth" : 1968, "gender" : "male", "courses" : [ { "course 1" : 10 }, { "course 2" : 3 }, { "course 3" : 8 } ] }

Που σημαίνει ότι όντως προστέθηκαν τα courses στον φοιτητή.

<h2>Ένατο endpoint :</h2>

Το συγκεκριμένο endpoint δέχεται στο body του request του χρήστη ένα json της μορφής :

{
    "email": "some email"
}

Αφού ο χρήστης έχει αυθεντικοποιηθεί, γίνεται ένας έλεγχος αν υπάρχει το email που έδωσε μέσα από το body του request στο collection Students. Αν δεν υπάρχει κάποιος φοιτητής με αυτό το email επιστρέφεται μήνυμα λάθους με response code 500, ενώ αν υπάρχει γίνεται έλεγχος για το αν ο φοιτητής έχει διαθέσιμα courses. Αν δεν υπάρχει η λίστα, επιστρέφεται μήνυμα λάθους με response code 500, ενώ αν υπάρχει γίνεται ένας ακόμη έλεγχος για να δούμε αν έχει περασμένα courses (value > 4).Αν δεν έχει περάσει ούτε ένα course επιστρέφεται μήνυμα λάθους με response code 500, ενώ αν έχει περάσει έστω ένα επιστρέφεται μήνυμα με το όνομά του και τα περασμένα courses.

Οπότε στο Postman στη θέση του url μπήκε : http://127.0.0.1:5000/getPassedCourses με method GET και στα headers του request σε μια παράμετρο authorization έχει μπει ως value το uuid που λάβαμε μετά το login : cd78359c-a76c-11eb-8e49-705a0f871404
Και στο body του request : 

{
    "email": "velazquezreilly@ontagene.com"
} 

Και επιστρέφεται μήνυμα : 

{
    "name": "Velazquez Reilly",
    "course 1": 10,
    "course 3": 8
}
Όπου είναι το όνομα του φοιτητή με όλα τα περασμένα μαθήματά του.

Αν προστέσουμε courses σε φοιτητή με μη προβιβάσιμο βαθμό, θα μας έβγαζε αντίστοιχο μήνυμα :
db.Students.find({"email":"tannerwilson@ontagene.com"})
{ "_id" : ObjectId("5e99cb577a781a4aac69da3c"), "name" : "Tanner Wilson", "email" : "tannerwilson@ontagene.com", "yearOfBirth" : 1962, "address" : [ { "street" : "Halsey Street", "city" : "Greenwich", "postcode" : 13832 } ], "courses" : [ { "course 1" : 4 }, { "course 2" : 3 }, { "course 3" : 3 } ] }

Και ξανακαλέσουμε το endpoint με body στο request :
{
    "email": "tannerwilson@ontagene.com"
} 
Θα επιστρέψει μήνυμα : Tanner Wilson has not passed any courses yet
