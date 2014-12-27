import enum

class ChangeType(enum.Enum):
    ADDED = 0, 
    DELETED = 1, 
    CHANGED = 2


def get_events(data):
    days = data['schedule']['conference']['days']
    events = {}
    for day in days:
        pass
        rooms = day['rooms']
        #print(rooms.keys())
        for room in rooms.keys():
            #print(room)
            event_list = rooms[room]
            for e in event_list:
                events[e['id']] = e
    return events


def get_version(data):
    return data['schedule']['version']


def diff_events(old, new):
    result = []
    old_set = set(old.keys())
    new_set = set(new.keys())
    add = new_set.difference(old_set)
    rem = old_set.difference(new_set)
    change = old_set.intersection(new_set)
    
    for i in add:
        result.append( (ChangeType.ADDED, new[i]) )
    for j in rem:
        result.appen( (ChangeType.REMOVED, old[j]) )
    for k in change:
        if new[k]['title'] != old[k]['title'] or new[k]['start'] != old[k]['start'] or new[k]['date'] != old[k]['date'] :
               result.append( (ChangeType.CHANGED, new[k], old[k]) )
    return result


