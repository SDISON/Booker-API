from django.http import Http404
from .serializers import CreateTicketSerializer, UpdateTimeSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from booker.views import BookerViews
import re
import json

# A post api call to create the ticket based on name, date, time and phone. 
# Return 4 responses :
#	1. 401 == When a particular slot is full in which user trying to book.
#	2. 201 == When the ticket succesfully registered for a slot.
#	3. 500 == If any internal server error occured in case.
#	4. 400 == If the query requested is not valid.

class CreateTicket(APIView):

	def post(self, request, format = None):
		serializer = CreateTicketSerializer(data = request.data)
		if(serializer.is_valid()):
			response = BookerViews().create_ticket(request)				# Calling the booker app functions for registering the ticket.
			json_ = json.loads(response.content)
			if json_["msg"] == 'Slot Full':
				return Response({"msg":"This Current Time Slot is Full"}, status = status.HTTP_401_UNAUTHORIZED)
			elif json_["msg"] == 'Successfully created':
				return Response({"msg":"Success", "ticket_id":json_["ticket_id"]}, status = status.HTTP_201_CREATED)
			else:
				return Response({"msg":"Some Internal Error Occurred"}, status = 500)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# A put api call to update the ticket time using the ticket-id.
# Return 4 responses :
#	1. 401 == When this particular ticket-id is not present in the database.
#	2. 201 == When the time succesfully changed.
#	3. 500 == If any internal server error occured in case.
#	4. 400 == If the query requested is not valid.


class UpdateTime(APIView):
	
	def put(self, request, pk, format = None):
		serializer = UpdateTimeSerializer(data = request.data)
		if(serializer.is_valid()):
			response = BookerViews().update_time(request, pk)			# Calling the booker app function for updating the time.
			json_ = json.loads(response.content)
			if json_["msg"] == 'Not Found':
				return Response({"msg":"This Ticket Id Is Not Found"}, status = status.HTTP_401_UNAUTHORIZED)
			elif json_["msg"] == 'Success':
				return Response({"msg":"Success"}, status = status.HTTP_201_CREATED)
			else:
				return Response({"msg":"Some Internal Error Occurred"}, status = 500)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
		
		
		
		
		
# A post api call to view all the ticket in a time slot based on time and date. 
# Return 3 responses :
#	1. 200 == When the ticket data succesfully fetched from server.
#	2. 500 == If any internal server error occured in case.
#	3. 400 == If the query requested is not valid.
		
		
class ViewByTime(APIView):
	
	def post(self, request, format = None):
		data_time = request.data['time']
		if(re.match(r'^[0-9]{2}[:][0-9]{2}$', data_time)):
			response = BookerViews().view_bytime(request)				# Calling the booker app function to get all slot tickets.
			json_ = json.loads(response.content)
			if json_["msg"] == 'Fail':
				return Response({"msg":"Some Internal Error Occurred"}, status = 500)
			else:
				return Response({"msg":"Success", "data":json_["data"]}, status = status.HTTP_200_OK)
		return Response({"msg":"Format Error"}, status=status.HTTP_400_BAD_REQUEST)
		
		
		
		
		
# A delete api call to delete the ticket based on ticket-id. 
# Return 3 responses :
#	1. 401 == When this particular id is not in database.
#	2. 200 == When the ticket succesfully deleted.
#	3. 500 == If any internal server error occured in case.


		
class DeleteTicket(APIView):
	
	def delete(self, request, pk, format = None):
		response = BookerViews().delete_ticket(request, pk)				# Calling the booker app function to delete the ticket.
		json_ = json.loads(response.content)
		if json_["msg"] == 'Not Found':
			return Response({"msg":"This Ticket Id Is Not Found"}, status = status.HTTP_401_UNAUTHORIZED)
		if json_["msg"] == 'Success':
			return Response({"msg":"Success"}, status = status.HTTP_200_OK)
		else:
			return Response({"msg":"Some Internal Error Occurred"}, status = 500)
		
		
		
# A get api call to get the ticket details based on ticket-id. 
# Return 4 responses :
#	1. 401 == When this particular id is not in database.
#	2. 200 == When the ticket data succesfully fetched from server.
#	3. 500 == If any internal server error occured in case.
#	4. 400 == If the query requested is not valid.		
		
		
class ViewTicket(APIView):
	
	def get(self, request, pk, format = None):
		if(re.match(r'^[1-9][0-9]{5}', pk)):
			response = BookerViews().view_ticket(request, pk)			# Calling the booker app function to get ticket details.
			json_ = json.loads(response.content)					
			if json_["msg"] == 'Not Found':
				return Response({"msg":"This Ticket Id Is Not Found"}, status = status.HTTP_401_UNAUTHORIZED)
			elif json_["msg"] == 'Fail':
				return Response({"msg":"Some Internal Error Occurred"}, status = 500)
			else:
				return Response({"msg":"Success", "data":json_["data"]}, status = status.HTTP_200_OK)
		return Response({"msg":"Ticker Id Format Error"}, status=status.HTTP_400_BAD_REQUEST)
		
		
		
		
# A put api call to mark a ticket expired based on ticket-id.
# Return 3 responses :
#	1. 401 == When this particular id is not in database.
#	2. 200 == When the ticket status succesfully updated.
#	3. 500 == If any internal server error occured in case.	
		
		
class MarkExpire(APIView):
	
	def put(self, request, pk, format = None):
		response = BookerViews().mark_expire_one(request, pk)				# Calling the booker app function to mark expired.
		json_ = json.loads(response.content)
		if json_["msg"] == 'Not Found':
			return Response({"msg":"This Ticket Id Is Not Found"}, status = status.HTTP_401_UNAUTHORIZED)
		elif json_["msg"] == 'Fail':
			return Response({"msg":"Some Internal Error Occurred"}, status = 500)
		else:
			return Response({"msg":"Success", "data":json_["data"]}, status = status.HTTP_200_OK)
	
