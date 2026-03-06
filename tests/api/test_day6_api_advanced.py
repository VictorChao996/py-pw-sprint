import pytest

from utils.schemas import Post, Comment
from utils.api_client import APIClient


class TestGetRequests:
    
    def test_get_all_posts(self, json_place_holder_api_client: APIClient):
        res = json_place_holder_api_client.get('/posts')
        assert res.status_code == 200
        posts = res.json()
        assert isinstance(posts, list)
        assert len(posts) > 0

    @pytest.mark.parametrize("i", [1,2,3])
    def test_single_post(self, json_place_holder_api_client: APIClient, i):
        res = json_place_holder_api_client.get(f"/posts/{i}")
        assert res.status_code == 200
        post = Post.model_validate(res.json())

        assert post.id == i

    @pytest.mark.parametrize("i", [101,200,300])
    def test_get_post_not_found(self, json_place_holder_api_client: APIClient, i):
        res = json_place_holder_api_client.get(f"/posts/{i}")
        assert res.status_code == 404


    @pytest.mark.parametrize("i", [1,2,3])
    def test_get_all_comments(self, json_place_holder_api_client: APIClient, i):
        res = json_place_holder_api_client.get(f"/posts/{i}/comments")
        assert res.status_code == 200
        comments = res.json()
        assert isinstance(comments, list)
        assert len(comments) > 0

        for comment in comments:
            comment = Comment.model_validate(comment)
            assert comment.postId == i

    



class TestPostRequests:

    def test_create_post(self, json_place_holder_api_client: APIClient):
        requestBody = {
            'title': "newPost",
            'body': "new Post body",
            'userId': 10
        }
        res = json_place_holder_api_client.post("/posts", json=requestBody)
        assert res.status_code == 201
        newPost = res.json()
        assert requestBody.keys() <= newPost.keys()

    # 模擬外部測試匯入測試資料
    CREATE_POST_TEST_DATA = [
        {"title": "Post A", "body": "Body A", "userId": 1, "expected_status": 201},
        {"title": "Post B", "body": "Body B", "userId": 2, "expected_status": 201},
        {"title": "", "body": "Body C", "userId": 1, "expected_status": 201},
    ]

    @pytest.mark.parametrize("test_data", CREATE_POST_TEST_DATA, ids=["valid_post_A", "valid_post_B", "empty_title"])
    def test_create_post_data_driven(self, json_place_holder_api_client: APIClient, test_data):
        requestBody = {
            'title': test_data['title'],
            'body': test_data['body'],
            'userId': test_data['userId']
        }
        
        res = json_place_holder_api_client.post('/posts', json=requestBody)
        assert res.status_code == test_data['expected_status']
        newPost = res.json()
        assert requestBody.keys() <= newPost.keys()

class TestPutRequests:

    @pytest.mark.parametrize("i", [1,2,3])
    def test_update_post(self, json_place_holder_api_client: APIClient, i):
        requestBody = {
            'title': 'updatePost',
            'body': 'update a post',
            'userId': 2
        }
        res = json_place_holder_api_client.put(f"/posts/{i}", json=requestBody)
        assert res.status_code == 200
        updatePost = Post.model_validate(res.json())
        assert updatePost.id == i
        for k, v in requestBody.items():
            assert getattr(updatePost, k) == v
        # logging.info(res.json())

class TestDeleteRequest:
    
    def test_delete_post(self, json_place_holder_api_client: APIClient):
        res = json_place_holder_api_client.delete(f"/posts/1")
        assert res.status_code == 200
