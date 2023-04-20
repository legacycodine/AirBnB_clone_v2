#!/usr/bin/python3
""" Write a fabric script that generates a .tgz archive
from the contents of the web_static folder in the AirBnB repo and lists all files"""
from datetime import datetime
from fabric.api import local
import os


def do_pack():
    """Creates a gzipped tar archive from the web_static/ content"""
    try:
        if not os.path.exists("versions"):
            local('mkdir versions')
        now = datetime.utcnow()
        ft = now.strftime("%Y%m%d%H%M%S")
        archive_path = "versions/web_static_{}.tgz".format(ft)
        local("tar -cvzf {}  web_static/".format(archive_path))
        return archive_path
    except Exception as e:
        print("An exception occurred: {}".format(e))
        return None
