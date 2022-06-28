from django.db.models import *
from django.conf import settings
class FilmGroup(Model):
    User = ForeignKey(settings.AUTH_USER_MODEL,on_delete=CASCADE)
    FilmGroup = ForeignKey("FilmGroup",on_delete=SET_NULL,null=True)
    Name = CharField(max_length=30,blank=False)
    def __str__(self): return self.Name
class Film(Model):
    User = ForeignKey(settings.AUTH_USER_MODEL,on_delete=CASCADE)
    FilmGroup = ForeignKey(FilmGroup,on_delete=SET_NULL,null=True)
    Name = CharField(max_length=30,blank=False)
    def __str__(self): return self.Name + " (" + self.FilmGroup.Name + ")"
class FilmWatch(Model):
    User = ForeignKey(settings.AUTH_USER_MODEL,on_delete=CASCADE)
    Film = ForeignKey(Film,on_delete=CASCADE)
    DateWatched = DateField()
    Notes = TextField()
    def __str__(self): return str(self.Film) + " on " + self.DateWatched.strftime("%Y/%m/%d")