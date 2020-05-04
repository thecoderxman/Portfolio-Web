from django.db import models

class stocks(models.Model):
	date = models.CharField(max_length=200, null=True)
	price = models.FloatField(null=True, blank=True, default=None)
	name = models.CharField(max_length=200, null=True)
	def __str__(self):
		return self.name

class investments(models.Model):
	name = models.CharField(max_length=200, null=True)
	price = models.FloatField(null=True, blank=True, default=None)
	date_created = models.CharField(max_length=200, null=True)
	current_time= models.CharField(max_length=200, null=True)
	gain_loss= models.CharField(max_length=200, null=True)

	def __str__(self):
		return self.name
class investmentsinfunds(models.Model):
	name = models.CharField(max_length=200, null=True)
	price = models.FloatField(null=True, blank=True, default=None)
	date_created = models.CharField(max_length=200, null=True)
	current_time= models.CharField(max_length=200, null=True)
	gain_loss= models.CharField(max_length=200, null=True)

	def __str__(self):
		return self.name
class investmentsincommodities(models.Model):
	name = models.CharField(max_length=200, null=True)
	price = models.FloatField(null=True, blank=True, default=None)
	date_created = models.CharField(max_length=200, null=True)
	current_time= models.CharField(max_length=200, null=True)
	gain_loss= models.CharField(max_length=200, null=True)

	def __str__(self):
		return self.name
class investmentsinindices(models.Model):
	name = models.CharField(max_length=200, null=True)
	price = models.FloatField(null=True, blank=True, default=None)
	date_created = models.CharField(max_length=200, null=True)
	current_time= models.CharField(max_length=200, null=True)
	gain_loss= models.CharField(max_length=200, null=True)

	def __str__(self):
		return self.name

class investmentsinbonds(models.Model):
	name = models.CharField(max_length=200, null=True)
	price = models.FloatField(null=True, blank=True, default=None)
	date_created = models.CharField(max_length=200, null=True)
	current_time= models.CharField(max_length=200, null=True)
	gain_loss= models.CharField(max_length=200, null=True)

	def __str__(self):
		return self.name
		
class investmentsinfutures(models.Model):
	name = models.CharField(max_length=200, null=True)
	price = models.FloatField(null=True, blank=True, default=None)
	date_created = models.CharField(max_length=200, null=True)
	current_time= models.CharField(max_length=200, null=True)
	gain_loss= models.CharField(max_length=200, null=True)
	expiry_date= models.CharField(max_length=200, null=True)
	def __str__(self):
		return self.name
		
class money(models.Model):
	mymoney = models.FloatField(null=True, blank=True, default=None)

	
