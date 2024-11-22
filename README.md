"# lets-go-tango" 
Was used by Free Django Template "Material Kit 2"

Tango community page where you can share your tango occupations, 
your tango activities and leave feedback on other community members' tango classes.

1. python manage.py migrate
2. python manage.py createsuperuser
3. python manage.py runserver & Open Home page, Sign in with superuser data

4. Open page "People"
5. Add the first occupation to sidebar "All members" button "New":
  - name - "Tanguero" (the name must match exactly because this is Tangueros page)
  - description - "I dance tango or learn it"  (here you can show your imagination)
6. You see only one member here is you ("Me"), you have the ability to change your data, 
add the necessary information (the same can be done on the admin page)
7. You can also add as many "occupations" as need. For example: 
  - Teacher - I teach tango, give group or private lessons
  - Organizer - I organize various tango events
  - Tango DJ  - I provide musical accompaniment for Tango events
  - Dancer - I dance professionally, participate in tango shows or dance in tango theater
  - Photographer - I make photo reports of tango events or private tango session
  - etc.
8. The members themselves can also add "occupations". This feature is available to all members.
9. Now you can add your occupations in your details, if necessary. Each member can adjust their own details.
10. In the members list there is also an "+add" of a new member, this is only available if you are is_staff or is_superuser
11. The members page also has a search by member's last name or selection by occupation (from sidebar)

12. Open page "Activity"
13. Add the categories de Tango activities to sidebar "All activities" button "New". 
    You can add as many "categories" as need. For example: 
 - Milonga - Milonga is an event where Argentine tango is danced. The venue dedicated to milongas may also be called "milonga".
 - Lesson - Tango lesson. Can be in a group of 4 or more people or private for 1-2
 - Show - This is a tango theatre or a performance by professional tango dancers.
 - Practice - This is a place where you can dance tango, usually after a group tango lesson.
 - etc.
14. The members themselves can also add "categories". This feature is available to all members.
15. Creating a new tango activity is available to all members. 
   But tango activity must have a place where the event will take place, so the following page...

16. Open page "Places"
17. Add new Tango Place button "New". We select a "city" from the list, and if not, we indicate a "new city". For example: 
  - name: Club La Paila, city: Buenos Aires, direction: Costa Rica 4824
  - etc.
18. In sidebar in the future we will be able to select places by city.
19. When viewing a place in detail you see all the tango activities in this place 
   with links to more details about these activities.
20. Now you can add new tango activity in this tango place on the page Activity
21. The one who adds new activity is the possessor of this activity automatically
22. Add new activity. For example:
   name: Milonga "Del Sur", category: Milonga (select), location: Club La Paila (select), 
   day: (select day of week), start_time: time begin, end_time: time finish, price: (in $), notes: (any additional information)
23. You can edit and delete activities that you are the owner of.
24. Also on the detailed information page about the activity all members can leave their opinion, feedback about this activity
25. Now on the details page about you, you see all your activities, with links to their details where you can edit them

26. On the page list-activities there is a selection by day of week of activities, sorted by the start time of the activity.
27. All sidebars have statistics figures by sections:
 - How many members from each occupation
 - How many Tango activities are  in each category
 - How many Tango activities are in each city
28. All -list pages have a pagination, including pages after selecting lists by criteria

29. Links to all the above pages are in the top panel, where there is also a "Logout"

