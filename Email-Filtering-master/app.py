#coding: utf8
from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort
import os,easyimap,json
import pandas as pd
from sklearn import preprocessing
import nltk
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cross_validation import train_test_split
from sklearn import svm 
from sklearn import metrics

df = pd.read_table('SMSSpamCollection.txt', header=None)
le = preprocessing.LabelEncoder()
y = df[0]
y_enc = le.fit_transform(y)

raw_text = df[1]

processed = raw_text.str.replace(r'\b[\w\-.]+?@\w+?\.\w{2,4}\b','emailaddr')
processed = processed.str.replace(r'(http[s]?\S+)|(\w+\.[A-Za-z]{2,4}\S*)','httpaddr')
processed = processed.str.replace(r'£|\$', 'moneysymb')    
processed = processed.str.replace(r'\b(\+\d{1,2}\s)?\d?[\-(.]?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}\b','phonenumbr')    
processed = processed.str.replace(r'\d+(\.\d+)?', 'numbr')
processed = processed.str.replace(r'[^\w\d\s]', ' ')
processed = processed.str.replace(r'\s+', ' ')
processed = processed.str.replace(r'^\s+|\s+?$', '')
processed = processed.str.lower()
stop_words = nltk.corpus.stopwords.words('english')
processed = processed.apply(lambda x: ' '.join(
    term for term in x.split() if term not in set(stop_words))
)
porter = nltk.PorterStemmer()
processed = processed.apply(lambda x: ' '.join(
    porter.stem(term) for term in x.split())
)

vectorizer = TfidfVectorizer(ngram_range=(1, 2))
X_ngrams = vectorizer.fit_transform(processed)

X_train, X_test, y_train, y_test = train_test_split(
    X_ngrams,
    y_enc,
    test_size=0.2,
    random_state=42,
    stratify=y_enc
)

clf = svm.LinearSVC(loss='hinge')
clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)

pd.DataFrame(
    metrics.confusion_matrix(y_test, y_pred),
    index=[['actual', 'actual'], ['spam', 'ham']],
    columns=[['predicted', 'predicted'], ['spam', 'ham']]
)

def preprocess_text(messy_string):
    #assert(type(messy_string) == str)
    cleaned = re.sub(r'\b[\w\-.]+?@\w+?\.\w{2,4}\b', 'emailaddr', messy_string)
    cleaned = re.sub(r'(http[s]?\S+)|(\w+\.[A-Za-z]{2,4}\S*)', 'httpaddr',
                     cleaned)
    cleaned = re.sub(r'£|\$', 'moneysymb', cleaned)
    cleaned = re.sub(
        r'\b(\+\d{1,2}\s)?\d?[\-(.]?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}\b',
        'phonenumbr', cleaned)
    cleaned = re.sub(r'\d+(\.\d+)?', 'numbr', cleaned)
    cleaned = re.sub(r'[^\w\d\s]', ' ', cleaned)
    cleaned = re.sub(r'\s+', ' ', cleaned)
    cleaned = re.sub(r'^\s+|\s+?$', '', cleaned.lower())
    return ' '.join(
        porter.stem(term) 
        for term in cleaned.split()
        if term not in set(stop_words)
    )

def spam_filter(message):
    if clf.predict(vectorizer.transform([preprocess_text(message)])):
        return 'spam'
    else:
        return 'not spam'



#from collections import OrderedDict
app = Flask(__name__)

@app.route('/')
def login():
	return render_template('login.html')

@app.route('/result',methods=['POST','GET'])
def result():
	if request.method == 'POST':
		userText1 = request.form['email']
		userText2 = request.form['password']
		imapper = easyimap.connect('imap.gmail.com', userText1, userText2)
		spam = 0
		ham = 0
		spam_list=[]
		ham_list=[]
		for mail_id in imapper.listids(limit=50):
			mail = imapper.mail(mail_id)
			message_text = mail.body
			result_type=spam_filter(message_text)
			print(result_type)
			if result_type == "spam":
				spam=spam+1
				spam_list.append(mail.from_addr)
			else:
				ham=ham+1	
				ham_list.append(mail.from_addr)
		result = [spam,ham]
		return render_template('result.html',result=result,ham_list=ham_list,spam_list=spam_list)

if __name__ == "__main__":
	app.secret_key = os.urandom(12)
	app.run(debug=True,host='0.0.0.0', port=4000)


