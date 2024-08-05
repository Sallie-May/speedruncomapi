import requests

class User:
    @staticmethod
    def Info(name=None, ID=None, Get=None, SubGet=None):
        if name is None and ID is None:
            return "You haven't put a username or ID."
        if ID is not None and name is not None:
            return "It is useless to put ID and Username; use one of the two."
        
        if ID is not None:
            url = f"https://www.speedrun.com/api/v1/users/{ID}"
        elif name is not None:
            url = f"https://www.speedrun.com/api/v1/users/{name}"
        
        data = requests.get(url).json()
        
        try:
            if data["status"] == 404:
                return "404, Maybe wrong username?"
        except KeyError:
            pass
        
        if Get is not None:
            if SubGet is not None:
                return data["data"][Get].get(SubGet, None)
            return data["data"].get(Get, None)
        return data

    @staticmethod
    def PersonalBest(name=None, ID=None, min_place=None, limit=None, game_id=None, offset=0, max_data=20):
        if max_data > 200:
            return "Max value must be 200 or below."
        
        if name is None and ID is None:
            return "You haven't put a username or ID. Put it using name"
        if ID is not None and name is not None:
            return "It's useless to put ID and Username, use one of them."
        
        if ID is not None:
            url = f"https://www.speedrun.com/api/v1/users/{ID}/personal-bests"
        elif name is not None:
            url = f"https://www.speedrun.com/api/v1/users/{name}/personal-bests"
        
        results = []
        params = {
            'offset': offset,
            'max': max_data 
        }
        
        while url:
            response = requests.get(url, params=params)
            data = response.json()
            
            try:
                if data["status"] == 404:
                    return "404, Maybe wrong username?"
            except KeyError:
                pass

            results.extend(data.get("data", []))
            
            pagination = data.get("pagination", {})
            url = None 
            if pagination.get("links"):
                for link in pagination["links"]:
                    if link["rel"] == "next":
                        url = link["uri"]
                        break
            params['offset'] = pagination.get('offset', offset) + params['max']

        if game_id is not None:
            check_validity = Game.get_game_id(game_id)
            if not check_validity:
                return "Invalid game ID or name."
            results = [run for run in results if run.get("run", {}).get("game") == check_validity]
        
        if min_place is not None:
            results = [run for run in results if run.get("place", float('inf')) <= min_place]
        
        if limit is not None:
            results = results[:limit]
        
        return results

class Game:
    @staticmethod
    def get_game_id(game_id):
        url = f"https://www.speedrun.com/api/v1/games/{game_id}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data["data"]["id"]
        else:
            return False

    @staticmethod
    def get_categories(game_id):
        if not game_id:
            return "You haven't provided a game ID."

        game_id = Game.get_game_id(game_id)
        if not game_id:
            return "Invalid game ID."
        
        url = f"https://www.speedrun.com/api/v1/games/{game_id}/categories"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()["data"]
        else:
            return f"Error {response.status_code}: Unable to retrieve categories. Err: {response.json()}."

    @staticmethod
    def get_category_details(category_id):
        url = f"https://www.speedrun.com/api/v1/categories/{category_id}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()["data"]
        else:
            return f"Error {response.status_code}: Unable to retrieve category details. Err: {response.json()}."

    @staticmethod
    def get_category_variables(category_id):
        url = f"https://www.speedrun.com/api/v1/categories/{category_id}/variables"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()["data"]
        else:
            return f"Error {response.status_code}: Unable to retrieve category variables. Err: {response.json()}."

    @staticmethod
    def get_category_records(category_id, top=3, skip_empty=False):
        url = f"https://www.speedrun.com/api/v1/categories/{category_id}/records"
        params = {
            "top": top,
            "skip-empty": str(skip_empty).lower()
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()["data"]
        else:
            return f"Error {response.status_code}: Unable to retrieve category records. Err: {response.json()}."

class Run:
    @staticmethod
    def get_runs(user=None, guest=None, examiner=None, game=None, level=None, category=None, platform=None, region=None, emulated=None, status=None, orderby='game', direction='asc', offset=0, max_data=20, limit=None):
        if max_data > 200:
            return "Error: max value must be 200 or below."
        
        
        url = "https://www.speedrun.com/api/v1/runs"
        params = {
            'user': user,
            'guest': guest,
            'examiner': examiner,
            'game': game,
            'level': level,
            'category': category,
            'platform': platform,
            'region': region,
            'emulated': emulated,
            'status': status,
            'orderby': orderby,
            'direction': direction,
            'offset': offset,
            'max': max_data  
        }
        
        results = []
        
        while url:
            response = requests.get(url, params={k: v for k, v in params.items() if v is not None})
            data = response.json()
            
            results.extend(data.get("data", []))
            
            pagination = data.get("pagination", {})
            url = None 
            if pagination.get("links"):
                for link in pagination["links"]:
                    if link["rel"] == "next":
                        url = link["uri"]
                        break
            params['offset'] = pagination.get('offset', offset) + params['max']

        if limit is not None:
            results = results[:limit]

        return results

    @staticmethod
    def get_run_by_id(run_id):
        url = f"https://www.speedrun.com/api/v1/runs/{run_id}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()["data"]
        else:
            return f"Error {response.status_code}: Unable to retrieve run details. Err: {response.json()}."
    
    @staticmethod
    def create_run(auth_token, category, level=None, date=None, region=None, platform=None, verified=False, times=None, players=None, emulated=False, video=None, comment=None, splitsio=None, variables=None):
        url = "https://www.speedrun.com/api/v1/runs"
        headers = {
            'Authorization': f'Bearer {auth_token}',
            'Content-Type': 'application/json'
        }
        payload = {
            "run": {
                "category": category,
                "level": level,
                "date": date,
                "region": region,
                "platform": platform,
                "verified": verified,
                "times": times,
                "players": players,
                "emulated": emulated,
                "video": video,
                "comment": comment,
                "splitsio": splitsio,
                "variables": variables
            }
        }
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 201:
            return response.json()["data"]
        else:
            return response.json()
        
    @staticmethod
    def update_run_status(auth_token, run_id, status, reason=None):
        url = f"https://www.speedrun.com/api/v1/runs/{run_id}/status"
        headers = {
            'Authorization': f'Bearer {auth_token}',
            'Content-Type': 'application/json'
        }
        payload = {
            "status": {
                "status": status,
                "reason": reason
            } if status == "rejected" else {"status": status}
        }
        response = requests.put(url, json=payload, headers=headers)
        if response.status_code == 200:
            return response.json()["data"]
        else:
            return response.json()
    
    @staticmethod
    def update_run_players(auth_token, run_id, players):
        url = f"https://www.speedrun.com/api/v1/runs/{run_id}/players"
        headers = {
            'Authorization': f'Bearer {auth_token}',
            'Content-Type': 'application/json'
        }
        payload = {
            "players": players
        }
        response = requests.put(url, json=payload, headers=headers)
        if response.status_code == 200:
            return response.json()["data"]
        else:
            return response.json()
        
    @staticmethod
    def delete_run(auth_token, run_id):
        url = f"https://www.speedrun.com/api/v1/runs/{run_id}"
        headers = {
            'Authorization': f'Bearer {auth_token}'
        }
        response = requests.delete(url, headers=headers)
        if response.status_code == 200:
            return response.json()["data"]
        else:
            return response.json()

class Region:
    
    @staticmethod
    def get_all_regions(orderby='name', direction='asc'):
        url = "https://www.speedrun.com/api/v1/regions"
        params = {
            'orderby': orderby,
            'direction': direction
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()["data"]
        else:
            return f"Error {response.status_code}: Unable to retrieve regions. Err: {response.json()}."
    
    @staticmethod
    def get_region_by_id(region_id):
        url = f"https://www.speedrun.com/api/v1/regions/{region_id}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()["data"]
        else:
            return f"Error {response.status_code}: Unable to retrieve region. Err: {response.json()}."


class Platform:
    
    @staticmethod
    def get_all_platforms(orderby='name', direction='asc'):
        url = "https://www.speedrun.com/api/v1/platforms"
        params = {
            'orderby': orderby,
            'direction': direction
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()["data"]
        else:
            return f"Error {response.status_code}: Unable to retrieve platforms."
    @staticmethod
    def get_platform_by_id(platform_id):
        url = f"https://www.speedrun.com/api/v1/platforms/{platform_id}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()["data"]
        else:
            return f"Error {response.status_code}: Unable to retrieve platform."
class Developer:
    @staticmethod
    def get_all_developers(orderby='name', direction='asc'):
        url = "https://www.speedrun.com/api/v1/developers"
        params = {
            'orderby': orderby,
            'direction': direction
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()["data"]
        else:
            return f"Error {response.status_code}: Unable to retrieve developers. Err: {response.json()}."

    @staticmethod
    def get_developer_by_id(developer_id):
        url = f"https://www.speedrun.com/api/v1/developers/{developer_id}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()["data"]
        else:
            return f"Error {response.status_code}: Unable to retrieve developer. Err: {response.json()}."
        
class Engine:
    @staticmethod
    def get_all_engines(orderby='name', direction='asc'):
        url = "https://www.speedrun.com/api/v1/engines"
        params = {
            'orderby': orderby,
            'direction': direction
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()["data"]
        else:
            return f"Error {response.status_code}: Unable to retrieve engines. Err: {response.json()}."

    @staticmethod
    def get_engine_by_id(engine_id):
        url = f"https://www.speedrun.com/api/v1/engines/{engine_id}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()["data"]
        else:
            return f"Error {response.status_code}: Unable to retrieve engine. Err: {response.json()}."
class GameType:
    @staticmethod
    def get_all_gametypes(orderby='name', direction='asc'):
        url = "https://www.speedrun.com/api/v1/gametypes"
        params = {
            'orderby': orderby,
            'direction': direction
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()["data"]
        else:
            return f"Error {response.status_code}: Unable to retrieve game types. Err: {response.json()}."

    @staticmethod
    def get_gametype_by_id(gametype_id):
        url = f"https://www.speedrun.com/api/v1/gametypes/{gametype_id}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()["data"]
        else:
            return f"Error {response.status_code}: Unable to retrieve game type. Err: {response.json()}."
class Genre:
    @staticmethod
    def get_all_genres(orderby='name', direction='asc'):
        url = "https://www.speedrun.com/api/v1/genres"
        params = {
            'orderby': orderby,
            'direction': direction
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()["data"]
        else:
            return f"Error {response.status_code}: Unable to retrieve genres. Err: {response.json()}."

    @staticmethod
    def get_genre_by_id(genre_id):
        url = f"https://www.speedrun.com/api/v1/genres/{genre_id}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()["data"]
        else:
            return f"Error {response.status_code}: Unable to retrieve genre. Err: {response.json()}."

class Guest:
    @staticmethod
    def get_guest_by_name(name):
        url = f"https://www.speedrun.com/api/v1/guests/{name}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()["data"]
        else:
            return f"Error {response.status_code}: Unable to retrieve guest. Err: {response.json()}."
class Leaderboard:
    @staticmethod
    def get_full_game_leaderboard(game_id, category_id, **filters):
        url = f"https://www.speedrun.com/api/v1/leaderboards/{game_id}/category/{category_id}"
        response = requests.get(url, params=filters)
        if response.status_code == 200:
            return response.json()["data"]
        else:
            return f"Error {response.status_code}: Unable to retrieve leaderboard. Err: {response.json()}."

    @staticmethod
    def get_individual_level_leaderboard(game_id, level_id, category_id, **filters):
        url = f"https://www.speedrun.com/api/v1/leaderboards/{game_id}/level/{level_id}/{category_id}"
        response = requests.get(url, params=filters)
        if response.status_code == 200:
            return response.json()["data"]
        else:
            return f"Error {response.status_code}: Unable to retrieve leaderboard. Err: {response.json()}."
class Level:
    @staticmethod
    def get_level_by_id(level_id):
        url = f"https://www.speedrun.com/api/v1/levels/{level_id}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()["data"]
        else:
            return f"Error {response.status_code}: Unable to retrieve level. Err: {response.json()}."

    @staticmethod
    def get_level_categories(level_id, miscellaneous=None, orderby='pos', direction='asc'):
        url = f"https://www.speedrun.com/api/v1/levels/{level_id}/categories"
        params = {
            'miscellaneous': miscellaneous,
            'orderby': orderby,
            'direction': direction
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()["data"]
        else:
            return f"Error {response.status_code}: Unable to retrieve categories. Err: {response.json()}."

    @staticmethod
    def get_level_variables(level_id, orderby='pos', direction='asc'):
        url = f"https://www.speedrun.com/api/v1/levels/{level_id}/variables"
        params = {
            'orderby': orderby,
            'direction': direction
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()["data"]
        else:
            return f"Error {response.status_code}: Unable to retrieve variables. Err: {response.json()}."

    @staticmethod
    def get_level_records(level_id, top=3, skip_empty=False):
        url = f"https://www.speedrun.com/api/v1/levels/{level_id}/records"
        params = {
            'top': top,
            'skip-empty': skip_empty
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()["data"]
        else:
            return f"Error {response.status_code}: Unable to retrieve records. Err: {response.json()}."
class Notification:
    BASE_URL = "https://www.speedrun.com/api/v1/notifications"

    @staticmethod
    def get_notifications(orderby='created', direction='desc'):
        params = {
            'orderby': orderby,
            'direction': direction
        }
        response = requests.get(Notification.BASE_URL, params=params)
        if response.status_code == 200:
            return response.json()["data"]
        else:
            return f"Error {response.status_code}: Unable to retrieve notifications. Err: {response.json()}."

class Profile:
    BASE_URL = "https://www.speedrun.com/api/v1/profile"

    @staticmethod
    def get_profile(api_key):

        headers = {
            'Authorization': f'Bearer {api_key}'
        }
        response = requests.get(Profile.BASE_URL, headers=headers)
        
        if response.status_code == 200:
            return response.json()["data"]
        else:
            return f"Error {response.status_code}: Unable to retrieve profile. Err: {response.json()}."

    @staticmethod
    def get_notifications(api_key, orderby='created', direction='desc'):

        headers = {
            'Authorization': f'Bearer {api_key}'
        }
        params = {
            'orderby': orderby,
            'direction': direction
        }
        response = requests.get(Notification.BASE_URL, headers=headers, params=params)
        
        if response.status_code == 200:
            return response.json()["data"]
        else:
            return f"Error {response.status_code}: Unable to retrieve notifications. Err: {response.json()}."

class Publisher:
    BASE_URL = "https://www.speedrun.com/api/v1/publishers"

    @staticmethod
    def get_publishers(orderby='name', direction='asc'):
        params = {
            'orderby': orderby,
            'direction': direction
        }
        response = requests.get(Publisher.BASE_URL, params=params)
        
        if response.status_code == 200:
            return response.json()["data"]
        else:
            return f"Error {response.status_code}: Unable to retrieve publishers. Err: {response.json()}."

    @staticmethod
    def get_publisher(publisher_id):

        url = f"{Publisher.BASE_URL}/{publisher_id}"
        response = requests.get(url)
        
        if response.status_code == 200:
            return response.json()["data"]
        else:
            return f"Error {response.status_code}: Unable to retrieve publisher. Err: {response.json()}."

class Series:
    BASE_URL = "https://www.speedrun.com/api/v1/series"

    @staticmethod
    def get_series(orderby='name.int', direction='asc', name=None, abbreviation=None, moderator=None):
        params = {
            'orderby': orderby,
            'direction': direction,
            'name': name,
            'abbreviation': abbreviation,
            'moderator': moderator
        }
        response = requests.get(Series.BASE_URL, params=params)
        
        if response.status_code == 200:
            return response.json()["data"]
        else:
            return f"Error {response.status_code}: Unable to retrieve series. Err: {response.json()}."

    @staticmethod
    def get_series_by_id(series_id):
        url = f"{Series.BASE_URL}/{series_id}"
        response = requests.get(url)
        
        if response.status_code == 200:
            return response.json()["data"]
        else:
            return f"Error {response.status_code}: Unable to retrieve series. Err: {response.json()}."

    @staticmethod
    def get_games_in_series(series_id):
        url = f"{Series.BASE_URL}/{series_id}/games"
        response = requests.get(url)
        
        if response.status_code == 200:
            return response.json()["data"]
        else:
            return f"Error {response.status_code}: Unable to retrieve games in series. Err: {response.json()}."
class Variables:
    BASE_URL = "https://www.speedrun.com/api/v1/variables"

    @staticmethod
    def get_variable(variable_id):
        url = f"{Variables.BASE_URL}/{variable_id}"
        response = requests.get(url)
        
        if response.status_code == 200:
            return response.json()["data"]
        else:
            return f"Error {response.status_code}: Unable to retrieve variable. Err: {response.json()}."

    @staticmethod
    def get_variables_for_game(game_id):
        url = f"https://www.speedrun.com/api/v1/games/{game_id}/variables"
        response = requests.get(url)
        
        if response.status_code == 200:
            return response.json()["data"]
        else:
            return f"Error {response.status_code}: Unable to retrieve variables for game. Err: {response.json()}."

    @staticmethod
    def get_variables_for_category(category_id):
        url = f"https://www.speedrun.com/api/v1/categories/{category_id}/variables"
        response = requests.get(url)
        
        if response.status_code == 200:
            return response.json()["data"]
        else:
            return f"Error {response.status_code}: Unable to retrieve variables for category. Err: {response.json()}."

    @staticmethod
    def get_variables_for_level(level_id):
        url = f"https://www.speedrun.com/api/v1/levels/{level_id}/variables"
        response = requests.get(url)
        
        if response.status_code == 200:
            return response.json()["data"]
        else:
            return f"Error {response.status_code}: Unable to retrieve variables for level. Err: {response.json()}."

class HiddenAPI:
    BASE_URL = "https://www.speedrun.com/api/v2/PutConversation"
    BASE_MESSAGES_URL = "https://www.speedrun.com/api/v2/GetConversationMessages"
    BASE_CONVERSATIONS_URL = "https://www.speedrun.com/api/v2/GetConversations"
    BASE_URL_GET_MODERATION_RUNS = "https://www.speedrun.com/api/v2/GetModerationRuns"

    def __init__(self, csrf_token, cookie_session):

        self.csrf_token = csrf_token
        self.cookie_session = cookie_session


    def send_message(self, recipient_ids, text):

        headers = {
            'Content-Type': 'application/json',
            'Cookie': f'PHPSESSID={self.cookie_session}',
            'Accept': 'application/json'
        }

        data = {
            'csrfToken': self.csrf_token,
            'recipientIds': recipient_ids,
            'text': text
        }

        response = requests.post(self.BASE_URL, json=data, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            return {
                "error": response.status_code,
                "message": response.json()
            }

    def send_message(self, recipient_ids, text):

        headers = {
            'Content-Type': 'application/json',
            'Cookie': f'PHPSESSID={self.cookie_session}',
            'Accept': 'application/json'
        }

        data = {
            'csrfToken': self.csrf_token,
            'recipientIds': recipient_ids,
            'text': text
        }

        response = requests.post(self.BASE_CONVERSATION_URL, json=data, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            return {
                "error": response.status_code,
                "message": response.json()
            }

    def get_conversation_messages(self, conversation_id, mark_as_read=False):
        headers = {
            'Content-Type': 'application/json',
            'Cookie': f'PHPSESSID={self.cookie_session}',
            'Accept': 'application/json'
        }

        data = {
            'conversationId': conversation_id,
            'markAsRead': mark_as_read
        }

        response = requests.post(self.BASE_MESSAGES_URL, json=data, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            return {
                "error": response.status_code,
                "message": response.json()
            }
    def get_conversations(self, limit=5):

        headers = {
            'Content-Type': 'application/json',
            'Cookie': f'PHPSESSID={self.cookie_session}',
            'Accept': 'application/json'
        }

        data = {
            'limit': limit
        }

        response = requests.post(self.BASE_CONVERSATIONS_URL, json=data, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            return {
                "error": response.status_code,
                "message": response.json()
            }
    def get_moderation_runs(self, game_id, verified_state='all', verified_by_id=None, search='', page=1, limit=20):

        if verified_state not in ['all', 'unverified', 'verified', 'rejected']:
            return {"error": "Invalid verified_state. Choose from 'all', 'unverified', 'verified', 'rejected'."}

        verified_mapping = {
            'all': None,
            'unverified': 0,
            'verified': 1,
            'rejected': 2
        }

        headers = {
            'Content-Type': 'application/json',
            'Cookie': f'PHPSESSID={self.cookie_session}',
            'Accept': 'application/json'
        }

        data = {
            'gameId': game_id,
            'limit': limit,
            'page': page,
            'search': search,
            'verifiedById': verified_by_id
        }

        verified_value = verified_mapping[verified_state]
        if verified_value is not None:
            data['verified'] = verified_value

        response = requests.post(self.BASE_URL_GET_MODERATION_RUNS, json=data, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            return {
                "error": response.status_code,
                "message": response.json()
            }
