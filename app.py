from flask import Flask, render_template, request, abort

app = Flask(__name__)

PROMPT = """Привет, до Нового Года осталось ... дней. Настраиваемся на праздничное настроение оливьешки и салюта.
Перейдите на /about чтобы посмотреть инфрмацию
Перейдите на /playlists чтобы посмотреть плейлисты 
Перейдите на /videos/ чтобы посмотреть видео"""

videos = {
    1: {"id": "1", "title": "Wham! - Last Christmas (Official 4K Video Video)",
        "videoid": "https://ok.ru/videoembed/1513983316419"},
    2: {"id": "2", "title": "Mariah Carey - All I Want For Christmas Is You (Official Music Video)",
        "videoid": "https://ok.ru/videoembed/6531909100"},
    3: {"id": "3", "title": "Abba - Happy New Year (Official Video)",
        "videoid": "https://ok.ru/videoembed/950544894691"},
    4: {"id": "4", "title": "Новогодняя Реклама Coca-Cola", "videoid": "https://www.youtube.com/embed/li1K6YOG-jk"},
    5: {"id": "5", "title": "Frank sinatra - Let it snow", "videoid": "https://ok.ru/videoembed/206672628391"},
    6: {"id": "6", "title": "Frank Sinatra - Jingle Bells",
        "videoid": "https://ok.ru/videoembed/1395940462938"},
    7: {"id": "7", "title": "Andrea Bocelli - Santa Claus Is Coming To Town (Official Video)",
        "videoid": "https://my.mail.ru/video/embed/158376979169542652"},
    8: {"id": "8", "title": "Enya - We Wish You A Merry Christmas",
        "videoid": "https://www.youtube.com/embed/Dt9l_SVvyRc"},
    9: {"id": "9", "title": "Kelly Clarkson, ft. Trisha Yearwood, Reba McEntire - Silent Night",
        "videoid": "https://www.youtube.com/embed/5BRVkgaIcaE"},
    10: {"id": "10", "title": "Billy Mack - Christmas Is All Around",
         "videoid": "https://www.youtube.com/embed/5Jo08wyCdUg"},
    11: {"id": "11", "title": "Alan Jackson - A holly jolly Christmas",
         "videoid": "https://www.youtube.com/embed/LoJAawcG_iY"},
    12: {"id": "12", "title": "Hayley Westenra, Russell Watson, Aled Jones - Twelve"
                              "Days of Christmas (Songs of Praise)",
         "videoid": "https://www.youtube.com/embed/T-cjK3f87jI"},
    13: {"id": "13", "title": "The Carpenters - Merry Christmas, Darling",
         "videoid": "https://www.youtube.com/embed/YR1ujXx2p-I"},
    14: {"id": "14", "title": "Chris Rea - Driving Home For Christmas (Official Music Video)",
         "videoid": "https://www.youtube.com/embed/czhZbqpyBm8"},
    15: {"id": "15", "title": "Darlene Love - All Alone On Christmas",
         "videoid": "https://www.youtube.com/embed/r1uJPGRfO5Y"},
    16: {"id": "16", "title": "Пять минут (из кинофильма 'Карнавальная ночь')",
         "videoid": "https://ok.ru/videoembed/500916423173"},
    17: {"id": "17", "title": "Соло феи Драже из балета щелкунчик ",
         "videoid": "https://www.youtube.com/embed/TdHL6brKMrc"},
    18: {"id": "18", "title": "Лариса Долина - Три белых коня", "videoid": "https://www.youtube.com/embed/jWiKX6wE9fY"},
    19: {"id": "19", "title": "ВИА Пламя - Снег кружится", "videoid": "https://www.youtube.com/embed/5tMMoYDh7Lc"},
    20: {"id": "20", "title": "Эдуард Хиль - Зима", "videoid": "https://www.youtube.com/embed/osBPrU0k21s"},
    21: {"id": "21", "title": "Жанна Агузарова - А снег идет", "videoid": "https://www.youtube.com/embed/vc6mB77esAI"},
    22: {"id": "22", "title": "Расскажи, Снегурочка! (м/ф Ну, погоди)",
         "videoid": "https://www.youtube.com/embed/qU44b9zk4FQ"},
    23: {"id": "23", "title": "Новогодняя песня (м/ф Маша и Медведь)",
         "videoid": "https://www.youtube.com/embed/ag02EEdIdZo"},
    24: {"id": "24", "title": "Валентина Толкунова - Кабы не было зимы",
         "videoid": "https://www.youtube.com/embed/_WL0utq-seo"},
    25: {"id": "25", "title": "В лесу родилась Елочка - детская новогодняя песня",
         "videoid": "https://www.youtube.com/embed/VAG1UTfDSjY"},
    26: {"id": "26", "title": "Дискотека Авария – Новогодняя", "videoid": "https://www.youtube.com/embed/nd_CYqU7VGA"},
    27: {"id": "27", "title": "София Ротару - Белая зима", "videoid": "https://www.youtube.com/embed/4d_y-TFbiC8"},
    28: {"id": "28", "title": "Блестящие и А-мега - Новый год", "videoid": "https://www.youtube.com/embed/Pf76lLHGYBY"},
    29: {"id": "29", "title": "Валерий Меладзе - Ночь накануне Рождества",
         "videoid": "https://www.youtube.com/embed/P8DrXqp7pks"},
    30: {"id": "30", "title": "Григорий Гладков - Падал прошлогодний снег финал",
         "videoid": "https://www.youtube.com/embed/0d_a_kyb_lw"},
    31: {"id": "31", "title": "Никого не будет в доме (песня из к/ф 'Ирония судьбы, или С легким паром!')",
         "videoid": "https://www.youtube.com/embed/n24BCHXB9V0"},
    32: {"id": "32", "title": "Микаэл Таривердиев - Музыка из к/ф 'Ирония судьбы, или С легким паром!'",
         "videoid": "https://www.youtube.com/embed/LqWh8H8mQvw"},
    33: {"id": "33", "title": "Семён Слепаков - Тяжёлый год", "videoid": "https://www.youtube.com/embed/5P6ADakiwcg"},
    34: {"id": "34", "title": "Дмитрий Маликов, Дайкири - Снежинка",
         "videoid": "https://www.youtube.com/embed/goSfBN9KugE"},
    35: {"id": "35", "title": "Звенит Январская вьюга (из к/ф Иван Васильевич меняет профессию)",
         "videoid": "https://www.youtube.com/embed/q1qzEiEUgO0"},
    36: {"id": "36", "title": "Perry Como - Magic Moments", "videoid": "https://www.youtube.com/embed/eXQTRqygi6w"},
    37: {"id": "37", "title": "Женя Любич - Новогодняя", "videoid": "https://ok.ru/videoembed/427948052946"},
}

playlists = {
    "Отечественные исполнители": {
        "id": "1",
        "wrap": "/static/1.jpg",
        "title": "Отечественные исполнители",
        "videos": [16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 37]
    },
    "Зарубежные артисты": {
        "id": "2",
        "wrap": "/static/2.jpg",
        "title": "Зарубежные исполнители",
        "videos": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 36]
    },
    "Рождество": {
        "id": "3",
        "wrap": "/static/3.jpeg",
        "title": "Рождественский плейлист",
        "videos": [1, 2, 5, 6, 8, 10, 11, 12, 13, 14, 15, 36]
    },
    "Новый год": {
        "id": "4",
        "wrap": "/static/4.jpg",
        "title": "Новогодний плейлист",
        "videos": [3, 4, 7, 9, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 37]
    },
    "Саундтреки": {
        "id": "5",
        "wrap": "/static/5.jpg",
        "title": "Песни из фильмов, мультфильмов и рекламных роликов",
        "videos": [2, 4, 10, 17, 15, 18, 22, 23, 24, 30, 35]
    },
    "Романтика": {
        "id": "6",
        "wrap": "/static/6.jpg",
        "title": "Романтичный Новый год",
        "videos": [1, 2, 10, 13, 14, 31, 32, 35]
    },
    "Реализм": {
        "id": "7",
        "wrap": "/static/7.jpg",
        "title": "Актуальные :D",
        "videos": [26, 33]
    },
}

USER_TEXT = "Ничего не найдено! Хлопни игристого и приходи позже!"


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/')
def main():
    output = render_template('index.html', playlist=playlists)
    return output


@app.route('/videos/<playlist_id>/')
def playlist_videos(playlist_id):
    playlist = playlists.get(playlist_id)
    video_id = playlist.get('videos')[0]
    video = videos.get(video_id)
    output = render_template('videos.html', videos=videos, video=video, playlist=playlist, playlist_id=playlist_id)
    return output


@app.route('/videos/<playlist_id>/<int:video_id>/')
def show_videos(playlist_id, video_id):
    playlist = playlists.get(playlist_id)
    if not video_id in playlist["videos"]:
        abort(404)
    video = videos.get(video_id)
    output = render_template('videos.html', videos=videos, video=video, playlist=playlist, playlist_id=playlist_id)
    return output


@app.route('/search', methods=['GET', 'POST'])
def search():
    search_videos = []
    if request.method == "POST":
        s = request.form['s']
        for item in videos.values():
            if s.lower() in item["title"].lower():
                search_videos.append(item)
    else:
        s = ''
    output = render_template("search.html", playlist=playlists, search_videos=search_videos, s=s)
    return output


@app.errorhandler(404)
def error(e):
    output = render_template('404.html')
    return output


if __name__ == '__main__':
    app.run()
