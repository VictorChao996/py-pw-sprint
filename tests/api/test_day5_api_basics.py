import pytest
import requests
import httpx
import logging

from utils.schemas import Post, Comment

BASE_URL = "https://jsonplaceholder.typicode.com"

class TestGetRequests:
    
    def test_get_all_posts(self):
        res = requests.get(f"{BASE_URL}/posts")
        assert res.status_code == 200
        posts = res.json()
        assert isinstance(posts, list)
        assert len(posts) > 0

    @pytest.mark.parametrize("i", [1,2,3])
    def test_single_post(self, i):
        res = requests.get(f"{BASE_URL}/posts/{i}")
        assert res.status_code == 200
        post = Post.model_validate(res.json())

        assert post.id == i

    @pytest.mark.parametrize("i", [101,200,300])
    def test_get_post_not_found(self, i):
        res = requests.get(f"{BASE_URL}/posts/{i}")
        assert res.status_code == 404


    @pytest.mark.parametrize("i", [1,2,3])
    def test_get_all_comments(self, i):
        res = requests.get(f"{BASE_URL}/posts/{i}/comments")
        assert res.status_code == 200
        comments = res.json()
        assert isinstance(comments, list)
        assert len(comments) > 0

        for comment in comments:
            comment = Comment.model_validate(comment)
            assert comment.postId == i

    



class TestPostRequests:

    def test_create_post(self):
        requestBody = {
            'title': "newPost",
            'body': "new Post body",
            'userId': 10
        }

        res = requests.post(f"{BASE_URL}/posts", json=requestBody)
        assert res.status_code == 201
        newPost = res.json()
        assert requestBody.keys() <= newPost.keys()

class TestPutRequests:

    @pytest.mark.parametrize("i", [1,2,3])
    def test_update_post(self, i):
        requestBody = {
            'title': 'updatePost',
            'body': 'update a post',
            'userId': 2
        }

        res = httpx.put(f"{BASE_URL}/posts/{i}", json=requestBody)
        assert res.status_code == 200
        updatePost = Post.model_validate(res.json())
        assert updatePost.id == i
        for k, v in requestBody.items():
            assert getattr(updatePost, k) == v
        # logging.info(res.json())

class TestDeleteRequest:
    
    def test_delete_post(self):
        res = httpx.delete(f"{BASE_URL}/posts/1")
        assert res.status_code == 200
