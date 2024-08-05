# Speedrun API Wrapper
This Python package provides a convenient wrapper for the Speedrun API. It simplifies the process of interacting with the API by offering classes and methods for accessing user, game, run, and various other Speedrun-related data!

If I forgot some API tell me, i'll work on it.

Installation

you can install it using pip:

```bash
pip install speedruncomapi
```

# Usage
Importing the Package

```py

from speedruncomapi import User, Game, Run, Region, Platform, Developer, Engine, GameType, Genre, Guest, Leaderboard, Level, Notification, Profile, Publisher, Series, Variables, HiddenAPI
```

or 

```py
import speedruncomapi
```
which will lead to having to put speedruncomapi before everything like info = speedruncomapi.User.Info(name="username")

## User

Get User Information

```py

info = User.Info(name="username")  # or User.Info(ID="user_id")
print(info)

```
Get Personal Bests

```py

personal_bests = User.PersonalBest(name="username", limit=5)
print(personal_bests)
```


Get Game ID

```py

game_id = Game.get_game_id("game_id_or_name")
print(game_id)

```

Get Categories
```py

categories = Game.get_categories("game_id")
print(categories)
```

Get Category Details
```py

category_details = Game.get_category_details("category_id")
print(category_details)
```
Get Runs
```py

runs = Run.get_runs(user="username", max_data=10)
print(runs)

```
Get Run by ID
```py

run = Run.get_run_by_id("run_id")
print(run)
```

Create Run
```py

new_run = Run.create_run(
    auth_token="your_auth_token",
    category="category_id",
    level="level_id",
    date="YYYY-MM-DD",
    region="region_id",
    platform="platform_id"
)
print(new_run)

```
Update Run Status
```py

updated_run = Run.update_run_status(
    auth_token="your_auth_token",
    run_id="run_id",
    status="accepted",
    reason="Looks good!"
)
print(updated_run)
```

Delete Run
```py

deleted_run = Run.delete_run(auth_token="your_auth_token", run_id="run_id")
print(deleted_run)

```

## Region
Get All Regions
```py

regions = Region.get_all_regions()
print(regions)

```

Get Region by ID
```py

region = Region.get_region_by_id("region_id")
print(region)

```

## Platform
Get All Platforms
```py

platforms = Platform.get_all_platforms()
print(platforms)
```
Get Platform by ID
```py

platform = Platform.get_platform_by_id("platform_id")
print(platform)
```

## Developer
Get All Developers
```py

developers = Developer.get_all_developers()
print(developers)
```
Get Developer by ID
```py

developer = Developer.get_developer_by_id("developer_id")
print(developer)
```
## Engine
Get All Engines
```py

engines = Engine.get_all_engines()
print(engines)
```
Get Engine by ID
```py

engine = Engine.get_engine_by_id("engine_id")
print(engine)
```
## GameType
Get All Game Types
```py

game_types = GameType.get_all_gametypes()
print(game_types)
```

Get Game Type by ID
```py

game_type = GameType.get_gametype_by_id("gametype_id")
print(game_type)
```
## Genre
Get All Genres
```py

genres = Genre.get_all_genres()
print(genres)
```
Get Genre by ID
```py

genre = Genre.get_genre_by_id("genre_id")
print(genre)

```
## Guest
Get Guest by Name
```py

guest = Guest.get_guest_by_name("guest_name")
print(guest)
```
## Leaderboard
Get Full Game Leaderboard

```py

leaderboard = Leaderboard.get_full_game_leaderboard("game_id", "category_id")
print(leaderboard)

```

Get Individual Level Leaderboard
```py

level_leaderboard = Leaderboard.get_individual_level_leaderboard("game_id", "level_id", "category_id")
print(level_leaderboard)
```
## Level
Get Level by ID
```py

level = Level.get_level_by_id("level_id")
print(level)
```
Get Level Categories
```py

categories = Level.get_level_categories("level_id")
print(categories)
```
Get Level Variables
```py

variables = Level.get_level_variables("level_id")
print(variables)
Get Level Records
```py

records = Level.get_level_records("level_id")
print(records)
```
## Notification
Get Notifications
```py

notifications = Notification.get_notifications()
print(notifications)
```
## Profile
Get Profile
```py

profile = Profile.get_profile(api_key="your_api_key")
print(profile)
Get Profile Notifications
```py

profile_notifications = Profile.get_notifications(api_key="your_api_key")
print(profile_notifications)
```
##Publisher
Get Publishers
```py

publishers = Publisher.get_publishers()
print(publishers)
Get Publisher by ID
```py

publisher = Publisher.get_publisher("publisher_id")
print(publisher)
```
## Series
Get Series
```py

series = Series.get_series()
print(series)
```
Get Series by ID
```py

series_by_id = Series.get_series_by_id("series_id")
print(series_by_id)
```
Get Games in Series
```py

games_in_series = Series.get_games_in_series("series_id")
print(games_in_series)
```
## Variables
Get Variable by ID
```py

variable = Variables.get_variable("variable_id")
print(variable)

```
Get Variables for Game
```py

variables_for_game = Variables.get_variables_for_game("game_id")
print(variables_for_game)
```
Get Variables for Category
```py

variables_for_category = Variables.get_variables_for_category("category_id")
print(variables_for_category)
```
Get Variables for Level
```py

variables_for_level = Variables.get_variables_for_level("level_id")
print(variables_for_level)
```

## HiddenAPI
Send Message
```py

hidden_api = HiddenAPI(csrf_token="your_csrf_token", cookie_session="your_cookie_session")
response = hidden_api.send_message(recipient_ids=["recipient_id"], text="Hello!")
print(response)
```
Get Conversations
```py

conversations = hidden_api.get_conversations(limit=5)
print(conversations)
```
Get Conversation Messages
```py

messages = hidden_api.get_conversation_messages(conversation_id="conversation_id", mark_as_read=True)
print(messages)
```
Get Moderations Runs

```py
moderation_runs = api.get_moderation_runs(
    game_id='game_id_here',
    verified=0,  # No verified parameter: Everything, 0: unverified, 1: verified, 2: rejected
    page=1,
    limit=20
)
print(moderation_runs)

```
## Contributing
Contributions are welcome! Please fork the repository and submit a pull request with your changes. Ensure that your code adheres to the existing coding style and includes appropriate tests.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

