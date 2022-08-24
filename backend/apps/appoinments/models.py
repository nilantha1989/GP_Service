
from django.db import models
from users import User
from django.utils.translation import gettext_lazy as _

class TreatmentType(models.TextChoices):
    VIDEOASSESSMENT = 'VIDEOASSESSMENT', _('VIDEOASSESSMENT')
    FORMASSESSMENT = 'FORMASSESSMENT', _('FORMASSESSMENT')


class Pharmacy(models.Model):
    pharmacy_name=models.CharField(max_lenght=255)
    postal_code=models.CharField(max_lenght=255)

class AppointmentAndAvailability(models.Model):
    doctor=models.ForeignKey('User',on_delete=models.PROTECT)
    date_and_time=models.DateTimeField
    treatment_type=models.CharField(
        max_length=20,
        choices=TreatmentType.choices
   )
    patient=models.ForeignKey('User',on_delete=models.PROTECT)
    is_booked=models.BooleanField
    consult_copy_shared=models.BooleanField
    prefered_pharmacy=models.ForeignKey(Pharmacy,on_delete=models.PROTECT) 
    can_access_SCR=models.BooleanField

class FormTreatmentType(models.TextChoices):
    ONETIMEFORM = 'ONETIMEFORM', _('ONETIMEFORM')
    SUBSCRIPTIONFORM = 'SUBSCRIPTIONFORM', _('SUBSCRIPTIONFORM')

class CreateFormOrder(models.Model):
    form_treatment_type=models.CharField(
        max_length=20,
        choices=FormTreatmentType.choices
   )
    is_active=models.BooleanField
    patient=models.ForeignKey('User',on_delete=models.PROTECT)
    doctor=models.ForeignKey('User',on_delete=models.PROTECT)
    is_picked_by_doctor=models.BooleanField
    subs_start_date=models.DateField
    subs_end_date=models.DateField
    prefered_pharmacy=models.ForeignKey(Pharmacy,on_delete=models.PROTECT) 

class FormAssessementQuestioner(models.Model):
    question=models.TextField()
    answer=models.TextField()
    form=models.ForeignKey(CreateFormOrder,on_delete=models.PROTECT)

class Prescription(models.Model):
    issued_datetime=models.DateTimeField()
    appoinment=models.OneToOneField(AppointmentAndAvailability,on_delete=models.PROTECT,primary_key=True,blank=True)
    form_assement=models.OneToOneField(CreateFormOrder,on_delete=models.PROTECT,primary_key=True,blank=True)
    is_accept_by_pharmacy=models.BooleanField
    is_accept_by_patient=models.BooleanField
    is_prapared=models.BooleanField
    doctor=models.ForeignKey('User',on_delete=models.PROTECT,blank=True)
    patient=models.ForeignKey('User',on_delete=models.PROTECT,blank=True)
    pharmacy=models.ForeignKey(Pharmacy,on_delete=models.PROTECT,blank=True)


class Drug(models.Model):
    drug_name=models.CharField(max_lenght=255)
    strength=models.CharField(max_lenght=25)
    availability=models.BooleanField
    
class PrescriptionDrug(models.Model):
    drug=models.ForeignKey(Drug,on_delete=models.PROTECT,blank=True)
    prescription=models.ForeignKey(Prescription,on_delete=models.PROTECT,blank=True)

    class Meta:
        unique_together=[['drug','prescription']]
