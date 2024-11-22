from django.db import models

# Create your models here.

class AccountOwner(models.Model):
    '''A person who owns zero to many bank accounts'''

    name = models.CharField(max_length=120)
    ssn = models.CharField(max_length=9)

    def __str__(self):
        return self.name
    
    def get_accounts(self):
        return BankAccount.objects.filter(owner=self)
    
class BankAccount(models.Model):

    number = models.IntegerField()
    balance = models.FloatField()
    owner = models.ForeignKey(AccountOwner, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.number} ({self.owner})'
    

# courses and students

class Course(models.Model):

    number = models.CharField(max_length=12)
    name = models.CharField(max_length=120)
    # students = models.ManyToManyField('Student')

    def __str__(self):
        return f'{self.number}: {self.name}'
    
class Student(models.Model):

    name = models.CharField(max_length=120)
    # courses = models.ManyToManyField('Course')

    def __str__(self):
        return self.name
    
class Registration(models.Model):
    '''Represent the many-to-many relationship between students and courses
    as two one to many relationships: one Course to many studnets;
    one student to many courses'''

    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    reg_date = models.DateField(auto_now_add=True)
    grade = models.CharField(max_length=2)

    def __str__(self):

        return f'{self.course.number}, {self.student.name}'
    

# geneology example

class Person(models.Model):
    
    name = models.CharField(max_length=120)
    mother = models.ForeignKey('Person', 
                               related_name='mother_person', 
                               null=True, # for the 
                               blank=True, #for the model form definition
                               on_delete=models.CASCADE)
    father = models.ForeignKey('Person', 
                               related_name='father_person', 
                               null=True,
                               blank=True,
                               on_delete=models.CASCADE)
    
    def __str__(self):
        if self.father and self.mother:
            return f'{self.name}, child of {self.father.name} and {self.mother.name}'
        if self.father:
            return f'{self.name}, child of {self.father.name}'
        if self.mother:
            return f'{self.name}, child of {self.mother.name}'
        return f'{self.name}'