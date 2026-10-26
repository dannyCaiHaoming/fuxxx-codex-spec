def receive(store, event):
    event_id = event["event_id"]
    if any(row.get("event_id") == event_id for row in store):
        return
    store.append(dict(event))

def list_orders(store):
    return [dict(row) for row in store]
