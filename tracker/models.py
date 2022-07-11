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
    class Meta:
        ordering = ["Name"]
class Film(Model):
    User = ForeignKey(settings.AUTH_USER_MODEL,on_delete=CASCADE)
    FilmGroup = ForeignKey(FilmGroup,on_delete=SET_NULL,null=True,blank=True,verbose_name="Film group")
    Name = CharField(max_length=70,blank=False)
    ReleaseYear = PositiveSmallIntegerField("Release year",null=True,blank=True)
    def __str__(self):
        if self.FilmGroup and self.ReleaseYear: return self.Name + " (" + str(self.ReleaseYear) + ", " + self.FilmGroup.Name + ")"
        elif self.FilmGroup: return self.Name + " (" + self.FilmGroup.Name + ")"
        elif self.ReleaseYear: return self.Name + " (" + str(self.ReleaseYear) + ")"
        else: return self.Name
    class Meta:
        ordering = ["Name","ReleaseYear"]
class FilmWatch(Model):
    User = ForeignKey(settings.AUTH_USER_MODEL,on_delete=CASCADE)
    Film = ForeignKey(Film,on_delete=CASCADE)
    DateWatched = DateField("Date watched",blank=True,null=True)
    Notes = TextField(blank=True)
    def __str__(self):
        if self.DateWatched: return str(self.Film) + " on " + self.DateWatched.strftime("%Y/%m/%d")
        else: return str(self.Film)
    class Meta:
        verbose_name_plural="Film watches"