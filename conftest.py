import pytest
from datetime import datetime
from news.models import News, Comment


@pytest.fixture
def author(django_user_model):  
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def author_client(author, client):
    client.force_login(author)
    return client


@pytest.fixture
def new():
    new = News.objects.create(
        title='Заголовок',
        text='Текст заметки',
    )
    return new

@pytest.fixture
def comment(new, author):
    comment = Comment.objects.create(
        news=new,
        author=author,
        text='Текст заметки',
    )
    return comment

@pytest.fixture
def id_for_args(new):  
    return new.id,

@pytest.fixture
def id_comment_for_args(comment):  
    return comment.id, 

@pytest.fixture
def form_data():
    return {
        'news': 'Новость',
        'text': 'Новый текст'
    }
