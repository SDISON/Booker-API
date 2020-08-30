from __future__ import unicode_literals
from django.db import models
from django.conf import settings
from django.core.validators import RegexValidator


validate_name = RegexValidator(r'^[a-zA-Z]+$')				# validator for name field in Ticket table.
validate_phone = RegexValidator(r'^[0-9]{10}$')				# validator for phone field in Ticket table.
validate_time = RegexValidator(r'^[0-9]{2}[:][0-9]{2}$', 'in HH:MM')	# validator for time field in Ticket table.
validate_status = RegexValidator(r'^[TF]{1}$')				# validator for status field in Ticket table.


# Ticket table to store the newly registered ticket indexed on basis of ticket_id.

class Ticket(models.Model):						
    ticket_id = models.IntegerField(default=10000000, unique = True)
    name = models.CharField(max_length=50,null=False, validators=[validate_name])
    phone = models.CharField(max_length=10,null=False, validators=[validate_phone])
    date = models.DateField()
    time = models.CharField(max_length=5, null=False, validators=[validate_time])
    status = models.CharField(max_length=1, default='T', validators=[validate_status])
    def __str__(self):
        return self.name
        
        
# Time_based table to store a particular slot tickets indexed on basis of time_id. Inner table only used to optimize the query for which we have to return tickets of a slot and also the count of tickets in a slot.
# json_id = store the ticket_id of tickets registered for a certain slot.
        
class Time_based(models.Model):
	time_id = models.IntegerField(unique= True)
	json_id = models.TextField(max_length=1000)
	def __str__(self):
		return str(self.time_id)
