# Django Channels Light Control

![Demo](docs/DjangoChannelsMeetup.gif)

Demo app using django channels to control(turn on and off) some lights 
using the WebSockets protocol.

This was created for Python St. Petersburg (https://www.meetup.com/Saint-Petersburg-Python-Meetup/).

## Demo

* **Main Interface:** https://django-channels-light.herokuapp.com
* **Control Interface(Admin):** https://django-channels-light.herokuapp.com/admin

**Credentials:**

* **Username:** admin
* **Password:** th3n0rthr3m3mb3rs


## Requirements

* Python 3.5+
* PostgreSQL
* Redis

## Running locally


```shell
$ pip install -r requirements.txt
$ ./manage.py runserver
```

Go to: http://localhost:8000

Create a few lights on the Django Admin(http://localhost:8000/admin)
and start controlling it.

That's all!

## License

MIT
