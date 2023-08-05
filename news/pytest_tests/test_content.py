import pytest

from django.urls import reverse

from yanews.settings import NEWS_COUNT_ON_HOME_PAGE
from http import HTTPStatus


# @pytest.mark.django_db
# def test_news_count(news_list):
#     assert news_list is NEWS_COUNT_ON_HOME_PAGE

# @pytest.mark.skip
@pytest.mark.django_db
def test_count(client, news_list):
    url = reverse('news:home')
    response = client.get(url)
    object_list = response.context['object_list']
    assert "news_list" in response.context 
    news_count = len(object_list)
    assert news_count is NEWS_COUNT_ON_HOME_PAGE

# @pytest.mark.django_db
# def test_news_count(client):
#     url = reverse('news:home')
#     response = client.get(url)
#     object_list = response.context['object_list']
#     news_count = len(object_list)
#     assert news_count == NEWS_COUNT_ON_HOME_PAGE

@pytest.mark.django_db
def test_news_order(client):
    url = reverse('news:home')
    response = client.get(url)
    object_list = response.context['object_list']
    all_dates = [news.date for news in object_list]
    sorted_dates = sorted(all_dates, reverse=True)
    assert all_dates == sorted_dates

# @pytest.mark.django_db
# def test_comments_order(client, new):
#     url = reverse('news:detail', args=(new.id,))
#     response = client.get(url)
#     assert 'news' in response.context
#     news = response.context['news']
#     all_comments = new.comment_set.all()
#     assert all_comments[0].created != all_comments[1].created
    
# @pytest.mark.django_db 
# def test_comments_order(client, comments, new): 
#     url = reverse("news:detail", args=(new.id,)) 
#     response = client.get(url)
#     assert "news" in response.context
#     news = response.context['news']
#     all_comments = news.comment_set.all()
#     assert all_comments[0].created < all_comments[1].created



@pytest.mark.django_db 
def test_comments_order(client, comments, new): 
    url = reverse("news:detail", args=(new.id,)) 
    response = client.get(url)
    assert "news" in response.context
    news = response.context['news']
    all_comments = news.comment_set.all()
    sorted_comments = sorted(all_comments, key=lambda x: x.created, reverse=False)
    assert sorted_comments == comments

    

# @pytest.mark.django_db
# def test_comments_order(client, comment_objects):
#     news, comments = comment_objects
#     detail_url = reverse("news:detail", args=(news.id,))
#     response = client.get(detail_url)
#     assert "news" in response.context
#     news = response.context['news']
#     all_comments = news.comment_set.all()
#     all_dates = [all_comments.date for all_comments in all_comments]
#     sorted_comments = sorted(all_dates, reverse=False)
#     assert sorted_comments == comments

# @pytest.mark.django_db 
# def test_comments_order(client, comments, new): 
#     url = reverse("news:detail", args=(new.id,)) 
#     response = client.get(url)
#     assert "news" in response.context
#     news = response.context['news']
#     all_comments = news.comment_set.all()
#     assert all_comments[0].created < all_comments[1].created
#     all_dates = [comments.created for comments in comments]
#     sorted_dates = sorted(all_dates, reverse=True)
#     assert sorted_dates == sorted(comments, reverse=True)

@pytest.mark.django_db 
@pytest.mark.parametrize(
    'parametrized_client, form_in_page',
    (
        (pytest.lazy_fixture('client'), False),
        (pytest.lazy_fixture('author_client'), True)
    ),
)
def test_form_availability_for_different_users(
        new, parametrized_client, form_in_page
):
    url = reverse('news:detail', args=(new.id,))
    response = parametrized_client.get(url)
    assert ('form' in response.context) is form_in_page
