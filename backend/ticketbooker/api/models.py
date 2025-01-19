from django.db import models
from django.contrib.auth.models import User  # Import User model

# Create your models here.

class Movie(models.Model):
    image = models.ImageField(upload_to='movies/', null=True, blank=True)
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    release_date = models.CharField(max_length=100)
    language = models.CharField(max_length=100)
    rating = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
class Theatre(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    movies = models.ManyToManyField(Movie, related_name='theatres')

    def __str__(self):
        return self.name

class ShowTiming(models.Model):
    theatre = models.ForeignKey(Theatre, related_name='show_timings', on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, related_name='show_timings', on_delete=models.CASCADE)
    timing = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.movie.name} at {self.theatre.name} on {self.timing}"
    
    def save(self, *args, **kwargs):
        if self.movie in self.theatre.movies.all():
            super().save(*args, **kwargs)
        else:
            raise ValueError("The movie is not available in the selected theatre.")

class Contact_us(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    phone = models.IntegerField()
    subject = models.CharField(max_length=255)
    message = models.TextField()
    
    def __str__(self):
        return self.name

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_intent_id = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    seats = models.JSONField()  # Store the list of booked seats
    user_info = models.JSONField()  # Store user info (name, email, etc.)
    status = models.CharField(max_length=50, default='pending')  # Payment status

    def __str__(self):
        return f"Payment for {self.user.username} - {self.payment_intent_id}"