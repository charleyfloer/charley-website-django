import pytest
from django.utils import timezone
from tests.factories import ArticlesFactory

@pytest.mark.django_db
def test_new_article():
    article = ArticlesFactory.create()
    
    print(article.title) 

    assert article.title != ""
    assert isinstance(article.summary, str)
    assert article.date <= timezone.now()
    
@pytest.mark.django_db 
def test_article_factory_build():
    article = ArticlesFactory.build()
    
    assert article.title != ""
    assert isinstance(article.summary, str)
    assert article.date <= timezone.now()
    assert article.pk is None  


    