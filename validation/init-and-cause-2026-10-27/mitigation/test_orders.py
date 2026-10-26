import copy
import json
from pathlib import Path
import unittest

from app import list_orders, receive


class ListMitigationTests(unittest.TestCase):
    def test_original_input_through_app_keeps_raw_export_source(self):
        events = json.loads(Path(__file__).with_name("events.json").read_text())
        store = []
        for event in events:
            receive(store, event)
        raw_export = json.dumps(store)
        self.assertEqual(list_orders(store), [events[0], events[2]])
        self.assertEqual(store, events)
        self.assertEqual(json.dumps(store), raw_export)
        self.assertEqual(len(store), 3)

    def test_distinct_events_with_equal_amount_and_nonadjacent_repeat(self):
        first = {"event_id": "a", "order_id": "o1", "amount": 10}
        second = {"event_id": "b", "order_id": "o2", "amount": 10}
        store = [first, second, dict(first)]
        self.assertEqual(list_orders(store), [first, second])
        result = list_orders(store)
        result[0]["amount"] = 99
        self.assertEqual(store[0]["amount"], 10)

    def test_unknown_history_is_preserved_and_empty_input_works(self):
        store = [{"amount": 10}, {"amount": 10},
                 {"event_id": None}, {"event_id": None},
                 {"event_id": ""}, {"event_id": ""}]
        before = copy.deepcopy(store)
        self.assertEqual(list_orders(store), before)
        self.assertEqual(store, before)
        self.assertEqual(list_orders([]), [])


if __name__ == "__main__":
    unittest.main()
