from django.urls import include, path
from rest_framework import status
from rest_framework.test import APITestCase, RequestsClient, URLPatternsTestCase
from booker.models import Ticket
import datetime
import json


class CreateTicket(APITestCase):
	
	# a valid data ticket creation
	def testcase1(self):
		data = {"name":"Ram", "phone":"9876543210", "date":"2020-08-29", "time":"23:46"}
		url = 'http://127.0.0.1:8000/api/CreateTicket'
		response = self.client.post(url, data)
		json_ = json.loads(response.content)
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertEqual(Ticket.objects.count(), 1)
		self.assertEqual(json_["ticket_id"], 1000000+(1*3128))				#ticket_id = 1000000 + (3128 * obj_id)
		self.assertEqual(Ticket.objects.get().name, data["name"])
		self.assertEqual(Ticket.objects.get().phone, data["phone"])
		self.assertEqual(Ticket.objects.get().date, datetime.datetime.strptime(data["date"], "%Y-%m-%d").date())
		self.assertEqual(Ticket.objects.get().time, data["time"]+":00")
		self.assertEqual(Ticket.objects.get().status, "T")
		
	# invalid(name) data ticket
	def testcase2(self):
		data = {"name":"Ram3", "phone":"9876543210", "date":"2020-08-29", "time":"23:46"}
		url = 'http://127.0.0.1:8000/api/CreateTicket'
		response = self.client.post(url, data)
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertEqual(Ticket.objects.count(), 0)
		
		
	# invalid(phone) data ticket
	def testcase3(self):
		data = {"name":"Ram", "phone":"987654321", "date":"2020-08-29", "time":"23:46"}
		url = 'http://127.0.0.1:8000/api/CreateTicket'
		response = self.client.post(url, data)
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertEqual(Ticket.objects.count(), 0)
		
	# invalid(date) data ticket
	def testcase4(self):
		data = {"name":"Ram", "phone":"9876543210", "date":"2020-02-30", "time":"23:46"}
		url = 'http://127.0.0.1:8000/api/CreateTicket'
		response = self.client.post(url, data)
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertEqual(Ticket.objects.count(), 0)
	
	# invalid(time should be in [HH:MM]) data ticket
	def testcase5(self):
		data = {"name":"Ram", "phone":"9876543210", "date":"2020-08-29", "time":"23:46:00"}
		url = 'http://127.0.0.1:8000/api/CreateTicket'
		response = self.client.post(url, data)
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertEqual(Ticket.objects.count(), 0)
		
	# multi valid ticket insertion
	def testcase6(self):
		for i in range(0, 7):
			data = {"name":"Ram", "phone":"9876543210", "date":"2020-08-29", "time":"23:46"}
			url = 'http://127.0.0.1:8000/api/CreateTicket'
			response = self.client.post(url, data)
			json_ = json.loads(response.content)
			self.assertEqual(response.status_code, status.HTTP_201_CREATED)
			self.assertEqual(Ticket.objects.count(), i+1)
			self.assertEqual(Ticket.objects.get(pk = i+1).ticket_id, int(json_["ticket_id"]))
			self.assertEqual(Ticket.objects.get(pk = i+1).name, data["name"])
			self.assertEqual(Ticket.objects.get(pk = i+1).phone, data["phone"])
			self.assertEqual(Ticket.objects.get(pk = i+1).date, datetime.datetime.strptime(data["date"], "%Y-%m-%d").date())
			self.assertEqual(Ticket.objects.get(pk = i+1).time, data["time"]+":00")
			self.assertEqual(Ticket.objects.get(pk = i+1).status, "T")
		self.assertEqual(Ticket.objects.count(), 7)
		
	# check time slot full query with database check also
	def testcase7(self):
		for i in range(0, 20):
			data = {"name":"Ram", "phone":"9876543210", "date":"2020-08-29", "time":"23:46"}
			url = 'http://127.0.0.1:8000/api/CreateTicket'
			response = self.client.post(url, data)
			self.assertEqual(response.status_code, status.HTTP_201_CREATED)
			self.assertEqual(Ticket.objects.count(), i+1)
		data = {"name":"Ram", "phone":"9876543210", "date":"2020-08-29", "time":"23:46"}
		url = 'http://127.0.0.1:8000/api/CreateTicket'
		response = self.client.post(url, data)
		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
		self.assertEqual(response.data['msg'], 'This Current Time Slot is Full')
		self.assertEqual(Ticket.objects.count(), 20)
		
		
class UpdateTime(APITestCase):
	
	#valid time update
	def testcase1(self):
		for i in range(0, 1):
			data = {"name":"Ram", "phone":"9876543210", "date":"2020-08-29", "time":"23:46"}
			url = 'http://127.0.0.1:8000/api/CreateTicket'
			response = self.client.post(url, data)
			self.assertEqual(Ticket.objects.get().time, data["time"]+":00")
		id_ = Ticket.objects.get().ticket_id
		data = {"date":"2020-08-29", "time":"23:00"}
		url = 'http://127.0.0.1:8000/api/UpdateTime/' + str(id_)
		response = self.client.put(url, data)
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertEqual(Ticket.objects.get().time, data["time"]+":00")
		
	#invalid time update request
	def testcase2(self):
		for i in range(0, 1):
			data = {"name":"Ram", "phone":"9876543210", "date":"2020-08-29", "time":"23:46"}
			url = 'http://127.0.0.1:8000/api/CreateTicket'
			response = self.client.post(url, data)
			self.assertEqual(Ticket.objects.get().time, data["time"]+":00")
		id_ = Ticket.objects.get().ticket_id
		data = {"date":"2020-08-29", "time":"23:00:10"}							#changing time format as valid format is [HH:MM]
		url = 'http://127.0.0.1:8000/api/UpdateTime/' + str(id_)
		response = self.client.put(url, data)
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
	
	#update using wrong ticket id
	def testcase3(self):
		for i in range(0, 1):
			data = {"name":"Ram", "phone":"9876543210", "date":"2020-08-29", "time":"23:46"}
			url = 'http://127.0.0.1:8000/api/CreateTicket'
			response = self.client.post(url, data)
			self.assertEqual(Ticket.objects.get().time, data["time"]+":00")
		id_ = Ticket.objects.get().ticket_id
		data = {"date":"2020-08-29", "time":"23:00"}
		url = 'http://127.0.0.1:8000/api/UpdateTime/' + str('0000000')
		response = self.client.put(url, data)
		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
		self.assertEqual(response.data['msg'], "This Ticket Id Is Not Found")
		
		
class ViewByTime(APITestCase):
	
	#valid test
	def testcase1(self):
		for i in range(0, 3):
			data = {"name":"Ram", "phone":"9876543210", "date":"2020-08-29", "time":"23:46"}
			url = 'http://127.0.0.1:8000/api/CreateTicket'
			response = self.client.post(url, data)
			self.assertEqual(Ticket.objects.count(), i+1)
		data = {"date":"2020-08-29","time":"23:46"}
		url = 'http://127.0.0.1:8000/api/ViewByTime/'
		response = self.client.post(url, data)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		json_ = json.loads(response.content)
		data = {"name":"Ram", "phone":"9876543210", "date":"2020-08-29", "time":"23:46"}
		for index, item in enumerate(json_["data"]):
			self.assertEqual(item["name"], data["name"])
			self.assertEqual(item["phone"], data["phone"])
			self.assertEqual(item["date"], data["date"])
			self.assertEqual(item["time"], data["time"]+":00")
			

	#invalid testcase
	def testcase2(self):
		data = {"date":"2020-08-29", "time":"23:46:10"}
		url = 'http://127.0.0.1:8000/api/ViewByTime/'
		response = self.client.post(url, data)
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		
		
class DeleteTicket(APITestCase):
	
	#valid testcase
	def testcase1(self):
		data = {"name":"Ram", "phone":"9876543210", "date":"2020-08-29", "time":"23:46"}
		url = 'http://127.0.0.1:8000/api/CreateTicket'
		response = self.client.post(url, data)
		json_ = json.loads(response.content)
		self.assertEqual(Ticket.objects.count(), 1)
		url = 'http://127.0.0.1:8000/api/DeleteTicket/' + str(json_["ticket_id"])
		response = self.client.delete(url)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		
		
	#invalid query
	def testcase2(self):
		data = {"name":"Ram", "phone":"9876543210", "date":"2020-08-29", "time":"23:46"}
		url = 'http://127.0.0.1:8000/api/CreateTicket'
		response = self.client.post(url, data)
		json_ = json.loads(response.content)
		self.assertEqual(Ticket.objects.count(), 1)
		url = 'http://127.0.0.1:8000/api/DeleteTicket/' + str(1010101)
		response = self.client.delete(url)
		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
			
			

class ViewTicket(APITestCase):
	
	#valid query
	def testcase1(self):
		data = {"name":"Ram", "phone":"9876543210", "date":"2020-08-29", "time":"23:46"}
		url = 'http://127.0.0.1:8000/api/CreateTicket'
		response = self.client.post(url, data)
		json_ = json.loads(response.content)
		self.assertEqual(Ticket.objects.count(), 1)
		url = 'http://127.0.0.1:8000/api/ViewTicket/' + str(json_["ticket_id"])
		response = self.client.get(url)
		json_ = json.loads(response.content)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		json_ = json_["data"]
		self.assertEqual(json_["name"], data["name"])
		self.assertEqual(json_["phone"], data["phone"])	
		self.assertEqual(json_["date"], data["date"])
		self.assertEqual(json_["time"], data["time"]+":00")
		
	#invalid regex request
	def testcase2(self):
		data = {"name":"Ram", "phone":"9876543210", "date":"2020-08-29", "time":"23:46"}
		url = 'http://127.0.0.1:8000/api/CreateTicket'
		response = self.client.post(url, data)
		json_ = json.loads(response.content)
		self.assertEqual(Ticket.objects.count(), 1)
		url = 'http://127.0.0.1:8000/api/ViewTicket/' + str('0123456')
		response = self.client.get(url)
		json_ = json.loads(response.content)
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

	#invalid ticket id 
	def testcase3(self):
		data = {"name":"Ram", "phone":"9876543210", "date":"2020-08-29", "time":"23:46"}
		url = 'http://127.0.0.1:8000/api/CreateTicket'
		response = self.client.post(url, data)
		json_ = json.loads(response.content)
		self.assertEqual(Ticket.objects.count(), 1)
		url = 'http://127.0.0.1:8000/api/ViewTicket/' + str('1111111')
		response = self.client.get(url)
		json_ = json.loads(response.content)
		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class MarkExpire(APITestCase):
	
	def testcase1(self):
		data = {"name":"Ram", "phone":"9876543210", "date":"2020-08-31", "time":"23:46"}
		url = 'http://127.0.0.1:8000/api/CreateTicket'
		response = self.client.post(url, data)
		json_ = json.loads(response.content)
		url = 'http://127.0.0.1:8000/api/MarkExpire/' + str(json_["ticket_id"])
		id_ = int(json_["ticket_id"])
		response = self.client.put(url)
		json_ = json.loads(response.content)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(Ticket.objects.get(ticket_id = id_).status, "T")




	
			
			
			
			
			
			
