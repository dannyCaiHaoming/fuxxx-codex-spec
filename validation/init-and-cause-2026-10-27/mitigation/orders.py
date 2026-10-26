def receive(store, event):
    store.append(dict(event))

def list_orders(store):
    # Presentation-only mitigation: never change the raw store/export source.
    seen = []
    result = []
    for row in store:
        event_id = row.get("event_id")
        # Unknown historical identities cannot safely be collapsed.
        if event_id is not None and event_id != "":
            if event_id in seen:
                continue
            seen.append(event_id)
        result.append(dict(row))
    return result
