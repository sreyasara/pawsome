from _decimal import Decimal

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from auth_login.models import User


def create_order_id():
    # create order id in the format ORD00001 , ORD00002 etc
    last_order = Order.objects.all().order_by('id').last()
    if not last_order:
        return 'ORD000001'
    order_id = last_order.id
    new_order_id = int(order_id) + 1
    new_order_id = 'ORD' + str(new_order_id).zfill(6)
    return new_order_id


countries = ["Afghanistan", "Åland Islands", "Albania", "Algeria", "American Samoa", "Andorra", "Angola", "Anguilla",
             "Antigua and Barbuda", "Argentina", "Armenia", "Aruba", "Australia", "Austria", "Azerbaijan", "Bahamas",
             "Bahrain", "Bangladesh", "Barbados", "Belgium", "Belize", "Benin", "Bermuda", "Bhutan", "Bolivia",
             "Bosnia and Herzegovina", "Botswana", "Brazil", "British Indian Ocean Territory", "Brunei Darussalam",
             "Bulgaria", "Burkina Faso", "Burundi", "Cambodia", "Cameroon", "Canada", "Cape Verde", "Cayman Islands",
             "Central African Republic", "Chad", "Chile", "China", "Cocos (Keeling) Islands", "Colombia", "Comoros",
             "Congo", "Democratic Republic of the Congo", "Cook Islands", "Costa Rica", "Côte d'Ivoire", "Croatia",
             "Cyprus", "Czech Republic", "Denmark", "Djibouti", "Dominica", "Dominican Republic", "Ecuador", "Egypt",
             "El Salvador", "Eritrea", "Estonia", "Ethiopia", "Faeroe Islands", "Fiji", "Finland", "France",
             "French Guiana", "French Polynesia", "Gabon", "Gambia", "Georgia", "Germany", "Ghana", "Gibraltar",
             "Greece",
             "Greenland", "Grenada", "Guadeloupe", "Guam", "Guatemala", "Guernsey", "Guinea", "Guinea-Bissau", "Guyana",
             "Haiti", "Holy See", "Honduras", "Hong Kong Special Administrative Region of China", "Hungary", "Iceland",
             "India", "Indonesia", "Iraq", "Ireland", "Isle of Man", "Israel", "Italy", "Jamaica", "Japan", "Jersey",
             "Jordan", "Kazakhstan", "Kenya", "Kiribati", "Republic of Korea", "Kuwait", "Kyrgyzstan",
             "Lao People's Democratic Republic", "Latvia", "Lebanon", "Lesotho", "Liberia", "Libyan Arab Jamahiriya",
             "Liechtenstein", "Lithuania", "Luxembourg", "Macao Special Administrative Region of China",
             "The former Yugoslav Republic of Macedonia", "Madagascar", "Malawi", "Malaysia", "Maldives", "Mali",
             "Malta",
             "Marshall Islands", "Martinique", "Mauritania", "Mauritius", "Mayotte", "Mexico",
             "Micronesia, Federated States of", "Republic of Moldova", "Monaco", "Mongolia", "Montenegro", "Montserrat",
             "Morocco", "Mozambique", "Namibia", "Nepal", "Netherlands", "Netherlands Antilles", "New Caledonia",
             "New Zealand", "Nicaragua", "Niger", "Nigeria", "Norfolk Island", "Northern Mariana Islands", "Norway",
             "Oman", "Pakistan", "Palau", "Occupied Palestinian Territory", "Panama", "Papua New Guinea", "Paraguay",
             "Peru", "Philippines", "Poland", "Portugal", "Puerto Rico", "Qatar", "Réunion", "Romania", "Rwanda",
             "Saint Kitts and Nevis", "Saint Lucia", "Saint Vincent and the Grenadines", "Samoa", "San Marino",
             "Sao Tome and Principe", "Saudi Arabia", "Senegal", "Serbia", "Seychelles", "Sierra Leone", "Singapore",
             "Slovakia", "Slovenia", "Solomon Islands", "South Africa", "Spain", "Sri Lanka", "Suriname",
             "Svalbard and Jan Mayen Islands", "Swaziland", "Sweden", "Switzerland", "Taiwan, Province of China",
             "Tajikistan", "Thailand", "Timor-Leste", "Togo", "Tonga", "Trinidad and Tobago", "Tunisia", "Turkey",
             "Turkmenistan", "Turks and Caicos Islands", "Tuvalu", "Uganda", "United Arab Emirates",
             "United Kingdom of Great Britain and Northern Ireland", "United States of America",
             "United States Minor Outlying Islands", "Uruguay", "Uzbekistan", "Vanuatu",
             "Venezuela (Bolivarian Republic of)", "Viet Nam", "British Virgin Islands", "United States Virgin Islands",
             "Wallis and Futuna Islands", "Yemen", "Zambia", "Zimbabwe",
             ]


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'

    @property
    def count(self):
        return self.pets.count()

    @property
    def get_image_url(self):
        if self.pets.count() > 0:
            return self.pets.first().image.url
        return ''


class Pet(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pets', blank=True, null=True)
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='pets')
    price = models.FloatField(validators=[MinValueValidator(0.0)])
    description = models.TextField()
    image = models.ImageField(upload_to='pet_images')
    stock = models.IntegerField(validators=[MinValueValidator(0)])
    discount = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(100.0)], default=0.0)
    vaccinated = models.BooleanField(default=False)
    vaccinated_certificate = models.ImageField(upload_to='pet_images', blank=True, null=True)
    origin = models.CharField(max_length=100, blank=True, null=True)
    age = models.IntegerField(validators=[MinValueValidator(0)], default=1)

    def __str__(self):
        return self.name

    @property
    def get_discounted_price(self):
        return self.price - (self.price * self.discount / 100)

    @property
    def is_available(self):
        return self.stock > 0


# to store the delivery address
class Address(models.Model):
    user = models.ForeignKey('auth_login.User', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    address_line_1 = models.CharField(max_length=100)
    address_line_2 = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=12)

    def __str__(self):
        return self.first_name + " " + self.last_name


class Order(models.Model):
    user = models.ForeignKey('auth_login.User', on_delete=models.CASCADE)
    # the name of the order
    name = models.CharField(max_length=200, default=create_order_id)
    # the description of the order
    description = models.TextField(blank=True, null=True)
    # the date of the order
    date = models.DateTimeField(auto_now_add=True)
    # the price of the order
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))],
                                default=0.00)
    # the status of the order
    status = models.CharField(max_length=200, choices=(
        ("not started", "not started"),
        ('pending', 'Pending'),
        ('in progress', 'In Progress'),
        ('completed', 'Completed'),
    ), default='not started')
    delivery_date = models.DateTimeField(auto_now_add=True)
    delivery_address = models.ForeignKey(Address, on_delete=models.CASCADE, null=True, blank=True,
                                         related_name='order_delivery_address')
    type = models.CharField(max_length=200, choices=(
        ('metal', 'Metal'),
        ("ornament", "Ornament"),
        ('plastic', 'Plastic'),
    ), default='metal')
    payment_status = models.CharField(max_length=200, choices=(
        ('pending', 'Pending'),
        ('paid', 'Paid'),
    ), default='pending')
    razorpay_order_id = models.CharField(max_length=200, null=True, blank=True)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, null=True, blank=True, )

    # the string representation of the order
    def __str__(self):
        return self.name

    @property
    def total_price(self):
        total = 0
        for item in self.order_items.all():
            total += item.price
        return total


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    # the name of the order item
    item = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='order_item')

    # the quantity of the order item

    # the string representation of the order item
    def __str__(self):
        return self.item.name

    # the total price of the order item
    @property
    def price(self):
        return self.item.get_discounted_price


class Cart(models.Model):
    user = models.OneToOneField('auth_login.User', on_delete=models.CASCADE, related_name='cart')

    # the name of the order

    @property
    def total(self):
        total = 0
        for item in self.items.all():
            total += item.price
        return total


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    # the name of the order item
    item = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='cart_item')

    # the quantity of the order item

    # the string representation of the order item
    def __str__(self):
        return self.item.name

    # the total price of the order item
    @property
    def price(self):
        return self.item.get_discounted_price


class Review(models.Model):
    user = models.ForeignKey('auth_login.User', on_delete=models.CASCADE, blank=True, null=True)
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='reviews', blank=True, null=True)
    rating = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    comment = models.TextField()

    def __str__(self):
        return self.user.username + " " + self.pet.name

    @property
    def rating_string(self):
        return "★" * self.rating + "☆" * (5 - self.rating)

    @property
    def user_name(self):
        if self.user is None:
            return "Anonymous"
        if self.user.first_name is "" and self.user.last_name is "":
            return self.user.username

        return self.user.first_name + " " + self.user.last_name
