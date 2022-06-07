from django.db import models

class country(models.Model):
    name = models.TextField(unique=True)

    class Meta:
        ordering = ['name']
        verbose_name = "Country"
        verbose_name_plural = "Countries"

    def __str__(self):
        return self.name

class city(models.Model):
    country = models.ForeignKey(to=country, on_delete=models.CASCADE)
    name = models.TextField(unique=True)

    class Meta:
        ordering = ['name']
        verbose_name = "City"
        verbose_name_plural = "Cities"

    def __str__(self):
        return self.name

class category(models.Model):
    name = models.TextField(unique=True)

    class Meta:
        ordering = ['name']
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class educational_sector(models.Model):
    name =  models.TextField(unique=True)

    class Meta:
        ordering = ['name']
        verbose_name = "Educational Sector"
        verbose_name_plural = "Educational Sectors"

    def __str__(self):
        return self.name

class coordinator(models.Model):
    name = models.TextField()
    email = models.TextField(null=True, blank=True)
    tel = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ['name']
        verbose_name = "Coordinator"
        verbose_name_plural = "Coordinators"

    def __str__(self):
        return self.name

class school(models.Model):
    category = models.ManyToManyField(to=category, blank=True)
    coordinator = models.ForeignKey(to=coordinator, on_delete=models.CASCADE, null=True, blank=True)
    educational_sector = models.ManyToManyField(to=educational_sector)
    city = models.ForeignKey(to=city, on_delete=models.CASCADE)
    name = models.TextField(unique=True)
    email = models.TextField(null=True)
    tel = models.TextField(null=True)
    address = models.TextField(null=True, blank=True)
    website = models.URLField(null=True)

    class Meta:
        ordering = ['name']
        verbose_name = "School"
        verbose_name_plural = "Schools"

    def __str__(self):
        return self.name