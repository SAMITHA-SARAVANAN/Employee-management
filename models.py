from django.db import models


class Employee(models.Model): 
    empnumber = models.IntegerField(unique=True)
    empname = models.CharField(max_length=50)
    empmail =models.EmailField(max_length=50)
    empcity =models.CharField(max_length=100)

    def __str__(self):
        return f"Employee:{self.empnumber} - {self.empmail}"

class Notification(models.Model):
    employee = models.ForeignKey('Employee', on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.employee.empname}: {self.message}"
