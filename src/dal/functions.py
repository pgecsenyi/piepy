"""
Common functions and utilities to be used by other modules.
"""

def build_result_dictionary(cursor, keys):
    """
    Builds a list from the given 'cursor' object where every item is a dictionary. The result looks like the
    following example.

        [{'id' : 1, 'path' : '/home/jsmith/image/01.jpg'},
         {'id' : 2, 'path' : '/home/jsmith/image/02.jpg'}]

    Parameters
    ----------
    cursor : Cursor
        The database cursor that can be used to fetch the result set.
    keys : list of str
        The list of the keys in the returned dictionaries.

    Returns
    -------
    A list of dictionaries containing values by the given keys.
    """

    result = []

    # Fetch result.
    rows = cursor.fetchall()
    if rows is None or not rows:
        return result
    if len(rows[0]) != len(keys):
        raise Exception('Number of columns and key names differ.')

    # Build result list.
    for row in rows:
        item = {}
        # pylint: disable=consider-using-enumerate
        for i in range(0, len(keys)):
            item[keys[i]] = row[i]
        result.append(item)

    return result
