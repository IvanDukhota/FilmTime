import os
import requests
import re
import tmdbsimple as tmdb
from yt_dlp import YoutubeDL
from django.core.management.base import BaseCommand
from DataBase.models import *

TMDB_API_KEY = 'a156846e2c691ef1efd0fe54cdcda912'

tmdb.API_KEY = TMDB_API_KEY


class Command(BaseCommand):
    help = 'Парсинг фільмів та серіалів з TMDB API'

    def add_arguments(self, parser):
        parser.add_argument('--type', type=str, choices=['movie', 'series'], required=True, help='Тип контенту: movie або series')
        parser.add_argument('--count', type=int, default=10, help='Кількість записів для парсингу (за замовчуванням 10)')
        parser.add_argument('--start_date', type=str, help='Початкова дата (формат YYYY-MM-DD)')
        parser.add_argument('--end_date', type=str, help='Кінцева дата (формат YYYY-MM-DD)')

    def handle(self, *args, **options):
        content_type = options['type']
        count = options['count']
        start_date = options.get('start_date')
        end_date = options.get('end_date')

        self.stdout.write(f"Початок парсингу для типу {content_type}...")
        if content_type == 'movie':
            self.parse_movies(count, start_date, end_date)
        elif content_type == 'series':
            self.parse_series(count, start_date, end_date)
        self.stdout.write("Парсинг завершено!")

    def parse_movies(self, count, start_date, end_date):
        discover = tmdb.Discover()
        params = {
            'sort_by': 'popularity.desc',
            'page': 1,
            'primary_release_date.gte': start_date,
            'primary_release_date.lte': end_date,
        }

        results = discover.movie(**params)['results'][:count]

        for movie in results:
            movie_details = tmdb.Movies(movie['id']).info()
            title = movie_details['title']
            release_date = movie_details.get('release_date', '')
            synopsis = movie_details.get('overview', '')
            cover_url = f"https://image.tmdb.org/t/p/w500{movie_details['poster_path']}" if movie_details.get('poster_path') else None
            duration = movie_details.get('runtime', 0)

            if not movie_details.get('poster_path'):
                self.stdout.write(f"У фільму {movie_details['title']} немає постера.")

            cover_path = self.save_media(cover_url, title, folder='covers')
            trailer_path = self.get_trailer_and_save(movie['id'], 'movie', title)

            content, created = Content.objects.get_or_create(
                title=title,
                defaults={
                    'release_date': release_date,
                    'content_type': 'movie',
                    'trailer_url': trailer_path,
                    'synopsis': synopsis,
                    'cover_image': cover_path,
                }
            )

            if created:
                Movie.objects.get_or_create(
                    content=content,
                    defaults={
                        'duration': duration,
                        'critic_rating': movie_details.get('vote_average', 0.0),
                        'content_url': f"https://www.themoviedb.org/movie/{movie['id']}"
                    }
                )
                self.add_directors_and_cast(movie['id'], content, 'movie')
                self.add_genres(movie['id'], content, 'movie')
                self.stdout.write(f"Фільм {title} успішно доданий!")
            else:
                self.stdout.write(f"Фільм {title} вже існує у базі даних.")


    def parse_series(self, count, start_date, end_date):
        discover = tmdb.Discover()
        params = {
            'sort_by': 'popularity.desc',
            'page': 1,
            'first_air_date.gte': start_date,
            'first_air_date.lte': end_date,
        }
        results = discover.tv(**params)['results'][:count]


        for tv in results:
            series_details = tmdb.TV(tv['id']).info()
            title = series_details['name']
            release_date = series_details.get('first_air_date', '')
            synopsis = series_details.get('overview', '')
            cover_url = f"https://image.tmdb.org/t/p/w500{series_details['poster_path']}" if series_details.get('poster_path') else None

            cover_path = self.save_media(cover_url, title, folder='covers')
            trailer_path = self.get_trailer_and_save(tv['id'], 'tv', title)

            content, created = Content.objects.get_or_create(
                title=title,
                defaults={
                    'release_date': release_date,
                    'content_type': 'series',
                    'trailer_url': trailer_path,
                    'synopsis': synopsis,
                    'cover_image': cover_path,
                }
            )

            if created:
                series, _ = Series.objects.get_or_create(content=content)

                for season_data in series_details.get('seasons', []):
                    season_number = season_data['season_number']
                    season_details = tmdb.TV_Seasons(tv['id'], season_number).info()
                    release_date = season_details.get('air_date', '')
                    critic_rating = season_details.get('vote_average', 0.0)

                    season, _ = Season.objects.get_or_create(
                        series=series,
                        number=season_number,
                        defaults={
                            'release_date': release_date,
                            'critic_rating': critic_rating,
                        }
                    )

                    for episode_data in season_details.get('episodes', []):
                        episode_number = episode_data['episode_number']
                        title_episod = episode_data['name']
                        release_date = episode_data.get('air_date', '')
                        duration = episode_data.get('runtime', 0) or 0
                        critic_rating = episode_data.get('vote_average', 0.0)
                        episode_url = f"https://www.themoviedb.org/tv/{tv['id']}/season/{season_number}/episode/{episode_number}"

                        Episode.objects.get_or_create(
                            season=season,
                            number=episode_number,
                            defaults={
                                'title': title_episod,
                                'release_date': release_date,
                                'duration': duration,
                                'critic_rating': critic_rating,
                                'episode_url': episode_url,
                            }
                        )

                self.add_directors_and_cast(tv['id'], content, 'tv')
                self.add_genres(tv['id'], content, 'tv')
                self.stdout.write(f"Серіал {title} успішно доданий!")
            else:
                self.stdout.write(f"Серіал {title} вже існує у базі даних.")


    def save_media(self, url, title, folder):
        if not url:
            self.stdout.write(f"URL для {title} відсутній. Пропускаю завантаження.")
            return None

        try:
            response = requests.get(url, stream=True, timeout=10)
            if response.status_code != 200:
                self.stdout.write(f"Помилка завантаження зображення для {title}. URL: {url}. Статус: {response.status_code}")
                return None
        except requests.exceptions.RequestException as e:
            self.stdout.write(f"Виняток при завантаженні зображення для {title}. URL: {url}. Помилка: {str(e)}")
            return None

        try:
            safe_title = re.sub(r'[<>:"/\\|?*]', '_', title).replace(' ', '_')
            if not safe_title.endswith('.jpg'):
                safe_title += '.jpg'


            media_folder = 'media'
            full_folder_path = os.path.join(media_folder, folder)
            os.makedirs(full_folder_path, exist_ok=True)
            full_file_path = os.path.join(full_folder_path, safe_title)
            relative_path = os.path.join(folder, safe_title)

        except Exception as e:
            self.stdout.write(f"Помилка створення каталогу для {title}. Шлях: {full_file_path}. Помилка: {str(e)}")
            return None

        try:
            with open(full_file_path, 'wb') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            self.stdout.write(f"Зображення для {title} успішно збережено. Шлях: {full_file_path}")
            return relative_path
        except Exception as e:
            self.stdout.write(f"Помилка запису зображення для {title}. Шлях: {full_file_path}. Помилка: {str(e)}")
            return None

    def get_trailer_and_save(self, content_id, content_type, title):
        try:
            safe_title = re.sub(r'[<>:"/\\|?*]', '_', title).replace(' ', '_')
            if not safe_title.endswith('_trailer.mp4'):
                safe_title += '_trailer.mp4'

            media_folder = 'media'
            trailers_folder = os.path.join(media_folder, 'trailers')
            os.makedirs(trailers_folder, exist_ok=True)

            full_file_path = os.path.join(trailers_folder, safe_title)
            relative_file_path = os.path.join('trailers', safe_title)

            if content_type == 'movie':
                videos = tmdb.Movies(content_id).videos()
            elif content_type == 'tv':
                videos = tmdb.TV(content_id).videos()
            else:
                return None

            for video in videos['results']:
                if video['type'] == 'Trailer' and video['site'] == 'YouTube':
                    youtube_url = f"https://www.youtube.com/watch?v={video['key']}"
                    self._download_from_youtube(youtube_url, full_file_path)
                    return relative_file_path

            return self.download_trailer_from_youtube(title, full_file_path)

        except Exception as e:
            self.stdout.write(f"Помилка отримання трейлера: {str(e)}")
            return None

    def download_trailer_from_youtube(self, title, full_file_path):
        ydl_opts = {
            'format': 'best',
            'outtmpl': full_file_path,
            'quiet': True,
        }
        try:
            with YoutubeDL(ydl_opts) as ydl:
                search_query = f"{title} trailer"
                info = ydl.extract_info(f"ytsearch:{search_query}", download=True)
                return os.path.relpath(ydl.prepare_filename(info['entries'][0]), 'media')
        except Exception as e:
            self.stdout.write(f"Помилка завантаження трейлера з YouTube: {str(e)}")
            return None

    def _download_from_youtube(self, youtube_url, full_file_path):
        ydl_opts = {
            'format': 'best',
            'outtmpl': full_file_path,
            'quiet': True,
        }
        try:
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([youtube_url])
        except Exception as e:
            self.stdout.write(f"Помилка завантаження з YouTube за URL: {str(e)}")


    def add_directors_and_cast(self, content_id, content, content_type):
        try:
            if content_type == 'movie':
                credits = tmdb.Movies(content_id).credits()
            elif content_type == 'tv':
                credits = tmdb.TV(content_id).credits()
            else:
                return

            for crew in credits['crew']:
                if crew['job'] == 'Director':
                    director, _ = Director.objects.get_or_create(name=crew['name'])
                    ContentDirector.objects.get_or_create(content=content, director=director)

            for cast in credits['cast'][:10]:
                actor, _ = Actor.objects.get_or_create(name=cast['name'])
                ContentActor.objects.get_or_create(
                    content=content,
                    actor=actor,
                    character_name=cast['character']
                )
        except Exception as e:
            self.stdout.write(f"Помилка при додаванні режисерів/акторів: {str(e)}")

    def add_genres(self, content_id, content, content_type):
        try:
            if content_type == 'movie':
                details = tmdb.Movies(content_id).info()
            elif content_type == 'tv':
                details = tmdb.TV(content_id).info()
            else:
                return

            genres = details.get('genres', [])
            added_genres = []

            for genre_data in genres:
                genre, _ = Genre.objects.get_or_create(name=genre_data['name'])

                ContentGenres.objects.get_or_create(content=content, genre=genre)

                added_genres.append(genre)

            self.notify_users_about_new_content(added_genres, content)

        except Exception as e:
            self.stdout.write(f"Помилка при додаванні жанрів: {str(e)}")

    def notify_users_about_new_content(self, genres, content):
        genre_ids = [genre.id for genre in genres]
        matching_users = UserProfile.objects.filter(
            usergenres__genre__id__in=genre_ids
        ).distinct()

        genre_names = ", ".join([genre.name for genre in genres])
        notification_text = f"Новий контент у ваших улюблених жанрах: {genre_names}! Назва фільму: {content.title}."

        notification = Notification.objects.create(
            content=content,
            text=notification_text
        )

        user_notifications = [
            UserProfileNotifications(
                userprofile=user_profile,
                notification=notification,
                status="unread"
            )
            for user_profile in matching_users
        ]

        UserProfileNotifications.objects.bulk_create(user_notifications)

        print(f"Створено {len(user_notifications)} сповіщень для користувачів.")




