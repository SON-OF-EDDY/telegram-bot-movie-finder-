import telebot
import imdb

########################################################################

# IMDB STUFF


def search_for_keyword(keyword, number_of_items):
  ia = imdb.IMDb()
  movies = ia.search_movie(keyword)
  first_five = movies[:number_of_items]

  refined = []

  for movie in first_five:

    to_retrieve = movie.movieID

    search = ia.get_movie(to_retrieve)

    kind = search.data['kind']

    if kind == 'tv series':

      title = search.data['localized title']
      number_of_seasons = search.data['number of seasons']
      cover = search.data['cover url']
      genres = search.data['genres']

      movie_dictionary = {
        'kind': kind,
        'title': title,
        'number_of_seasons': number_of_seasons,
        'cover': cover,
        'genres': genres,
      }

    else:

      movie_title = search['title']

      year = search['year']

      cast = search['cast']

      final_cast = []
      if len(cast) >= 3:
        cast = cast[:3]
        for i in range(len(cast)):
          final_cast.append(str(cast[i]))
      else:
        final_cast.append(str(cast[0]))

      print(cast)

      cover = search.data['cover url']

      plot = search.data['plot outline']

      director = search['director'][0]

      video = search.data['videos']

      genres = search.data['genres']

      movie_dictionary = {
        'kind': kind,
        'title': movie_title,
        'year': year,
        'cast': final_cast,
        'genres': genres,
        'director': director,
        'plot': plot,
        'cover': cover,
        'video': video,
      }

    refined.append(movie_dictionary)

  return refined


########################################################################

# TELEGRAM STUFF

API_KEY = '5943105176:AAGvrfu598Q18xKQxnDJIj2SELZUqrYt6P8'
bot = telebot.TeleBot(API_KEY)


@bot.message_handler(commands=['movies'], content_types=['text'])
def movies_with_keyword(message):
  full_text = message.text
  keyword = full_text[8:]
  output = search_for_keyword(keyword, 1)

  for entry in output:
    formatted = ''
    if entry['kind'] == 'tv series':
      formatted += f"Title: {entry['title']}\nType: {entry['kind']}\nNo. of seasons: {entry['number_of_seasons']}\nGenres: {entry['genres']}"
    else:
      formatted += f"Title: {entry['title']}\nType: {entry['kind']}\nYear: {entry['year']}\nGenres: {entry['genres']}\nDirector: {entry['director']}\nCast: {entry['cast']}\nVideo: {entry['video'][0]}"
    bot.send_photo(message.chat.id, entry['cover'])
    bot.send_message(message.chat.id, formatted)


bot.polling()