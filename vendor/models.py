from django.db import models
from accounts.models import User, UserProfile
from accounts.utils import send_notification_email  # Apnar folder/file onujayi path thik korun

# Create your models here.


class Vendor(models.Model):
    user = models.OneToOneField(User, related_name='user', on_delete=models.CASCADE)
    user_profile = models.OneToOneField(UserProfile, related_name='userprofile', on_delete=models.CASCADE)
    vendor_name = models.CharField(max_length=50)
    vendor_license = models.ImageField(upload_to='vendor/license')
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.vendor_name

    def save(self, *args, **kwargs):
        # Jodi record-ti age thekei database-e thake (update operation)
        if self.pk is not None:
            try:
                orig = Vendor.objects.get(pk=self.pk)

                # Jodi is_approved status poriborton hoy
                if orig.is_approved != self.is_approved:
                    mail_template = 'accounts/emails/admin_approval_email.html'
                    context = {
                        'user': self.user,
                        'to_email': self.user.email,
                    }

                    if self.is_approved:
                        mail_subject = 'Congratulations! Your vendor account has been approved.'
                    else:
                        mail_subject = 'We are sorry! Your vendor account has been rejected.'

                    send_notification_email(mail_subject, mail_template, context)
            except Vendor.DoesNotExist:
                pass

        super(Vendor, self).save(*args, **kwargs) 