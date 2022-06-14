from unicodedata import name
from django.test import TestCase, Client
from django.urls import reverse

from .models import Author, Tred, Topic, User

# Create your tests here.
class TestProject(TestCase):
    
    def setUp(self) -> None:
        self.test_client = Client()
        self.unauthorized_test_client = Client()

        self.user1 = User.objects.create_user(username='testuser1', password='12345')
        self.user2 = User.objects.create_user(username='testuser2', password='12345')
        self.test_client.login(username="testuser1", password="12345")

        self.home_url = reverse('home')
        self.signin_url = reverse('signin')
        self.signout_url = reverse('signout')
        self.signup_url = reverse('signup')
        self.add_tred_url = reverse('addtred')
        self.add_topic_url = reverse('addtopic')
        self.search_url = reverse('search')
        self.update_url = reverse('update')

        # Models
        self.authors = []
        self.authors.append(Author.objects.create(name="Author1", bio="Bio1", user=self.user1))
        self.authors.append(Author.objects.create(name="Author2", bio="Bio1", user=self.user2))

        self.topics = []
        self.topics.append(Topic.objects.create(title="Title1", description="Description1", approved=True))
        self.topics.append(Topic.objects.create(title="Title2", description="Description2", approved=True))
        self.topics.append(Topic.objects.create(title="Title3", description="Description3", approved=True))

        self.treds = []
        self.treds.append(Tred.objects.create(title="Tred1", content="Content1", author=self.authors[0], topic=self.topics[0], approved=True))
        self.treds.append(Tred.objects.create(title="Tred2", content="Content2", author=self.authors[0], topic=self.topics[1], approved=True))
        self.treds.append(Tred.objects.create(title="Tred3", content="Content3", author=self.authors[0], topic=self.topics[2], approved=True))

        self.treds.append(Tred.objects.create(title="Tred1", content="Content1", author=self.authors[1], topic=self.topics[0], approved=True))
        self.treds.append(Tred.objects.create(title="Tred2", content="Content2", author=self.authors[1], topic=self.topics[1], approved=True))
        self.treds.append(Tred.objects.create(title="Tred3", content="Content3", author=self.authors[1], topic=self.topics[2], approved=True))

        self.profile_url = reverse('profile', kwargs={'slug': self.authors[0].slug })
        self.topic_url = reverse('topic', kwargs={'slug': self.topics[0].slug })
        self.treds_url = reverse('tred', kwargs={'slug': self.treds[0].slug})

    def test_home(self):
        respon_auth = self.test_client.get(self.home_url)
        respon_unauth = self.unauthorized_test_client.get(self.home_url)
    
    def test_signin(self):
        respon_auth = self.test_client.get(self.signin_url)
        respon_unauth = self.unauthorized_test_client.get(self.signin_url)
    
    def test_signup(self):
        respon_auth = self.test_client.get(self.signup_url)
        respon_unauth = self.unauthorized_test_client.get(self.signup_url)
    
    def test_signout(self):
        respon_auth = self.test_client.get(self.signout_url)
        respon_unauth = self.unauthorized_test_client.get(self.signout_url)
    
    def test_update(self):
        respon_auth = self.test_client.get(self.update_url)
        respon_unauth = self.unauthorized_test_client.get(self.update_url)

    def test_search(self):
        respon_auth = self.test_client.get(self.search_url)
        respon_unauth = self.unauthorized_test_client.get(self.search_url)

    def test_profile(self):
        respon_auth = self.test_client.get(self.profile_url)
        respon_unauth = self.unauthorized_test_client.get(self.profile_url)
    
    def test_topic(self):
        respon_auth = self.test_client.get(self.topic_url)
        respon_unauth = self.unauthorized_test_client.get(self.topic_url)
    
    def test_tred(self):
        respon_auth = self.test_client.get(self.treds_url)
        respon_unauth = self.unauthorized_test_client.get(self.treds_url)

    def test_add_tred(self):
        respon_auth = self.test_client.get(self.add_tred_url)
        respon_add = self.test_client.post(self.add_tred_url)
        respon_unath = self.unauthorized_test_client.get(self.add_tred_url)
    
    def test_add_topic(self):
        respon_auth = self.test_client.get(self.add_topic_url)
        respon_add = self.test_client.post(self.add_topic_url)
        respon_unauth = self.unauthorized_test_client.get(self.add_topic_url)
    