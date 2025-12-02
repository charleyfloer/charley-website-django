import factory
from django.utils import timezone
from main.models import Articles
from faker import Faker

fake = Faker()

class ArticlesFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Articles

    title = factory.LazyFunction(fake.catch_phrase)
    full_text = factory.LazyFunction(lambda: fake.text(max_nb_chars=2000))
    date = factory.LazyFunction(timezone.now)
    summary = factory.LazyFunction(lambda: fake.text(max_nb_chars=250))
    author = factory.LazyFunction(fake.name)