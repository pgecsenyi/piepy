def are_expected_items_in_list(test_case, actual_list, *expected_items):
    """
    Checks whether the expected items are in the given list and only those are in the list.

    Parameters
    ----------
    test_case : unittest.TestCase
        The test case that provides assert methods.
    actual_list : list of object
        The result list to check.
    expected_items : list of object
        The list of the expected items.
    """

    test_case.assertIsNotNone(actual_list, 'The list should not be None.')
    test_case.assertEqual(
        len(expected_items),
        len(actual_list),
        'There are different number of items in expected and in actual lists ({}/{}).'.format(
            len(expected_items),
            len(actual_list)))

    for item in expected_items:
        test_case.assertIn(item, actual_list, 'The item \'{}\' is missing from the list.'.format(item))

def are_expected_kv_pairs_in_list(test_case, actual_list, item_key, expected_items):
    """
    Checks whether the values for the given key in the given result list are the expected ones.

    Parameters
    ----------
    test_case : unittest.TestCase
        The test case that provides assert methods.
    actual_list : list of object
        The result list to check.
    item_key : object
        The interesting key for the items in the list.
    expected_items : list of object
        The list of the expected items.
    """

    if expected_items is None:
        test_case.assertEqual(None, actual_list, 'There are no expected items, but the actual list is not None.')
    else:
        test_case.assertNotEqual(None, actual_list, 'There are no items in the actual list.')

    test_case.assertEqual(
        len(expected_items),
        len(actual_list),
        'There are different number of items in expected and in actual lists ({}/{}).'.format(
            len(expected_items),
            len(actual_list)))

    for expected_item in expected_items:
        match = False
        for item in actual_list:
            if item[item_key] == expected_item:
                match = True
                break
        test_case.assertTrue(match, '\'{}\' is missing from the actual list.'.format(expected_item))

def get_item_from_embedded_dictionary(actual_list, search_key, search_value, return_key):

    if actual_list is None or search_key is None or search_value is None:
        return None

    for item in actual_list:
        if item[search_key] == search_value:
            return item[return_key]

    return None
