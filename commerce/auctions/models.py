from django.contrib.auth.models import AbstractUser
from django.db import models

# note to self: the smallest entity shouldn't FR back
class User(AbstractUser):
    pass

# required model for auction listings
class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    image_url = models.TextField()
    category = models.CharField(max_length=64)
    is_active = models.BooleanField()
    def __str__(self):
        return f"{self.title}\n{self.category}\n{self.description}\n{self.image_url}\nis active: {self.is_active}"

# class Comments(models.Model):
#     num_comments = models.BigIntegerField(default=0)
#     listing = models.OneToOneField(Listing, on_delete=models.CASCADE, primary_key=False, null=True, blank=True)
#     def __str__(self):
#         return f"{self.num_comments} comments in {self.listing}"

'''
# required model for comments
class Comment(models.Model):

    comment = models.CharField(max_length=1000,)
    timestamp = models.DateTimeField(auto_now_add=True)
    # foreign key for many to one relationship where class is the many
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments_listing",  blank=True, null=True)
    def __str__(self):
        if self.listing and self.comment and self.timestamp:
            return f"{self.listing} [{self.timestamp}]: {self.comment}"
        else:
            return "no comments"
'''

# required model for bids
class Bid(models.Model):
    price = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidding_user",  blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bid_listing",  blank=True, null=True)
    def __str__(self):
        return f"[{self.timestamp}]: {self.user} bidding at ${self.price} for {self.listing}"

'''
class Watchlist(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_watchlist",  blank=True, null=True)
    listings = models.ManyToManyField(Listing, blank=True, related_name="watchlists")
    def __str__(self):
        return f"{self.user}'s Listing\n{self.listings}"
'''