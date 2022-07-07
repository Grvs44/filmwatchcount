from django.conf import settings
from django.forms import ValidationError
from django.forms import DateInput
from django.db.models import *
DateInput.input_type = "date"
class FilmGroup(Model):
    User = ForeignKey(settings.AUTH_USER_MODEL,on_delete=CASCADE)
    FilmGroup = ForeignKey("FilmGroup",on_delete=SET_NULL,null=True,blank=True,verbose_name="Film group")
    Name = CharField(max_length=50,blank=False)
    def __str__(self):
        if self.FilmGroup == None: return self.Name
        else: return self.Name + " (" + self.FilmGroup.Name + ")"
    def clean(self):
        if self.FilmGroup == self: raise ValidationError("A film group's film group can't be itself")
        super().clean()
class Film(Model):
    User = ForeignKey(settings.AUTH_USER_MODEL,on_delete=CASCADE)
    FilmGroup = ForeignKey(FilmGroup,on_delete=SET_NULL,null=True,blank=True,verbose_name="Film group")
    Name = CharField(max_length=70,blank=False)
    def __str__(self):
        if self.FilmGroup == None: return self.Name
        else: return self.Name + " (" + self.FilmGroup.Name + ")"
class FilmWatch(Model):
    User = ForeignKey(settings.AUTH_USER_MODEL,on_delete=CASCADE)
    Film = ForeignKey(Film,on_delete=CASCADE)
    DateWatched = DateField("Date watched")
    Notes = TextField()
    def __str__(self): return str(self.Film) + " on " + self.DateWatched.strftime("%Y/%m/%d")
    class Meta:
        verbose_name_plural="Film watches"