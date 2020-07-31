from django.test import TestCase
from django.urls import reverse, resolve

from .views import home, board_topics
from .models import Board

# Create your tests here.

# メインページから詳細ページへのリンクのテスト
class HomeTests(TestCase):
  def setUp(self):
    self.board = Board.objects.create(name="django", description="django board.")
    url = reverse('home')
    self.response = self.client.get(url)
  
  def test_home_view_status_code(self):
    self.assertEqual(self.response.status_code, 200)
  
  def test_home_url_resolvers_home_view(self):
    view = resolve('/')
    self.assertEqual(view.func, home)

  def test_home_view_contains_link_to_topics_page(self):
    board_topics_url = reverse('board_topics', kwargs={'pk': self.board.pk})
    self.assertContains(self.response, 'href="{0}"'.format(board_topics_url))

# 詳細ページからメインページへのリンクのテスト
class BoardTopicsTests(TestCase):
  # 仮のインスタンスを生成するメソッド
  def setUp(self):
    Board.objects.create(name="django", description="django board.")

  # board_topicsにアクセスしたとき、ちゃんとページが表示されるかのテスト
  def test_board_topics_view_success_status_code(self):
    url = reverse('board_topics', kwargs = {'pk':1})
    response = self.client.get(url)
    self.assertEqual(response.status_code, 200)

  # 存在しないurlにアクセスしたときに、エラーメッセージが出るかのテスト
  def test_board_topics_view_not_found_status_code(self):
    url = reverse('board_topics', kwargs = {'pk':99})
    response = self.client.get(url)
    self.assertEqual(response.status_code, 404)
    # views.pyのほうで例外を考慮したコードを書いていないのでdoesnotexistエラーが出た？

  # urlから紐づけたビューが呼び出されるかのテスト
  def test_board_topics_url_resolvers_board_topics_view(self):
    view = resolve('/boards/1')
    self.assertEqual(view.func, board_topics)

  def test_board_topics_view_contains_link_back_to_homepage(self):
    board_topics_url = reverse('board_topics', kwargs={'pk':1})
    response = self.client.get(board_topics_url)
    homepage_url = reverse('home')
    self.assertContains(response, 'href="{0}"'.format(homepage_url))

class NewTopicTests(TestCase):
  def setUp(self):
      Board.objects.create(name='Django', description='Django board.')

  def test_new_topic_view_success_status_code(self):
      url = reverse('new_topic', kwargs={'pk': 1})
      response = self.client.get(url)
      self.assertEquals(response.status_code, 200)

  def test_new_topic_view_not_found_status_code(self):
      url = reverse('new_topic', kwargs={'pk': 99})
      response = self.client.get(url)
      self.assertEquals(response.status_code, 404)

  def test_new_topic_url_resolves_new_topic_view(self):
      view = resolve('/boards/1/new/')
      self.assertEquals(view.func, new_topic)

  def test_new_topic_view_contains_link_back_to_board_topics_view(self):
      new_topic_url = reverse('new_topic', kwargs={'pk': 1})
      board_topics_url = reverse('board_topics', kwargs={'pk': 1})
      response = self.client.get(new_topic_url)
      self.assertContains(response, 'href="{0}"'.format(board_topics_url))

