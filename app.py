from flask import Flask, render_template, request, session, url_for

#import yaml
from PIL import Image
import pytesseract
import re
import nltk
import sqlite3
#import csv
#import pandas as pd
from nltk.corpus import stopwords    
#from nltk.stem.porter import PorterStemmer
#from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from collections import Counter

from werkzeug.utils import redirect

app = Flask(__name__)





@app.route('/',methods=['GET','POST'])
def login():
    # connection = sqlite3.connect('student.db')
    # with open('student.sql') as f:
    #     connection.executescript(f.read())
    # cursor = connection.cursor()
    # cursor.execute("INSERT INTO user (username, passwordd) VALUES ('nandita', '12345')")

    # username = request.form.get('username')
    # password = request.form.get('password')
    # #statement = ("SELECT username, passwordd from user WHERE username = {username} AND passwordd = {password}".format(username=username,password=password))
    # row = cursor.execute("SELECT username, passwordd FROM user WHERE username = ? AND passwordd = ?", (username,password))
    # row = row.fetchall()
    # print(row)
    # connection.commit()
    # connection.close()
    # if len(row)==1:  # An empty result evaluates to False.
    #     return render_template("index.html")
    # else:
    #     message = "Invalid User"

    r = ""
    message = ""
    if (request.method == 'POST'):
        username = request.form['username']
        password = request.form['password']
        connection = sqlite3.connect('student.db')
        cursor = connection.cursor()

        cursor.execute("SELECT * from user WHERE username = '"+username+"' AND passwordd = '"+password+"' ")
        r = cursor.fetchall()
        for i in r:
            if (username==i[1] and password==i[2]):
                session["loggedin"] = True
                session["username"] = username
                return redirect(url_for("index"))
            else:
                message = "Invalid Please enter valid Username and Password"


    return render_template("login.html",message=message)


    




@app.route('/index')
def index():       
    return render_template('index.html',username=session["username"])


@app.route('/index')
def getKeywords():
    keywords = request.form['keywords']
    return keywords

def getName():
    name = request.form['name']
    return name

def getEmail():
    email = request.form['email']
    return email

def getQuestion():
    question = request.form['question']
    return question




@app.route('/index',methods=['POST','GET'])
def answer_evaluation():

    connection = sqlite3.connect('database.db')
    #with open('schema.sql') as f:
        #connection.executescript(f.read())
    cur = connection.cursor()

    name = getName()
    email = getEmail()
    question = getQuestion()
    
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    imagee = request.form['answer_sheet']
    file = Image.open(imagee)
    answer = pytesseract.image_to_string(file, lang='eng')
    
    # Tokenizing sentences
    #sentences = nltk.sent_tokenize(answer)

    # Tokenizing words
    words = nltk.word_tokenize(answer)
    #Lematization
    #wordnet = WordNetLemmatizer()
    corpus = []
    for i in range(len(words)):
        review = re.sub('[^a-zA-Z]', ' ', words[i])
        review = review.lower()
        review = review.split()
        review = [word for word in review if not word in stopwords.words('english')]
        review = ' '.join(review)
        corpus.append(review)
    corpus = list(filter(None,corpus))
    keywords = list(map(str, getKeywords().strip().split()))
    
    corpus_synonyms = []
    for i in range(len(corpus)):
        for syn in wordnet.synsets(corpus[i]):
            for l in syn.lemmas():
                corpus_synonyms.append(l.name())
    
    common = set(keywords) & set(corpus_synonyms)
    
    # count word occurrences
    a_vals = Counter(common)
    b_vals = Counter(keywords)
    # convert to word-vectors
    words  = list(a_vals.keys() | b_vals.keys())
    a_vect = [a_vals.get(word, 0) for word in words]        # [0, 0, 1, 1, 2, 1]
    b_vect = [b_vals.get(word, 0) for word in words]        # [1, 1, 1, 0, 1, 0]
    # find cosine-similarity
    len_a  = sum(av*av for av in a_vect) ** 0.5             # sqrt(7)
    len_b  = sum(bv*bv for bv in b_vect) ** 0.5             # sqrt(4)
    dot    = sum(av*bv for av,bv in zip(a_vect, b_vect))    # 3
    cosine = dot / (len_a * len_b) 
    cosine = cosine*100
    
    if(cosine>=90):
        Marks = 10
        cur.execute("INSERT INTO adminn (fname, email, question, keywords, mark_obtained) VALUES (?,?,?,?,?)",(name,email,question,str(keywords),Marks))
        cur.execute("SELECT * from adminn")
        results = cur.fetchall()
        print(results)
        connection.commit()
        connection.close()
        return render_template('pass.html', mark=Marks, name=name, email=email, question=question)    
    elif(89.99>=cosine>=80):
        Marks = 9
        cur.execute("INSERT INTO adminn (fname, email, question, keywords, mark_obtained) VALUES (?,?,?,?,?)",(name,email,question,str(keywords),Marks))
        cur.execute("SELECT * from adminn")
        results = cur.fetchall()
        print(results)
        connection.commit()
        connection.close()
        return render_template('pass.html', mark=Marks, name=name, email=email, question=question)
    elif(79.99>=cosine>=70):
        Marks = 8
        cur.execute("INSERT INTO adminn (fname, email, question, keywords, mark_obtained) VALUES (?,?,?,?,?)",(name,email,question,str(keywords),Marks))
        cur.execute("SELECT * from adminn")
        results = cur.fetchall()
        print(results)
        connection.commit()
        connection.close()
        return render_template('pass.html', mark=Marks, name=name, email=email, question=question)
    elif(69.99>=cosine>=60):    
        Marks = 7
        cur.execute("INSERT INTO adminn (fname, email, question, keywords, mark_obtained) VALUES (?,?,?,?,?)",(name,email,question,str(keywords),Marks))
        cur.execute("SELECT * from adminn")
        results = cur.fetchall()
        print(results)
        connection.commit()
        connection.close()
        return render_template('pass.html', mark=Marks, name=name, email=email, question=question)
    elif(59.99>=cosine>=50):
        Marks = 6
        cur.execute("INSERT INTO adminn (fname, email, question, keywords, mark_obtained) VALUES (?,?,?,?,?)",(name,email,question,str(keywords),Marks))
        cur.execute("SELECT * from adminn")
        results = cur.fetchall()
        print(results)
        connection.commit()
        connection.close()
        return render_template('pass.html', mark=Marks, name=name, email=email, question=question)
    elif(49.99>=cosine>=40):
        Marks = 5
        cur.execute("INSERT INTO adminn (fname, email, question, keywords, mark_obtained) VALUES (?,?,?,?,?)",(name,email,question,str(keywords),Marks))
        cur.execute("SELECT * from adminn")
        results = cur.fetchall()
        print(results)
        connection.commit()
        connection.close()
        return render_template('pass.html', mark=Marks, name=name, email=email, question=question)
    elif(39.99>=cosine>=30):
        Marks = 4
        cur.execute("INSERT INTO adminn (fname, email, question, keywords, mark_obtained) VALUES (?,?,?,?,?)",(name,email,question,str(keywords),Marks))
        cur.execute("SELECT * from adminn")
        results = cur.fetchall()
        print(results)
        connection.commit()
        connection.close()
        return render_template('pass.html', mark=Marks, name=name, email=email, question=question)
    elif(29.99>=cosine>=20):
        Marks = 3
        cur.execute("INSERT INTO adminn (fname, email, question, keywords, mark_obtained) VALUES (?,?,?,?,?)",(name,email,question,str(keywords),Marks))
        cur.execute("SELECT * from adminn")
        results = cur.fetchall()
        print(results)
        connection.commit()
        connection.close()
        return render_template('pass.html', mark=Marks, name=name, email=email, question=question)
    elif(19.99>=cosine>=10):
        Marks = 2
        cur.execute("INSERT INTO adminn (fname, email, question, keywords, mark_obtained) VALUES (?,?,?,?,?)",(name,email,question,str(keywords),Marks))
        cur.execute("SELECT * from adminn")
        results = cur.fetchall()
        print(results)
        connection.commit()
        connection.close()
        return render_template('pass.html', mark=Marks, name=name, email=email, question=question)
    elif(9.99>=cosine>=1):
        Marks = 1
        cur.execute("INSERT INTO adminn (fname, email, question, keywords, mark_obtained) VALUES (?,?,?,?,?)",(name,email,question,str(keywords),Marks))
        cur.execute("SELECT * from adminn")
        results = cur.fetchall()
        print(results)
        connection.commit()
        connection.close()
        return render_template('pass.html', mark=Marks, name=name, email=email, question=question)
    else:
        Marks = 0
        cur.execute("INSERT INTO adminn (fname, email, question, keywords, mark_obtained) VALUES (?,?,?,?,?)",(name,email,question,str(keywords),Marks))
        cur.execute("SELECT * from adminn")
        results = cur.fetchall()
        print(results)
        connection.commit()
        connection.close()
        return render_template('pass.html', mark=Marks, name=name, email=email, question=question)
    


if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug=True)