from unittest import TestCase

from app import app
from models import db, User, Post


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'


app.config['TESTING'] = True


app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()


class UserTestCase(TestCase):
    """Tests for Users"""

    def setUp(self):
        """Add user."""

        User.query.delete()

        user = User(first_name="TestUser_first_name",
                    last_name="TestUser_last_name", image_url="Testimage")
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id
        self.user = user

    def tearDown(self):
        """Clean up."""

        db.session.rollback()

    def test_list_users(self):
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('TestUser', html)

    def test_show_user(self):
        with app.test_client() as client:
            resp = client.get(f"/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>user.id</h1>', html)

    def test_add_user(self):
        with app.test_client() as client:
            d = {"first_name": "first_name", "last_name": "last_name",
                 "image_url": "image_url"}
            resp = client.post("/users/new", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("first_name", html)

    def test_edit_user(self):
        with app.test_client() as client:
            e = {"first_name": "first_name", "last_name": "last_name",
                 "image_url": "image_url"}
            resp = client.post('/users/<int:user_id>/edit',
                               data=e, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('first_name', html)


class PostTestCase(TestCase):
    """Tests for Users"""

    def setUp(self):
        """Add user."""

        Post.query.delete()

        post = Post(title="title",
                    content="content",
                    createdAt="createdAt")
        db.session.add(post)
        db.session.commit()

        self.post_id = post.id
        self.post = post

    def tearDown(self):
        """Clean up."""

        db.session.rollback()

    def test_show_posts(self):
        with app.test_client() as client:
            resp = client.get("/posts/<int:post_id>")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('title', html)
