from django.db import models

class Review(models.Model):

    """ Definition of Review Model """
    stars        = models.IntegerField()
    date         = models.DateField(auto_now_add = True)
    review       = models.TextField()
    user         = models.ForeignKey("user.Userinfo", on_delete = models.CASCADE, related_name = "wrote_review")
    product      = models.ForeignKey("product.Product", on_delete = models.CASCADE, related_name = "written_review")

    class Meta:
        db_table = "reviews"

    def __str__(self):
        return f"{self.product.name}_{self.user.user_id}_review"

class ReviewImage(models.Model):

    """ Definition of ReviewImage Model """
    url          = models.URLField()
    review       = models.ForeignKey("Review", on_delete = models.CASCADE, related_name = "added_image")

    class Meta:
        db_table = "review_images"

    def __str__(self):
        return f"{self.review_id}_image"
