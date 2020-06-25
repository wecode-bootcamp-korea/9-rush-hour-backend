from django.db import models

class Menu(models.Model):

    """ Definition of Menu Model """
    name            = models.CharField(max_length = 50)

    class Meta:
        db_table    = "menu"

    def __str__(self):
        return self.name

class Category(models.Model):

    """ Definition of Category Model """
    name            = models.CharField(max_length = 50)
    code            = models.CharField(max_length = 50)
    menu            = models.ForeignKey("Menu", on_delete = models.CASCADE)

    class Meta:
        db_table    = "categories"

    def __str__(self):
        return self.name

class SubCategory(models.Model):

    """ Definition of SubCategory Model """
    name            = models.CharField(max_length = 50)
    code            = models.CharField(max_length = 50)
    category        = models.ForeignKey("Category", on_delete = models.CASCADE)

    class Meta:
        db_table    = "sub_categories"

    def __str__(self):
        return self.name

class Product(models.Model):

    """ Definition of Product Model """
    product_no      = models.CharField(max_length = 50)
    name            = models.CharField(max_length = 50)
    is_new          = models.BooleanField(default =False)
    is_vegan        = models.BooleanField(default =False)
    hash_tag        = models.CharField(max_length = 100)
    price           = models.IntegerField()
    stock           = models.IntegerField()
    sub_category    = models.ForeignKey("SubCategory", on_delete = models.SET_NULL, null = True, related_name = "product")
    detail          = models.OneToOneField("Detail", on_delete = models.CASCADE)
    related_products= models.ManyToManyField("self", through = "RelatedProduct", symmetrical = False)
    #orders          = models.ManyToManyField("order.Order", through = "order.OrderItem", on_delete = models.SET_NULL, null = True, related_name = "order_product")
    likes           = models.ManyToManyField("user.UserInfo", through = "Like", related_name = "likes_product")

    class Meta:
        db_table    = "products"

    def __str__(self):
        return self.name

class Image(models.Model):

    """ Definition of Image Model """
    url             = models.URLField()
    product         = models.ForeignKey("Product", on_delete = models.CASCADE, related_name = "thumbnail_image")

    class Meta:
        db_table    = "images"

    def __str__(self):
        return f"{self.product.name}_image"

class Detail(models.Model):

    """ Definition of Detail Model """
    video_url       = models.URLField()
    html            = models.TextField()

    class Meta:
        db_table    = "details"

    def __str__(self):
        return f"{self.product.name}_detail"

class Weight(models.Model):

    """ Definition of Weight Model """
    weight_g        = models.IntegerField()
    extra_price     = models.IntegerField()
    product         = models.ForeignKey("Product", on_delete = models.CASCADE, related_name = "weight")

    class Meta:
        db_table    = "weights"

    def __str__(self):
        return f"{self.prodcut.name}_weight"

class RelatedProduct(models.Model):
    
    """ Definition of RelatedProduct Model """
    from_product    = models.ForeignKey("Product", on_delete = models.CASCADE, related_name = "from_product")
    to_product      = models.ForeignKey("Product", on_delete = models.CASCADE, related_name = "to_product")

    class Meta:
        db_table    = "related_products"

    def __str__(self):
        return f"{self.from_product.name}_related"

class Like(models.Model):

    """ Definition of Like Model """
    user            = models.ForeignKey("user.UserInfo", on_delete = models.CASCADE)
    product         = models.ForeignKey("Product", on_delete = models.CASCADE)

    class Meta:
        db_table = "likes"

    def __str__(self):
        return f"user_{self.user_id}_likes_{self.product_id}"