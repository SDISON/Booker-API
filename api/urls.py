from django.contrib import admin
from django.conf.urls import url
from . import views


# CreateTicket = An api call to create a ticket
# UpdateTime   = An api call to update the time of a pre-registered ticket.
# ViewByTime   = An api call to view all tickets registered at a particular date and time.
# DeleteTicket = An api call to delete a pre-registered ticket using the ticket-id.
# ViewTicket   = An api call to view the details of a per-registered ticket using ticket-id.
# MarkExpire   = An api call to change the status of a ticket to expire using ticket-id. 

urlpatterns = [
    url('^CreateTicket', views.CreateTicket.as_view()),
    url('^UpdateTime/(?P<pk>[0-9]+)', views.UpdateTime.as_view()),
    url('^ViewByTime', views.ViewByTime.as_view()),
    url('^DeleteTicket/(?P<pk>[0-9]+)', views.DeleteTicket.as_view()),
    url('^ViewTicket/(?P<pk>[0-9]+)', views.ViewTicket.as_view()),
    url('^MarkExpire/(?P<pk>[0-9]+)', views.MarkExpire.as_view()),
]
