from conndb import database
import base64
import re
from nltk.stem import *
from nltk.corpus import stopwords
import pickle
import operator

link = "https://myanimelist.net/anime/666/JoJo_no_Kimyou_na_Bouken"
judul = "JoJo no Kimyou na Bouken"
sinopsis = """By A.D. 2010, all men have died off quickly due to a dramatic change in the environment and an unknown contaminant. The population decreased to the lowest number ever seen...until only the women were left alive.

They live huddled in small corners of a world mostly reclaimed by nature.
There are those who accept their inevitable extinction and live a carefree life...
There are those who try to continue on the race with the help of science...
It is a society of constant conflict over their differences of principles and policies.

The story takes place in the center of Tokyo. It is one of the places left for them. The conflict over the specimen of "ICE" and the chance it may provide to save humanity begins."""
episode = "6 eps"
rating = "7.47"

link = link.encode("ascii", "replace").decode("utf-8")
sinopsis = sinopsis.encode("ascii", "replace").decode("utf-8")

print(link)
print(sinopsis)

# case folding
syn_lower = sinopsis.lower()
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
print("----------------------------------------------")

kamus = {}
for kata in syn_stopw:
    if kata not in kamus:
        kamus[kata] = 0
    kamus[kata] += 1
print(kamus)
syn_list_distinct = list(set(syn_stopw))

sql_check_pry = "SELECT link, genre FROM anime"
database.dbcursor.execute(sql_check_pry)
pry = database.dbcursor.fetchall()

if any(link in i for i in pry):
    print("LINK SUDAH ADA")
else:
    dbgenre = []
    for i in range(len(pry)):
        dbgenre.append(pry[i][1])
    dbgenre = sorted(list(set(dbgenre)))
    print(dbgenre)

    hasil = []
    dict_hasil = {}
    for c in dbgenre:

        count = "SELECT COUNT(*) FROM anime WHERE genre = %s"
        database.dbcursor.execute(count, (c))
        check = database.dbcursor.fetchone()

        sql = "SELECT a.link, a.genre, s.word_list FROM anime a JOIN stemword s ON a.link = s.link WHERE genre = %s"
        database.dbcursor.execute(sql, (c))
        data = database.dbcursor.fetchall()

        count_word = "SELECT COUNT(*) FROM word"
        database.dbcursor.execute(count_word)
        jml_kata = database.dbcursor.fetchone()[0]

        # MENGHITUNG RUMUS PCI.
        jml_doc = check[0]
        jml_data = len(pry)
        jml_pci = jml_doc/jml_data

        jml_freq = 0
        jml_fwc = 0
        temp_hasil = []

        for l in syn_list_distinct:
            print("     Kata yang di cari adalah ", l)
            for y in range(len(data)):

                kamus_raw = data[y][2]
                kamus_b64 = base64.b64decode(kamus_raw)
                kamus = pickle.loads(kamus_b64)

                if l in kamus:
                    jml_freq += kamus[l]

                jml_fwc += sum(kamus.values())

            print("         JUMLAH KEMUNCULAN KATA = ", jml_freq)
            print("         JUMLAH KATA PADA GENRE = ", jml_fwc)

            temp_hasil.append((jml_freq+1)/(jml_fwc+jml_kata))
            test = (jml_freq+1)/(jml_fwc+jml_kata)
            print(test)

            jml_fwc = 0
            jml_freq = 0

        kali = 1
        for t in temp_hasil:
            kali *= t

        hasil.append(kali*jml_pci)

        dict_hasil[c] = hasil[-1]
        print("*********************************************************")
        print("Hasil terhadap kategori",c, "adalah", hasil[-1])
        print("*********************************************************")

    genre = list(dict(sorted(dict_hasil.items(), key = operator.itemgetter(1), reverse = True)[:2]))
    print("2 GENRE PALING DEKAT DENGAN DATA YANG DICARI ADALAH =", genre[0] ,",", genre[1])
