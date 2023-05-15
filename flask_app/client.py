import requests


class Anime(object):
    def __init__(self, anime):

        kitsu_json = anime['attributes']


        self.anime_id=anime['id']
        self.title= kitsu_json['canonicalTitle']
        self.synopsis = kitsu_json['synopsis']
        self.small_poster = kitsu_json['posterImage']['small'] 
        self.med_poster = kitsu_json['posterImage']['medium'] 
        self.epi_count = kitsu_json['episodeCount']
        self.type = kitsu_json['showType']
        self.genres = [genre["attributes"]["name"] for genre in anime["relationships"]["genres"]["data"]]

    def __repr__(self):
        return self.title


class AnimeClient(object):
    def __init__(self):
        self.url = 'https://kitsu.io/api/edge/anime'
        self.headers = {
            'Accept': 'application/vnd.api+json',
            'Content-Type': 'application/vnd.api+json',
            'Authorization': f'Bearer avK9bsEcYm4DuTGNPhis2o4rp32QzvcelbB29sJ-IPo'
        }

    def search(self, search_string):
        """
        When querying, this will return a list of anime objects that a relevant to the query
        """

        params = {
            'filter[text]': search_string,
            "include": "genres"
        }
        resp = requests.get(url, headers=self.headers, params=params)

        if resp.status_code != 200:
            raise ValueError(
                "Search request failed"
            )

        data = resp.json()['data']
        results = []
        if response.status_code == 200:
            for anime in data:
                
                results.append(Anime(anime))

        return results

    def retrieve_anime_by_id(self, anime_id):
        """
        Use to obtain an Anime object representing the anime by its id
        """
        url = f'https://kitsu.io/api/edge/anime/{anime_id}'
        params = {
            "include": "genres"
        }
        response = requests.get(url, headers=self.headers, params=params)

        if response.status_code == 200:
            data = response.json()['data']
            anime = Anime(data)
            return anime
        else:
            print('Failed to retrieve anime:', response.text)
            return None

    def search_by_genre(self, genres):
        # Convert the list of genre IDs to a comma-separated string
        genre_ids_str = ",".join(genres)

        # Make a GET request to the Kitsu API with the filter parameter set to the list of genre IDs
        response = requests.get("https://kitsu.io/api/edge/anime", params={"filter[genres]": genre_ids_str})

        if response.status_code != 200:
            raise ValueError("Search failed")

        # Parse the JSON response
        data = response.json()

        results = []
        # Print the titles of the anime that match the search criteria
        for anime in data["data"]:
            results.append(Anime(anime))

        return results


