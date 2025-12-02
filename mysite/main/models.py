from django.db import models

class Articles(models.Model):
    title = models.CharField('Title', max_length=50)
    summary = models.CharField('Summary', max_length=250, default='')
    full_text = models.TextField('Article')
    author = models.CharField('Author', max_length=100, null=True, blank=True)
    date = models.DateTimeField('Publication Date')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'

class Comments(models.Model):
    article = models.ForeignKey(Articles, on_delete=models.CASCADE, related_name='comments')
    author = models.CharField('Author', max_length=100)
    content = models.TextField('Comment')
    date = models.DateTimeField('Publication Date', null=True, blank=True)
    
    def __str__(self):
        return f'Comment by {self.author}'
    
    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
