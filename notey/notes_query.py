from __init__ import login_manager, db
from cruddy.model import Notes
from flask_login import current_user, login_user, logout_user


# this is method called by frontend, it has been randomized between Alchemy and Native SQL for fun
def notes_all():
    """  May have some problems with sql in deployment
    if random.randint(0, 1) == 0:
        table = users_all_alc()
    else:
        table = users_all_sql()
    return table
    """

    return notes_all_alc()


# SQLAlchemy extract all users from database
def notes_all_alc():
    table = Notes.query.all()
    json_ready = [peep.read() for peep in table]
    return json_ready


# Native SQL extract all users from database
def notes_all_sql():
    table = db.session.execute('select * from notes')
    json_ready = sqlquery_2_list(table)
    return json_ready


# ALGORITHM to convert the results of an SQL Query to a JSON ready format in Python
def sqlquery_2_list(rows):
    out_list = []
    keys = rows.keys()  # "Keys" are the columns of the sql query
    for values in rows:  # "Values" are rows within the SQL database
        row_dictionary = {}
        for i in range(len(keys)):  # This loop lines up K, V pairs, same as JSON style
            row_dictionary[keys[i]] = values[i]
        row_dictionary["query"] = "by_sql"  # This is for fun a little watermark
        out_list.append(row_dictionary)  # Finally we have a out_list row
    return out_list


# SQLAlchemy extract users from database matching term
def notes_ilike(term):
    """filter Users table by term into JSON list (ordered by User.name)"""
    term = "%{}%".format(term)  # "ilike" is case insensitive and requires wrapped  %term%
    table = Notes.query.order_by(Notes.name).filter((Notes.name.ilike(term)) | (Notes.email.ilike(term)))
    return [peep.read() for peep in table]


# SQLAlchemy extract single user from database matching ID
def notes_by_id(noteid):
    """finds User in table matching userid """
    return Notes.query.filter_by(id=noteid).first()
