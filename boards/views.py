from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User

from .models import Board, Topic, Post
from .forms import NewTopicForm, PostForm

# Create your views here.
def home(request):
  boards = Board.objects.all()
  return render(request, 'home.html', {'boards' :boards})

def board_topics(request, pk):
  # try:
  #   board = Board.objects.get(pk=pk)
  # except Board.DoesNotExist:
  #   raise Http404
  board = get_object_or_404(Board, pk=pk)
  return render(request, 'topics.html', {'board': board})

def new_topic(request, pk):
  board = get_object_or_404(Board, pk=pk)
  user = User.objects.first()
  if request.method == 'POST':
    # 送信されたデータでインスタンスが生成される
    form = NewTopicForm(request.POST)
    if form.is_valid():
      topic = form.save(commit=False)
      topic.board = board
      topic.starter = user
      topic.save()
      post = Post.objects.create(
        message=form.cleaned_data.get('message'),
        topic=topic,
        created_by=user
      )
      return redirect('topic_posts',pk=pk, topic_pk=topic.pk)
  else:
    # 逆にGETメソッドでアクセスしたときは初期化されたフォームが表示される
    form = NewTopicForm()
  return render(request, 'new_topic.html', {'board':board, 'form':form})

def topic_posts(request, pk, topic_pk):
  topic = get_object_or_404(Topic, board_id = pk, pk = topic_pk)
  return render(request, 'topic_posts.html', {'topic':topic})

def reply_topic(request, pk, topic_pk):
  topic = get_object_or_404(Topic, board_id = pk, pk = topic_pk)
  if request.method == 'POST':
    form = PostForm(request.POST)
    if form.is_valid():
      post = form.save(commit = False)
      post.topic = topic
      post.created_by = request.user
      post.save()
      return redirect('topic_posts', pk=pk, topic_pk = topic_pk)
  else:
    form = PostForm()
  return render(request, 'reply_topic.html', {'topic':topic, 'form':form})
