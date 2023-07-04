# BlogAPI

It's a RESTful blogging API built on top of Python and FastAPI. It provides a function for creating and using users and blog posts, and adds and retrieves likes and dislikes to posts.

The API includes a user authorization feature and includes separate endpoints that require user credentials to be validated. All data, including information about users, posts, likes and dislikes, blocks in the SQL database.

I left a .env file with the base configuration and jwt so that you can easily raise the project in docker and test the API at localhost:8000/docs

---
## How to run (Useage with docker)

```
docker compose up -d
```
