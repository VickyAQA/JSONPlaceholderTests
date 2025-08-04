from enum import Enum


class Endpoints(Enum):
    POSTS_ENDPOINT = "/posts"
    COMMENTS_ENDPOINT = "/comments"
    USERS_ENDPOINT = "/users"
    POST_COMMENTS_ENDPOINT = "/posts/{post_id}/comments"