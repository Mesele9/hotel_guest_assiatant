from django.db import models

class MainCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100)
    main_category = models.ForeignKey(MainCategory, on_delete=models.CASCADE)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.main_category.name} - {self.name}"

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    icon = models.CharField(max_length=50, blank=True, 
                          help_text="Font Awesome icon class (e.g. 'fas fa-leaf')")
    color = models.CharField(max_length=20, default='#6c757d', 
                           help_text="Hex color code for tag background")

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    categories = models.ManyToManyField(Category)
    tags = models.ManyToManyField(Tag, blank=True)
    image = models.ImageField(upload_to='menu_images/', blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag, blank=True) 

    def __str__(self):
        return self.name

class Rating(models.Model):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    stars = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField(blank=True)
    guest_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.menu_item} - {self.stars} stars"
