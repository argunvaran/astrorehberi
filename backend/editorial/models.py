from django.db import models

class WeeklyEditorial(models.Model):
    title = models.CharField(max_length=200, default="Haftalık Kozmik Yorum")
    content = models.TextField(help_text="Buraya haftalık genel yorum gelecek. HTML kullanılabilir.")
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} ({self.created_at.strftime('%d.%m.%Y')})"
