"""A database encapsulating collections of NEOs and their close approaches.

A `NEODatabase` holds an interconnected data set of NEOs and close approaches.
It provides methods to fetch an NEO by primary designation or by name, as well
as a method to query the set of close approaches that match a collection of
user-specified criteria.

Under normal circumstances, the main module creates one NEODatabase from the
data on NEOs and close approaches extracted by `extract.load_neos` and
`extract.load_approaches`.

You'll edit this file in Tasks 2 and 3.
"""
import random


class NEODatabase:
    """A database of near-Earth objects and their close approaches.

    A `NEODatabase` contains a collection of NEOs and a collection of close
    approaches. It additionally maintains a few auxiliary data structures to
    help fetch NEOs by primary designation or by name and to help speed up
    querying for close approaches that match criteria.
    """

    def __init__(self, neos, approaches):
        """Create a new `NEODatabase`.

        As a precondition,this constructor assumes that the collections of NEOs
        and close approaches haven't yet been linked - that is, the
        `.approaches` attribute of each `NearEarthObject` resolves to an empty
        collection, and the `.neo` attribute of each `CloseApproach` is None.

        However, each `CloseApproach` has an attribute (`._designation`) that
        matches the `.designation` attribute of the corresponding NEO. This
        constructor modifiesthe supplied NEOs and close approaches to link them
        together - after it's done, the `.approaches` attribute of each NEO has
        a collection of that NEO's close approaches,and the `.neo` attribute of
        each close approach references the appropriate NEO.

        :param neos: A collection of `NearEarthObject`s.
        :param approaches: A collection of `CloseApproach`es.
        """
        self._neos = neos
        self._approaches = approaches

        self.des_neo_dict = {}
        for n in neos:
            self.des_neo_dict[n.designation] = n
        self.name_neo_dict = {}
        for i in neos:
            if ((i.name is None) or (len(i.name) == 0)):
                continue
            self.name_neo_dict.setdefault(i.name, []).append(i)
        for appr in approaches:
            appr.neo = self.des_neo_dict[appr._designation]
            obj_neo = appr.neo
            obj_neo.approaches.append(appr)

    def get_neo_by_designation(self, designation):
        """Find and return an NEO by its primary designation.

        If no match is found, return `None` instead.

        Each NEO in the data set has a unique primary designation, as a string.

        The matching is exact - check for spelling and capitalization if no
        match is found.

        :param designation: The primary designation of the NEO to search for.
        :return: The `NearEarthObject` with the desired primary
        designation, or `None`.
        """
        if designation in self.des_neo_dict.keys():
            return self.des_neo_dict[designation]
        else:
            return None

    def get_neo_by_name(self, name):
        """Find and return an NEO by its name.

        If no match is found, return `None` instead.

        Not every NEO in the data set has a name. No NEOs are associated with
        the empty string nor with the `None` singleton.

        The matching is exact - check for spelling and capitalization if no
        match is found.

        :param name: The name, as a string, of the NEO to search for.
        :return: The `NearEarthObject` with the desired name, or `None`.
        """
        if not ((name is None) or (len(name) == 0)):
            if name in self.name_neo_dict.keys():
                if (len(self.name_neo_dict[name]) > 1):
                    return_obj = self.name_neo_dict[name][0]
                    return return_obj
                else:
                    return_obj = self.name_neo_dict[name][0]
                    return return_obj
        return None

    def query(self, filters=()):
        """Query close approaches using a collection of filters.

        This generates stream of `CloseApproach` objects that match all of the
        provided filters.

        If no arguments are provided, generate all known close approaches.

        The `CloseApproach` objects are generated in internal order,which isn't
        guaranteed to be sorted meaningfully, although is often sorted by time.

        :param filters: A collection of filters capturing user-specified
        criteria.
        :return: A stream of matching `CloseApproach` objects.
        """
        for approach in self._approaches:
            if (len(filters) == 0):
                yield approach
            else:
                appr_status = []
                for i in filters:
                    status = i(approach)
                    appr_status.append(status)
                if (set(appr_status) == {True}):
                    yield approach
