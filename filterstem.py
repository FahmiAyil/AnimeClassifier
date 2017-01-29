from conndb import database
import re
from nltk.stem import *
from nltk.corpus import stopwords
import pickle
import base64

sql_check_pry = "SELECT link,sinopsis FROM anime"
database.dbcursor.execute(sql_check_pry)
anime = database.dbcursor.fetchall()

for counter in range(len(anime)):
    temp_link = anime[counter][0]
    try:
        # mengambil sinopsis
        temp_syn = anime[counter][1]
        # case folding
        syn_lower = temp_syn.lower()
        # tokenizing
        syn_tokenize = re.findall(r"[\w]+", syn_lower)
        print("Token ", syn_tokenize)
        # remove stopwords
        stopword = stopwords.words("english")
        syn_stopw = []
        for word in syn_tokenize:
            if word not in stopword:
                syn_stopw.append(word)
        print("Stopw ", syn_stopw)
        # stemming
        stemmer = PorterStemmer()
        for s in range(len(syn_stopw)):
            syn_stopw[s] = stemmer.stem(syn_stopw[s])
        print("Stemm ", syn_stopw)
        print(counter,"----------------------------------------------")

        # DATABASE operation
        sql_check_pry = "SELECT link FROM stemword"
        database.dbcursor.execute(sql_check_pry)
        pry = database.dbcursor.fetchall()

        # CHECK DATABASE
        if any(temp_link in c for c in pry):
            print("DUMP SUDAH ADA")
        else:
            sql_insert_data = "INSERT INTO stemword (link, word_list)\
            VALUES (%s, %s)"
            # MEMASUKKAN PADA DICT
            kamus = {}
            for kata in syn_stopw:
                if kata not in kamus:
                    kamus[kata] = 0
                kamus[kata] += 1
            # PROSES DUMP
            syn_dump = pickle.dumps(kamus)
            print(syn_dump)
            syn_enc = base64.b64encode(syn_dump)
            # INSERT DATA DUMP
            database.dbcursor.execute(sql_insert_data, (temp_link, syn_enc))
            database.conn.commit()
            print ("STEM DUMP DITAMBAHKAN")

        # INSERT KATA UNIK
        for w in syn_stopw:
            sql_check_word = "SELECT word FROM word"
            database.dbcursor.execute(sql_check_word)
            sword = database.dbcursor.fetchall()

            if any(w in sw for sw in sword):
                print("KATA UNIK SUDAH ADA")
            else:
                sql_insert_word = "INSERT INTO word (word)\
                VALUES (%s)"
                database.dbcursor.execute(sql_insert_word, (w))
                database.conn.commit()
                print ("KATA UNIK DITAMBAHKAN")

    except Exception as e:
        print(e)
        pass
