from django.contrib import admin
from django.conf.urls import url
from . import views


# create_ticket = Without api call to create a ticket
# view_bytime   = Without api call to view all tickets registered at a particular date and time.
# delete_ticket = Without api call to delete a pre-registered ticket using the ticket-id.
# view_ticket   = Without api call to view the details of a per-registered ticket using ticket-id.
# mark_expire_one  = Without api call to change the status of a ticket to expire using ticket-id. 


urlpatterns = [
    url('^create_ticket', views.BookerViews.create_ticket, name="create"),
    url('^delete_ticket/(?P<pk>[0-9]+)', views.BookerViews.delete_ticket, name="delete"),
    url('^view_ticket', views.BookerViews.view_ticket, name="view"),
    url('^view_bytime/(?P<pk>[0-9]+)', views.BookerViews.view_bytime, name="grp_view"),
    url('^mark_expire_one/(?P<pk>[0-9]+)', views.BookerViews.mark_expire_one, name="mark"),
]
