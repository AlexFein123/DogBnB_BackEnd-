from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
	ROLE_CHOICES = (
		("tutor", "Tutor"),
		("host", "Host"),
	)
	HOST_STATUS = (
		("none", "None"),
		("pending", "Pending"),
		("active", "Active"),
		("rejected", "Rejected"),
	)

	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
	roles = models.JSONField(default=list)  # e.g., ["tutor"], ["tutor","host"]
	host_status = models.CharField(max_length=12, choices=HOST_STATUS, default="none")
	active_role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="tutor")

	def ensure_role(self, role: str):
		if role not in (self.roles or []):
			self.roles = [*(self.roles or []), role]
			self.save(update_fields=["roles"])


class Reservation(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reservations")
	stay_slug = models.CharField(max_length=120)
	check_in = models.DateField()
	check_out = models.DateField()
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ["-created_at"]
