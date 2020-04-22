import api


print(api.get_events_of_the_day('msk'))
print(api.get_specification(187576))
print(api.get_coords(12271))
events = api.get_events('msk', 0, 37.623026, 55.751557, 1000)
print(events)
print(api.get_next(events['next']))