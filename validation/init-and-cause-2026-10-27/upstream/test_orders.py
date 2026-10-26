import json
from pathlib import Path
import unittest

from app import receive, list_orders


class OrderReceiptTests(unittest.TestCase):
    def test_original_events_and_replay_keep_raw_and_list_unique(self):
        events = json.loads(Path(__file__).with_name("events.json").read_text())
        store = []
        for event in events:
            receive(store, event)
        expected = [events[0], events[2]]
        self.assertEqual(store, expected)
        self.assertEqual(list_orders(store), expected)
        for event in events:
            receive(store, event)
        self.assertEqual(store, expected)
        self.assertEqual(list_orders(store), expected)

    def test_equal_amount_different_orders_are_preserved(self):
        store = []
        for event in [
            {"event_id": "a", "order_id": "x", "amount": 10},
            {"event_id": "b", "order_id": "y", "amount": 10},
        ]:
            receive(store, event)
        self.assertEqual(len(store), 2)

    def test_existing_event_is_not_inserted_again(self):
        event = {"event_id": "e1", "order_id": "o1", "amount": 10}
        store = [dict(event)]
        receive(store, event)
        self.assertEqual(store, [event])

    def test_unknown_history_and_existing_duplicates_are_untouched(self):
        historical = [{"order_id": "legacy", "amount": 10}] * 2
        event = {"event_id": "e1", "order_id": "o1", "amount": 10}
        store = historical + [dict(event), dict(event)]
        before = [dict(row) for row in store]
        receive(store, event)
        self.assertEqual(store, before)
        self.assertEqual(list_orders(store), before)

    def test_input_and_list_copy_behavior_is_preserved(self):
        event = {"event_id": "e1", "order_id": "o1", "amount": 10}
        store = []
        receive(store, event)
        event["amount"] = 20
        visible = list_orders(store)
        visible[0]["amount"] = 30
        self.assertEqual(store[0]["amount"], 10)


if __name__ == "__main__":
    unittest.main()
