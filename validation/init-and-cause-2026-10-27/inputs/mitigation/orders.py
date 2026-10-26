def receive(store, event):
    store.append(dict(event))

def list_orders(store):
    return [dict(row) for row in store]
