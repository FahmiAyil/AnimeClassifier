from conndb import database
from lxml import html
import requests

#web dan konten
url = requests.get("https://myanimelist.net/anime.php")
konten = html.fromstring(url.content)

# konten yang diambil
get_konten = konten.xpath("//div[@class='genre-list al']/a")
get_konten = get_konten[0:15]

for isi in get_konten:
    # potong kata dengan delimiter "("
    genre = isi.text.split(" (")
    genre = genre[0]
    href = ""
    genre_url = ""
    pry = ""

    # ambil link dr isi konten
    if "href" in isi.attrib:
        href = isi.attrib["href"]
        genre_url = "https://myanimelist.net" + href

    print ("Genre    : " + genre)

    # buka detail halaman genre
    detail_genre = requests.get(genre_url)
    konten_detail_genre = html.fromstring(detail_genre.content)
    get_judul_anime = konten_detail_genre.xpath("//p[@class='title-text']/a")
    get_synopsis = konten_detail_genre.xpath("//div[@class='synopsis js-synopsis']/span")
    get_episodes = konten_detail_genre.xpath("//div[@class='eps']/a/span")
    get_rating = konten_detail_genre.xpath("//div[@class='scormem']/span[@class='score']")

    get_judul_anime = get_judul_anime[0:15]
    # menghindari error utf-8 dikasih try except
    try:
        for i in range(len(get_judul_anime)):
            anime_url = ""
            href = ""
            synopsis = ""
            episodes = ""
            rating = ""
            judul_anime = get_judul_anime[i].text.encode("ascii", "replace")
            #  ambil link dr isi konten
            if "href" in get_judul_anime[i].attrib:
                href = get_judul_anime[i].attrib["href"]
                anime_url = href.encode("ascii", "replace")

            # <Mengatasi utf 8 eror
            synopsis = get_synopsis[i].text.encode("ascii", "replace")
            episodes = get_episodes[i].text
            # menghilangkan spasi
            rating = get_rating[i].text.replace("\n", "")
            rating = rating.replace(" ", "")

            print("Anime    : ", judul_anime)
            print("     URL anime   : ", anime_url)
            print("     Sinopsis    : ", synopsis)
            print("     Episodes    : ", episodes)
            print("     rating      : ", rating)

            # DATABASE operation
            sql_check_pry = "SELECT link FROM anime"
            database.dbcursor.execute(sql_check_pry)
            pry = database.dbcursor.fetchall()


            # check link primary dan yang akan ditambah
            if any(anime_url.decode("UTF-8") in c for c in pry):
                print("LINK SUDAH ADA")
            else:
                sql_insert_data = "INSERT INTO anime (link, judul_anime, genre, sinopsis, episode, rating)\
                VALUES (%s, %s, %s, %s, %s, %s)"
                database.dbcursor.execute(sql_insert_data, (anime_url, judul_anime, genre, synopsis, episodes, rating))
                database.conn.commit()
                print ("LINK DITAMBAHKAN")


    except Exception as e:
        print(e, "------Error-------")
        pass


    print("")
    print ("Akhir dari for inti")
