from django_cron import CronJobBase, Schedule
from booker.views import BookerViews

#Cron job that run every hour to delete expired tickets and configured using linux-crontab.

class MyCronJob(CronJobBase):
	RUN_EVERY_MINS = 60 					# every 1 hours

	schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
	code = 'api.my_cron_job'    				# a unique code

	def do(self):
		print(BookerViews().delete_expire_tickets())	# Calling function of Booker app to delete all expired tickets
