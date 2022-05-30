# THIS FILE IS AUTOGENERATED
# The template can be found in tools/hektemplate.py
# Unless you are editing the template, DO NOT EDIT THIS FILE.
# ALL CHANGES WILL BE LOST THE NEXT TIME IT IS GENERATED FROM THE TEMPLATE.

"""
Attributes that can be used to construct HEK queries. They are different to
the VSO ones in that a lot of them are wrappers that conveniently expose
the comparisons by overloading Python operators. So, e.g., you are able
to say AR & AR.NumSpots < 5 to find all active regions with less than 5 spots.
As with the VSO query, you can use the fundamental logic operators AND and OR
to construct queries of almost arbitrary complexity. Note that complex queries
result in multiple requests to the server which might make them less efficient.
"""

from sunpy.net import attr as _attr
from sunpy.net import attrs as _attrs
from sunpy.time import parse_time as _parse_time

# Due to the fact this file is autogenereted it doesn't have an __all__, so all
# not _ prefixed variables must be parseable by automodapi


def _makeinstance(f):
    """
    A decorator which converts a class object to a class instance.
    """
    return f()


class HEKAttr(_attr.AttrComparison):
    """
    This ensures the attr inspect magic works for registering in the client.
    """


class HEKComparisonParamAttrWrapper:
    def __init__(self, name):
        self.name = name

    def __lt__(self, other):
        return HEKAttr(self.name, '<', other)

    def __le__(self, other):
        return HEKAttr(self.name, '<=', other)

    def __gt__(self, other):
        return HEKAttr(self.name, '>', other)

    def __ge__(self, other):
        return HEKAttr(self.name, '>=', other)

    def __eq__(self, other):
        return HEKAttr(self.name, '=', other)

    def __ne__(self, other):
        return HEKAttr(self.name, '!=', other)

    def collides(self, other):
        return isinstance(other, HEKComparisonParamAttrWrapper)


class Time(_attrs.Time):
    f"""
    `sunpy.net.hek.attrs.Time` is deprecated, please use `sunpy.net.attrs.Time`

    {_attrs.Time.__doc__}
    """

    def __init__(self, *args, **kwargs):
        # Do this here to not clutter the namespace
        from sunpy.util.exceptions import SunpyDeprecationWarning, _warn

        name = type(self).__name__
        _warn(f"`sunpy.net.hek.attrs.{name}` is deprecated, please use `sunpy.net.attrs.{name}`",
              SunpyDeprecationWarning)
        super().__init__(*args, **kwargs)


class EventType(_attr.Attr):
    def __init__(self, item):
        super().__init__()
        self.item = item

    def collides(self, other):
        return isinstance(other, EventType)

    def __or__(self, other):
        if isinstance(other, EventType):
            return EventType(self.item + ',' + other.item)
        else:
            return super().__or__(other)


class SpatialRegion(_attr.Attr):
    def __init__(self, x1=-5000, y1=-5000, x2=5000, y2=5000,
                 sys='helioprojective'):
        super().__init__()

        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.sys = sys

    def collides(self, other):
        return isinstance(other, SpatialRegion)

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return vars(self) == vars(other)

    def __hash__(self):
        return hash(tuple(vars(self).items()))


class Contains(_attr.Attr):
    def __init__(self, *types):
        super().__init__()
        self.types = types

    def collides(self, other):
        return False

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return vars(self) == vars(other)

    def __hash__(self):
        return hash(tuple(vars(self).items()))


class _StringParamAttrWrapper(HEKComparisonParamAttrWrapper):
    def like(self, other):
        return HEKAttr(self.name, 'like', other)


# The walker is what traverses the attribute tree and converts it to a format
# that is understood by the server we are querying. The HEK walker builds up
# a dictionary of GET parameters to be sent to the server.
walker = _attr.AttrWalker()


@walker.add_applier(Contains)
def _a(wlk, root, state, dct):
    dct['type'] = 'contains'
    if Contains not in state:
        state[Contains] = 1

    nid = state[Contains]
    n = 0
    for n, type_ in enumerate(root.types):
        dct[f'event_type{nid + n:d}'] = type_
    state[Contains] += n
    return dct


@walker.add_creator(
    _attrs.Time, SpatialRegion, EventType, HEKAttr, _attr.AttrAnd, Contains)
def _c(wlk, root, state):
    value = {}
    wlk.apply(root, state, value)
    return [value]


@walker.add_applier(_attrs.Time)
def _a(wlk, root, state, dct):
    dct['event_starttime'] = _parse_time(root.start).strftime('%Y-%m-%dT%H:%M:%S')
    dct['event_endtime'] = _parse_time(root.end).strftime('%Y-%m-%dT%H:%M:%S')
    return dct


@walker.add_applier(SpatialRegion)
def _a(wlk, root, state, dct):
    dct['x1'] = root.x1
    dct['y1'] = root.y1
    dct['x2'] = root.x2
    dct['y2'] = root.y2
    dct['event_coordsys'] = root.sys
    return dct


@walker.add_applier(EventType)
def _a(wlk, root, state, dct):
    if dct.get('type', None) == 'contains':
        raise ValueError
    dct['event_type'] = root.item
    return dct


@walker.add_applier(HEKAttr)
def _a(wlk, root, state, dct):
    if HEKAttr not in state:
        state[HEKAttr] = 0
    nid = state[HEKAttr]
    dct[f'param{nid:d}'] = root.name
    dct[f'operator{nid:d}'] = root.operator
    dct[f'value{nid:d}'] = root.value
    state[HEKAttr] += 1
    return dct


@walker.add_applier(_attr.AttrAnd)
def _a(wlk, root, state, dct):
    for attribute in root.attrs:
        wlk.apply(attribute, state, dct)


@walker.add_creator(_attr.AttrOr)
def _c(wlk, root, state):
    blocks = []
    for attribute in root.attrs:
        blocks.extend(wlk.create(attribute, state))
    return blocks
