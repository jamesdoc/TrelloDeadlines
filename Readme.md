# Digital Media Deadlines

Powered by Trello cards, select the board(s) to look at and pulls out and presents the upcoming deadlines.

Presented as:

- Deadlines this week
- Next 30 days (not including this week's tasks)
- On the RADAR
- Past deadlines (last 5-10)

## Up and running

1. Copy `www/config_template.py` to `www/config.py`
2. Add to `www/config.py` the [key and secret](https://trello.com/app-key), [token](https://trello.com/1/authorize?key=|YOURKEY|&name=Deadlines&expiration=never&response_type=token) and [board ids](https://api.trello.com/1/members/me/boards?key=|YOURKEY|&token=|YOURTOKEN|) to look at.
2. `vagrant up && vagrant ssh`
3. `cd /vagrant/www`
4. `python server.py`