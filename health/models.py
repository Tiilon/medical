from random import randrange
from django.db import models
from django.conf import settings
from django.utils import timezone

from user.models import UserProfile

# Create your models here.
def generate():
    FROM = '0123456789'
    LENGTH = 10
    pat_id = ""
    for i in range(LENGTH):
        pat_id += FROM[randrange(0, len(FROM))]

    return f"PT{pat_id}/{timezone.now().year}"


GENDER = {
    ('Male', 'Male'),
    ('Female', 'Female'),
}

COMPLAINTS_STATUS = {
    ('Pending', 'Pending'),
    ('Resolved', 'Resolved'),
    ('Canceled', 'Canceled'),

}

TREATMENT_STATUS = {
    ('Pending', 'Pending'),
    ('Canceled','Canceled'),
    ('Completed', 'Completed'),
}

PRE_STATUS = {
  (1, 'Confirmed'),
  (0, 'Pending'),

}


class Patient(models.Model):
    patient_id = models.CharField(max_length=100,blank=True,null=True,default=generate())
    profile = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, related_name='patient_profile', blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='patients', blank=True, null=True)

    def __str__(self):
        return self.patient_id

    def full_name(self):
        return f"{self.profile.first_name} {self.profile.last_name}"

    class Meta:
        db_table = 'patient'

class Complaints(models.Model):
    complaints = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='complaints', blank=False, null=True)
    review = models.CharField(max_length=3000, blank=True, null=True)
    is_seen = models.BooleanField(blank=True, null=True, default=False)
    seen_at = models.DateTimeField(blank=True, null=True)
    seen_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='complaint_seen', blank=False, null=True)
    status = models.CharField(max_length=200, blank=True, null=True, choices=COMPLAINTS_STATUS)
    review_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='complaint_review',blank=False, null=True)
    review_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ('-created_at',)
        db_table = 'complaint'

    def __str__(self):
        return str(self.complaints)

class VitalSign(models.Model):
    patient = models.ForeignKey('Patient', on_delete=models.SET_NULL, blank=True, null=True, related_name='vital_sign_patient')
    time = models.TimeField(default=timezone.now)
    weight = models.DecimalField( max_digits=10, decimal_places=2,blank=True, null=True)
    diastolic = models.IntegerField( blank=True, null=True)
    pulse = models.IntegerField(blank=True, null=True)
    systolic = models.IntegerField( blank=True, null=True)
    respiration = models.IntegerField( blank=True, null=True)
    temperature = models.DecimalField( max_digits=10, decimal_places=2,blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True, related_name='vital_signs')

    class Meta:
        db_table = 'vital_sign'
        ordering = ('-time',)

    def __str__(self):
        return f"{self.patient.full_name()}-{self.time}"

class MedicalDiagnosis(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.SET_NULL, related_name='diagnosis_patient', blank=True, null=True)
    complaints = models.CharField(max_length=1000, blank=True, null=True)
    symptoms = models.CharField(max_length=2000, blank=True, null=True)
    diagnosis = models.CharField(max_length=100,blank=True, null=True)
    is_admitted = models.BooleanField(blank=True,null=True)
    onset = models.CharField(max_length=100, blank=True, null=True)
    treatments = models.ManyToManyField('Treatment', related_name='diagnosis_treatments', blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='diagnosis', blank=True, null=True)

    def __str__(self):
        return self.diagnosis

    class Meta:
        db_table= 'medical diagnosis'
        ordering = ('-created_at',)

class Treatment(models.Model):
    diagnosis = models.ForeignKey(MedicalDiagnosis, on_delete=models.SET_NULL, related_name='treatment_diagnosis', blank='null', null=True)
    treatment = models.CharField(max_length=2000, blank=True, null=True)
    prescription = models.CharField(max_length=2000, blank=True,null=True)
    pharmacy_prescription = models.ForeignKey('Prescription', on_delete= models.SET_NULL, related_name='treatment_prescription', blank=True, null=True)
    status = models.CharField(max_length=100,blank=True,null=True, choices= TREATMENT_STATUS)
    time_treated = models.TimeField(blank=True, null=True)
    date_treated= models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='treatments',blank=True, null=True)

    def __str__(self):
        return str(self.treatment) + ' - ' + str(self.prescription)

    class Meta:
        db_table = 'treatment'
        ordering = ('-created_at',)

    
class Note(models.Model):
    note = models.TextField(max_length=3000, blank=True, null=True)
    treatment = models.ForeignKey(Treatment, on_delete=models.SET_NULL, related_name='treatment_note', blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='notes', blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.note)

    class Meta:
        db_table = 'note'
        ordering = ('-created_at',)

class PrescribedMedicine(models.Model):
    name = models.CharField(max_length=2000, blank=True, null=True)
    prescription = models.ForeignKey('Prescription', on_delete=models.SET_NULL, related_name='prescribed_medicine_prescribed',blank=True, null=True)
    dosage = models.CharField(max_length=2000, blank=True, null=True)
    frequency = models.CharField(max_length=200, blank=True, null=True)
    quantity = models.IntegerField(blank=True, null=True)
    amount = models.DecimalField(max_digits=10,decimal_places=2, blank=True,null=True)
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='prescribed_medicines', blank=True, null=True)

    def __str__(self):
        return str(self.name)

    class Meta:
        db_table ='prescibed_medicine'


class Prescription(models.Model):
    prescription_id = models.CharField(max_length=200,blank=True,null=True)
    medicines = models.ManyToManyField(PrescribedMedicine, related_name='prescription_medicine', blank=True)
    patient = models.ForeignKey('Patient', on_delete=models.SET_NULL, related_name='prescription_patient', blank=True,null=True)
    treatment = models.ForeignKey('Treatment',on_delete=models.SET_NULL, related_name='prescription_treatment', blank=True,null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    is_paid = models.BooleanField(default=False, blank=True, null=True)
    status = models.IntegerField(blank=True, null=True, choices=PRE_STATUS)
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='prescriptions', blank=True, null=True)

    def __str__(self):
        return str(self.patient.full_name())

    class Meta:
        db_table = 'prescription'


