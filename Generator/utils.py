#!/usr/bin/env python
# -*- coding: utf-8 -*-
from functools import reduce
from Generator.data_structures import *


def get_from_dict(data_dict, coords, default_value=None):
    """Get element from a nested dictionary.

    Args:
        data_dict: nested dict that element should be put to
        coords: coordinates where to put the element
        default_value: return that if there is no element under that coords
    """

    def get_ignoring_zero(my_dict, key):
        if my_dict == 0:
            return 0
        else:
            return my_dict.get(key, default_value)

    return reduce(get_ignoring_zero, coords, data_dict)


def set_in_dict(data_dict, coords, el):
    """Put element into nested dictionary

    Args:
        data_dict: nested dict that element should be put to
        coords: coordinates where to put the element
        el: element to put
    """
    if len(coords) == 1:
        data_dict[coords[0]] = el
    else:
        reduce(lambda my_dict, key: my_dict.setdefault(key, {}), coords, data_dict)
        get_from_dict(data_dict, coords[:-1])[coords[-1]] = el


def nested_dict_coords_list(nested_dict, current_coord):
    """Get every possible coordinate of a nested dict."""
    return reduce(
        (lambda list, key:
         list + [current_coord + [key]] if type(nested_dict[key]) != dict
         else list + [current_coord + [key]] + nested_dict_coords_list(nested_dict[key], current_coord + [key])),
        nested_dict.keys(), []
    )


def order(el, list):
    """Get order of element: formatted to 2-decimal string."""
    list.sort()
    return str(list.index(el)).zfill(2)


def get_link(list_coords):
    """Create link from coordinate in dict."""
    retlink = BASE_LINK
    for i in range(len(list_coords)):
        elements = get_from_dict(circuit_results, list_coords[:i])
        retlink += order(list_coords[i], list(elements.keys()))
    return retlink


def update_dict(dict, key_list, val_to_add):
    prev_val = get_from_dict(dict, key_list, 0)
    set_in_dict(dict, key_list, prev_val + val_to_add)
