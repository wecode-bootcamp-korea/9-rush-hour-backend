from django.db import models


class UserInfo(models.Model):

    """ Definition of User Model """
    user_id          = models.CharField(max_length = 50, null = True)
    password         = models.CharField(max_length = 200)
    nickname         = models.CharField(max_length = 50, null = True)
    email            = models.EmailField(max_length = 200)
    name             = models.CharField(max_length = 50)
    phone_number     = models.CharField(max_length = 50)
    address          = models.CharField(max_length = 300)
    marketing_agreed = models.BooleanField(default = False)
    is_guest         = models.BooleanField(default = True)
    created_at       = models.DateTimeField(auto_now_add = True)
    updated_at       = models.DateTimeField(auto_now  = True)
    #likes            = models.ManyToManyField("product.Product", through = "product.like", on_delete = models.SET_NULL, null = True, related_name = "liked_by_user")

    class Meta:
        db_table = "users"

    def __str__(self):
        return self.user_id
