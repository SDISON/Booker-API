from django.shortcuts import render
from .models import Ticket, Time_based
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
import datetime
import json
from django.http import JsonResponse


class BookerViews:

	try:
		id0 = Ticket.objects.latest('id').id						# To maintain a unique id of tickets.
	except:
		id0 = 0
	
	def get_latest_id(self):								# Function which return a unique id for new ticket.
		BookerViews.id0 += 1
		return int(BookerViews.id0)
		
	def generate_id(self,latest):								# Function to genrate a unique ticket_id for new ticket.
		return (latest * 3128) + 1000000
		
	def get_current_datetime(self):								# Get current time-date.
		return (datetime.datetime.now())
	
	def create_ticket(self, request):							# Function for creatinf new ticket.
		if request.method == 'POST':
			try:
				ticket = Ticket()
				latest = BookerViews().get_latest_id()
				ticket.ticket_id = BookerViews().generate_id(latest)
				ticket.name = request.data['name']
				ticket.phone = request.data['phone']
				ticket.date = datetime.datetime.strptime(request.data['date'], "%Y-%m-%d").date()
				ticket.time = datetime.datetime.strptime(request.data['time'], "%H:%M").time()
				response = BookerViews().check_time_full(ticket)					# Checking whether slot is full or not. 
				if  response == 'Full':
					return HttpResponse(json.dumps({"msg":'Slot Full'}))
				elif response == 'KO':
					return HttpResponse(json.dumps({"msg":'Error in checking'}))
				result = BookerViews().add_to_timebased_(ticket)					# Adding ticket-id to internal time-based table.
				if(result == 'KO'):
					return HttpResponse(json.dumps({"msg":"Error at time_based"}))
				ticket.save()
				return HttpResponse(json.dumps({"msg":"Successfully created", "ticket_id":ticket.ticket_id}))
			except Exception as e:
				#print(e)	
				return HttpResponse(json.dumps({"msg":"Error occured"}))
	
	def update_time(self, request, pk):							# Function to update time of a pre-registered ticket.
		try:
			try:
				ticket = Ticket.objects.get(ticket_id = pk)
			except ObjectDoesNotExist:
				return HttpResponse(json.dumps({"msg":"Not Found"}))
			try:
				BookerViews().remove_from_timebased_(ticket)			# Removing ticket-id from internal time-based table.
			except:
				return HttpResponse(json.dumps({"msg":"Error"}))
			ticket.time = datetime.datetime.strptime(request.data['time'], "%H:%M").time()
			ticket.date = datetime.datetime.strptime(request.data['date'], "%Y-%m-%d").date()
			try:
				BookerViews().add_to_timebased_(ticket)				# Adding ticket-id to internal time-based table.
			except:
				return HttpResponse(json.dumps({"msg":"Error"}))
			ticket.save()
			return HttpResponse(json.dumps({"msg":"Success"}))
		except:
			return HttpResponse(json.dumps({"msg":"Error"}))
		
	def view_bytime(self, request):								# Function to view tickets in a slot.
		try:
			time_ = datetime.datetime.strptime(request.data['time'], "%H:%M").time()
			date_ = datetime.datetime.strptime(request.data['date'], "%Y-%m-%d").date()
			id_ = (((((date_.year*100) + date_.month)*100 + date_.day)*100 + time_.hour)*100 + time_.minute)
			id_list = Time_based.objects.get(time_id = id_).json_id
			id_list = json.loads(id_list)
			data = []
			for item in id_list:
				if(item != 'length' and id_list[item] == 1):
					ticket_ = Ticket.objects.get(ticket_id = item)
					dict_ = {}
					dict_["ticket_id"] = item
					dict_["name"] = ticket_.name
					dict_["phone"] = ticket_.phone
					dict_["date"] = str(ticket_.date)
					dict_["time"] = ticket_.time
					data.append(dict_)
			return HttpResponse(json.dumps({"msg":"Success","data":data}))
		except Exception as e:
			#print(e)
			return HttpResponse(json.dumps({"msg":"Fail"}))
			
	def delete_ticket(self, request, pk_):							# Function to delete ticket based on ticket-id.
		try:
			id_ = pk_
			try:
				ticket = Ticket.objects.get(ticket_id = id_)
			except ObjectDoesNotExist as e:
				return HttpResponse(json.dumps({"msg":"Not Found"}))
			try:
				BookerViews().remove_from_timebased_(ticket)			# Removing ticket-id from internal time-based table.
			except:
				return HttpResponse(json.dumps({"msg":"Error"}))
			ticket.delete()
			return HttpResponse(json.dumps({"msg":"Success"}))
		except:
			return HttpResponse(json.dumps({"msg":"Error"}))
			
	def view_ticket(self, request, pk):							# Function to view details of a registered ticket.
		try:
			id_ = pk
			try:
				ticket = Ticket.objects.get(ticket_id = id_)
			except ObjectDoesNotExist as e:
				#print(e)
				return HttpResponse(json.dumps({"msg":"Not Found"}))
			data = {"id":ticket.ticket_id,"name":ticket.name, "phone":ticket.phone, "date":str(ticket.date), "time":ticket.time}
			return HttpResponse(json.dumps({"msg":"Success", "data":data}))
		except Exception as e:
			#print(e)
			return HttpResponse(json.dumps({"msg":"Fail"}))
			
	def mark_expire_one(self, request, pk):							# Function to mark a ticket expired on ticket-id based.
		try:
			current_datetime = BookerViews().get_current_datetime()
			try:
				ticket = Ticket.objects.get(ticket_id = pk)
				ticket_datetime = datetime.datetime.combine(ticket.date, datetime.datetime.strptime(ticket.time, "%H:%M:%S").time())
			except ObjectDoesNotExist as e:
				#print(e)
				return HttpResponse(json.dumps({"msg":"Not Found"}))
			diff = current_datetime - ticket_datetime
			diff = diff.days*24*3600 + diff.seconds
			if(diff >= 28800):							# Checking 8hrs condition.
				ticket.status = 'F'
			data = {"id":ticket.ticket_id,"name":ticket.name, "phone":ticket.phone, "date":str(ticket.date), "time":ticket.time, "status":ticket.status}
			ticket.save()
			return HttpResponse(json.dumps({"msg":"Success", "data":data}))
		except:
			return HttpResponse(json.dumps({"msg":"Fail"}))
			
	def delete_expire_tickets(self):							# Function to delete all expired tickets.
		try:
			all_obj = Ticket.objects.filter()
			current_datetime = BookerViews().get_current_datetime()
			for ticket in all_obj:
				ticket_datetime = datetime.datetime.combine(ticket.date, datetime.datetime.strptime(ticket.time, "%H:%M:%S").time())
				diff = current_datetime - ticket_datetime
				diff = diff.days*24*3600 + diff.seconds
				if(diff >= 28800):
					BookerViews().remove_from_timebased_(ticket)		# Removing ticket-id from internal time-based table.
				ticket.delete()
			return 'Done'
		except Exception as e:
			#print(e)
			return 'Fail'
			
	def add_to_timebased_(self, ticket):							# Function for adding ticket-id to internal time-based table.
		try:
			id_ = (((((ticket.date.year*100) + ticket.date.month)*100 + ticket.date.day)*100 + ticket.time.hour)*100 + ticket.time.minute)
			try:
				timebased_ = Time_based.objects.get(time_id = id_)
				json_ = json.loads(timebased_.json_id)
				json_[ticket.ticket_id] = 1
				json_["length"] = json_["length"] + 1
				timebased_.json_id = json.dumps(json_)
				timebased_.save()
			except ObjectDoesNotExist as e:
				#print(e)
				timebased_ = Time_based()
				timebased_.time_id = id_
				dict_ = "{}"
				json_ = json.loads(dict_)
				json_["length"] = 1
				json_[ticket.ticket_id] = 1
				timebased_.json_id = json.dumps(json_)
				timebased_.save()
			return 'OK'
		except Exception as e:
			#print(e)
			return 'KO'
			
	def remove_from_timebased_(self, ticket):						# Function for removing ticket-id from internal time-based table.
		try:
			ticket.time = datetime.datetime.strptime(ticket.time, "%H:%M:%S").time()
			id_ = (((((ticket.date.year*100) + ticket.date.month)*100 + ticket.date.day)*100 + ticket.time.hour)*100 + ticket.time.minute)
			try:
				timebased_ = Time_based.objects.get(time_id = id_)
				json_ = json.loads(timebased_.json_id)
				del json_[str(ticket.ticket_id)]
				json_["length"] = json_["length"] - 1
				timebased_.json_id = json.dumps(json_)
				timebased_.save()
			except ObjectDoesNotExist as e:
				#print(e, 'remove_object')
				return 'KO'
			return 'OK'
		except Exception as e:
			#print(e, 'exception_remove')
			return 'KO'
			
	def check_time_full(self, ticket):							# Function for checking ticket slot in internal time-based table.
		try:
			id_ = (((((ticket.date.year*100) + ticket.date.month)*100 + ticket.date.day)*100 + ticket.time.hour)*100 + ticket.time.minute)
			try:
				timebased_ = Time_based.objects.get(time_id = id_)
				json_ = json.loads(timebased_.json_id)
				if json_["length"] >= 20:
					return 'Full'
			except ObjectDoesNotExist as e:
				#print(e, 'object_full_check')
				return 'Empty'
			return 'Empty'
		except Exception as e:
			#print(e, 'full_exception')
			return 'KO'
