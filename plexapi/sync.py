# -*- coding: utf-8 -*-

import requests
from plexapi import utils
from plexapi.exceptions import NotFound


class SyncItem(object):
    """Summary

    Attributes:
        device (TYPE): Description
        id (TYPE): Description
        location (TYPE): Description
        machineIdentifier (TYPE): Description
        MediaSettings (TYPE): Description
        metadataType (TYPE): Description
        policy (TYPE): Description
        rootTitle (TYPE): Description
        servers (TYPE): Description
        status (TYPE): Description
        title (TYPE): Description
        version (TYPE): Description
    """
    def __init__(self, device, data, servers=None):
        """Summary

        Args:
            device (TYPE): Description
            data (TYPE): Description
            servers (None, optional): Description
        """
        self.device = device
        self.servers = servers
        self.id = utils.cast(int, data.attrib.get('id'))
        self.version = utils.cast(int, data.attrib.get('version'))
        self.rootTitle = data.attrib.get('rootTitle')
        self.title = data.attrib.get('title')
        self.metadataType = data.attrib.get('metadataType')
        self.machineIdentifier = data.find('Server').get('machineIdentifier')
        self.status = data.find('Status').attrib.copy()
        self.MediaSettings = data.find('MediaSettings').attrib.copy()
        self.policy = data.find('Policy').attrib.copy()
        self.location = data.find('Location').attrib.copy()

    def __repr__(self):
        """Summary

        Returns:
            TYPE: Description
        """
        return '<%s:%s>' % (self.__class__.__name__, self.id)

    def server(self):
        """Summary

        Returns:
            TYPE: Description

        Raises:
            NotFound: Description
        """
        server = list(filter(lambda x: x.machineIdentifier ==
                             self.machineIdentifier, self.servers))
        if 0 == len(server):
            raise NotFound('Unable to find server with uuid %s' %
                           self.machineIdentifier)
        return server[0]

    def getMedia(self):
        """Summary

        Returns:
            TYPE: Description
        """
        server = self.server().connect()
        items = utils.listItems(server, '/sync/items/%s' % self.id)
        return items

    def markAsDone(self, sync_id):
        """Summary

        Args:
            sync_id (TYPE): Description

        Returns:
            TYPE: Description
        """
        server = self.server().connect()
        url = '/sync/%s/%s/files/%s/downloaded' % (
            self.device.clientIdentifier, server.machineIdentifier, sync_id)
        server.query(url, method=requests.put)
