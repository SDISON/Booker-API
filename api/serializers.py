from booker.models import Ticket, Time_based
from rest_framework import serializers



# A serializer to format the data coming for registration of new ticket.

class CreateTicketSerializer(serializers.ModelSerializer):

	class Meta:
		model = Ticket
		fields = ('name', 'phone', 'date', 'time')
		
		

# A serializer to format the data coming for update of time of a pre-registered ticket.
		
class UpdateTimeSerializer(serializers.ModelSerializer):	
	
	class Meta:
		model = Ticket
		fields = ('ticket_id', 'time', 'date')
