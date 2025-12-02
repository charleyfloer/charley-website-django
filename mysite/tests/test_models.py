import pytest
from django.utils import timezone
from main.models import Articles

@pytest.fixture
def article_factory():
    def create_article(title, summary, full_text, author, date=None):
        if date is None:
            date = timezone.now()
        return Articles.objects.create(
            title=title,
            summary=summary,
            full_text=full_text,
            author=author,
            date=date
        )
    return create_article

@pytest.mark.django_db
@pytest.mark.parametrize(
    "title, summary, full_text, author",
    [
        ("Article A", "Summary A", "Full text A", "Author A"),
        ("Article B", "Summary B", "Full text B", "Author B"),
    ]
)
def test_article_creation(article_factory, title, summary, full_text, author):
    article = article_factory(title=title, summary=summary, full_text=full_text, author=author)
    assert article.title == title
    assert article.summary == summary
    assert article.full_text == full_text
    assert article.date is not None







