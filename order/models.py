from django.db import models

class Order(models.Model):

    """ Definition of Order Model """
    user_info       = models.ForeignKey("user.UserInfo", on_delete = models.CASCADE, related_name = "ordered")
    order_date      = models.DateTimeField(auto_now_add = True)
    order_number    = models.CharField(max_length = 200)
    amount          = models.IntegerField(null=True)
    price           = models.DecimalField(max_digits = 10, decimal_places = 2, null = True)
    payment         = models.ForeignKey("Payment", on_delete = models.SET_NULL, null = True)
    order_status    = models.ForeignKey("OrderStatus", on_delete = models.SET_NULL, null = True, related_name = "order_list")
    product         = models.ManyToManyField("product.Product", through = "OrderItem", related_name = "order")
    shipping        = models.OneToOneField("ShippingInfo", on_delete = models.SET_NULL, null = True)

    class Meta:
        db_table    = "orders"

    def __str__(self):
        return f"{self.user_info.user_id}_order"

class OrderItem(models.Model):

    """ Definition of OrderItem Model """
    order           = models.ForeignKey("Order", on_delete = models.CASCADE)
    product         = models.ForeignKey("product.Product", on_delete = models.CASCADE)
    amount          = models.IntegerField()

    class Meta:
        db_table    = "order_items"

    def __str__(self):
        return f"order:{self.order_id}_product:{self.product_id}"

class OrderStatus(models.Model):

    """ Definition of OrderStatus Model """
    status          = models.CharField(max_length = 50)

    class Meta:
        db_table    = "status"

    def __str__(self):
        return self.status

class ShippingInfo(models.Model):

    """ Definition of ShippingInfo Model """
    name            = models.CharField(max_length = 50)
    address         = models.CharField(max_length = 300)
    phone_no        = models.CharField(max_length = 100, null=True)
    message         = models.TextField()
    shipping_list   = models.OneToOneField('ShippingList', on_delete = models.SET_NULL, null=True) 

    class Meta:
        db_table    = "shipping_info"

class ShippingList(models.Model):

    """ Definition of Shpping Model """
    name            = models.CharField(max_length = 50)
    recipient       = models.CharField(max_length = 50)
    address         = models.CharField(max_length = 300)
    phone_no        = models.CharField(max_length = 100, null=True)
    default         = models.BooleanField(default=False)
    user            = models.ForeignKey("user.UserInfo", on_delete = models.CASCADE, related_name = "shipping_info")
    
    class Meta:
        db_table = "shipping_lists"

    def __str__(self):
        return f"{self.recipient}_shipping_info"

class Payment(models.Model):

    """ Definition of Payment Model """
    name    = models.CharField(max_length = 50)

    class Meta:
        db_table    = "payments"

    def __str__(self):
        return self.payment
