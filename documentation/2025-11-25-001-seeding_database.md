I am trying to figure out how we do mock data seeding in django

i am going to try out a bunch of different ways of seeding the database
there is bunch of different method of doing it and am going to try out all of them to get a feel for what each of them can do

here are the methods
1. raw sql (using sql lite)
2. raw python script
3. django shell script
4. django fixtures
5. django management command
6. django management with faker

from these i think ill be able to pick out the best one to adopt as my go to


for starters, clearing the database in django is
this will clear out the entire database
python manage.py flush
uv run manage.py flush


