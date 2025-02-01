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
    seats = models.JSONField()  # Assuming seats is a JSON field
    user_info = models.JSONField()  # Store user information as JSON
    movie_id = models.IntegerField()  # Add movie_id field
    theatre_id = models.IntegerField()  # Add theatre_id field
    show_timings_id = models.IntegerField()  # Add show_timings_id field
    status = models.CharField(max_length=50, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Payment for {self.user.username} - {self.payment_intent_id}"
    
class BookedSeat(models.Model):
    seat_id = models.CharField(max_length=10)  # Example: A1, B2
    show_timings_id = models.IntegerField()
    movie_id = models.IntegerField()  # New field for movie ID
    theatre_id = models.IntegerField()  # New field for theatre ID
    booked = models.BooleanField(default=False)

    def __str__(self):
        return f"Seat {self.seat_id} for movie {self.movie_id}, show {self.show_timings_id} at theatre {self.theatre_id} - {'Booked' if self.booked else 'Available'}"