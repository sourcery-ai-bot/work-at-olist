# Work at Olist [![Build Status](https://travis-ci.org/luizdepra/work-at-olist.svg?branch=master)](https://travis-ci.org/luizdepra/work-at-olist) [![Coverage Status](https://coveralls.io/repos/github/luizdepra/work-at-olist/badge.svg?branch=master)](https://coveralls.io/github/luizdepra/work-at-olist?branch=master) [![Code Health](https://landscape.io/github/luizdepra/work-at-olist/master/landscape.svg?style=flat)](https://landscape.io/github/luizdepra/work-at-olist/master)

This is my implementation of the test described [here](SPECIFICATION.md).

## Usage

To run this app you'll need:

* Python 3.5+ (It should work with older Python 3 version).
* PIP
* VirtualEnv
* PostgreSQL

There is two easy ways to run and test this app.

### Locally

1. Clone this repository.
2. Create a virtualenv that uses `python3.5` binary. e.g. `virtualenv -p /usr/bin/python3.5 venv`
3. Install requirements: `pip install -r requirements-local.txt`
4. Create a database for the app.
5. Create a `.env` file. Use `local.env` as a example.
6. Export `.env`: `export $(cat .env | xargs)`
7. Run: `python work-at-olist/manage.py runserver`

### Heroku

1. Clone this repository.
2. Install [`heroku-cli`](https://devcenter.heroku.com/articles/heroku-cli).
3. Create the heroku app and deploy it.

## Testing

To test, just run `manage.py test`. e.g.

```
python work-at-olist/manage.py channels
```

## Importing Data

To import a CSV file containing categories, run `manage.py importcategories channel csv` where `channel` is the name of the target channel to import and `csv` is the path to the CSV file. e.g.

```
python work-at-olist/manage.py importcategories Amazon ~/amazon.csv
```

## Implementation Details

About the development environment, I'm developing this project using a PC, running Ubuntu GNOME 16.10. I have been writing these text and code almost entirely in VS Code, with minors editions in Vim. I choose it over PyCharm, Atom and others because I saw this project as a oportunity to test VS Code. I have no regrests so far. Also, there are some tools I'm using to help linting and formating the code: [pylint](https://www.pylint.org/) and [yapf](https://github.com/google/yapf).

To develop this app I added some extra dependencies:

* *[django-mptt](https://github.com/django-mptt/django-mptt):* implementation of Modified Preorder Tree Traversal models.
* *[drf-nested-routers](https://github.com/alanjds/drf-nested-routers):* routers and fields to create nested resources in the Django REST Framework.
* *[djangorestframework-recursive](https://github.com/heywbj/django-rest-framework-recursive):* recursive Serializers for Django REST Framework.
* *[django-rest-swagger](https://github.com/marcgibbons/django-rest-swagger):* Swagger documentation generator for Django REST Framework.
* *[whitenoise](https://github.com/evansd/whitenoise):* static file serving for WSGI applications.

I used *django-mptt* to solve the problem of storing hierarchical data on a Relational Database. I came across some other options, but I choose MPTT because of its good query performance. However, it has a drawback, the insertion cost. Anyhow, this isn't a big problem in this case, categories don't change all the time. Also, I could have used PostgreSQL's *arrays* or *ltree*, but this would tie the app to PostgreSQL. And, the *drf-nested-routers* boosts DRF routing allowing nested routes, so `/api/v1/channels/{ref}/categories/{ref}/` turned possible. No need to comment about the other ones, they're are very straightforward.

About the app tools, the `importcategories` command is silent, following the Unix philosophy: *No news is good news*. And, when developing the API, I tried to follow best practices and the idea of simplicity.

## API Doc

This app provides a public API with `channels` and `categories` endpoints. The API is read-only, i.e. it provides only list and retrieve features.
You can check all endpoints and test them accessing `/api-docs/` when running the app.

### Channels endpoints

#### List all channels

```
GET /api/v1/channels/
```

##### Filters

* *limit:* maximum number of items to retrieve. Optional.
* *offset:*	number of items to skip. Optional.
* *search:*	term to search in `name` and `reference` fields. Optional.
* *ordering:* field that is used to order the items. Optional. Default: `reference`.

##### Response

```json
{
  "count": ITEMS_COUNT,
  "next": "NEXT_PAGE_URL",
  "previous": "PREVIOUS_PAGE_URL",
  "results": [
    {
      "url": "CHANNEL_URL+REFERENCE",
      "name": "NAME"
    },
    ...
  ]
}
```

#### Retrieve a channel

```
GET /api/v1/channels/{reference}/
```

##### Parameters

* *reference:* channel's reference.

##### Response

```json
{
  "url": "CHANNEL_URL+REFERENCE",
  "name": "NAME"
}
```

#### List all channel's categories

```
GET /api/v1/channels/{ch_reference}/categories/
```

##### Parameters

* *ch_reference:* channel's reference.

##### Filters

* *limit:* maximum number of items to retrieve. Optional.
* *offset:*	number of items to skip. Optional.
* *search:*	term to search in `name` and `reference` fields. Optional.
* *ordering:* field used to order the items. Optional. Default: `reference`.

##### Response

```json
{
  "count": ITEMS_COUNT,
  "next": "NEXT_PAGE_URL",
  "previous": "PREVIOUS_PAGE_URL",
  "results": [
    {
      "url": "CATEGORY_URL+REFERENCE",
      "name": "NAME",
      "channel": "CHANNEL_URL+REFERENCE",
      "parent": "CATEGORY_URL+REFERENCE",
      "children": [
        "CATEGORY_URL+REFERENCE",
        ...
      ]
    },
    ...
  ]
}
```

#### Retrieve a channel's category

```
GET /api/v1/channels/{ch_reference}/categories/{reference}/
```

##### Parameters

* *ch_reference:* channel's reference.
* *reference:* category's reference.

##### Response

```json
{
  "url": "CATEGORY_URL+REFERENCE",
  "name": "NAME",
  "channel": "CHANNEL_URL+REFERENCE",
  "parent": "CATEGORY_URL+REFERENCE",
  "children": [
    "CATEGORY_URL+REFERENCE",
    ...
  ]
}
```

#### Retrieve a channel's category with ancestors and children

```
GET /api/v1/channels/{ch_reference}/categories/{reference}/relatives/
```

##### Parameters

* *ch_reference:* channel's reference.
* *reference:* category's reference.

##### Response

```json
{
  "url": "CATEGORY_URL+REFERENCE",
  "name": "NAME",
  "channel": "CHANNEL_URL+REFERENCE",
  "parent": {
    "url": "CATEGORY_URL+REFERENCE",
    "name": "NAME",
    "parent": {...}
  },
  "children": [
    {
      "url": "CATEGORY_URL+REFERENCE",
      "name": "NAME",
      "children": [...]
    },
    ...
  ]
}
```

### Categories endpoints

#### List all categories

```
GET /api/v1/categories/
```

##### Filters

* *limit:* maximum number of items to retrieve. Optional.
* *offset:*	number of items to skip. Optional.
* *search:*	term to search in `name` and `reference` fields. Optional.
* *ordering:* field used to order the items. Optional. Default: `reference`.

##### Response

```json
{
  "count": ITEMS_COUNT,
  "next": "NEXT_PAGE_URL",
  "previous": "PREVIOUS_PAGE_URL",
  "results": [
    {
      "url": "CATEGORY_URL+REFERENCE",
      "name": "NAME",
      "channel": "CHANNEL_URL+REFERENCE",
      "parent": "CATEGORY_URL+REFERENCE",
      "children": [
        "CATEGORY_URL+REFERENCE",
        ...
      ]
    },
    ...
  ]
}
```

#### Retrieve a category

```
GET /api/v1/categories/{reference}/
```

##### Parameters

* *reference:* category's reference.

##### Response

```json
{
  "url": "CATEGORY_URL+REFERENCE",
  "name": "NAME",
  "channel": "CHANNEL_URL+REFERENCE",
  "parent": "CATEGORY_URL+REFERENCE",
  "children": [
    "CATEGORY_URL+REFERENCE",
    ...
  ]
}
```

#### Retrieve a category with ancestors and children

```
GET /api/v1/categories/{reference}/relatives/
```

##### Parameters

* *reference:* category's reference.

##### Response

```json
{
  "url": "CATEGORY_URL+REFERENCE",
  "name": "NAME",
  "channel": "CHANNEL_URL+REFERENCE",
  "parent": {
    "url": "CATEGORY_URL+REFERENCE",
    "name": "NAME",
    "parent": {...}
  },
  "children": [
    {
      "url": "CATEGORY_URL+REFERENCE",
      "name": "NAME",
      "children": [...]
    },
    ...
  ]
}
```

