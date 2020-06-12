22
Parish
    - Name, address, priest
    - Attendee limit
    - Open Registration
    - Close Registration

Mass
    - Title (Default Mass)
    - Date / Time
    - Attendee limit override

Users
    - Parish admin
    - Parishioner
        - Email
        - Name
        - Address

Registration
    - Mass ID
    - Parishioner ID
    - Additional attending
    - Names of those attending

Will need to create masses every week on the same day.




#### Permission Groups
    request.User.groups.add(perm_group)
        e.g. perm-group = (parishioner, parish)
    request.User.has_perm('appname.action_model')
        e.g. dashboard.view_mass, _.add_mass, _.del_mass, _.change_mass
    'templates' use django perms
        {% if perms.myapp.can_view_something %}{% endif %}
