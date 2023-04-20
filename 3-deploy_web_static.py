#!/usr/bin/python3
""" Fabfile to distribute an archive to a web server.(deploy)
Creates and distributes an archive to your web servers
"""
from datetime import datetime
from fabric.api import *
from os import path

env.hosts = ['54.237.52.200', '34.224.62.212']
env.user = 'ubuntu'


def deploy():
    """Creates and distributes an archive to web servers.
    """
    archive_path = do_pack()
    if archive_path is None:
        return False
    return (do_deploy(archive_path))


def do_pack():
    """Creates a gzipped tar archive from the web_static/ content"""
    try:
        if not path.exists("versions"):
            local('mkdir versions')
        now = datetime.utcnow()
        ft = now.strftime("%Y%m%d%H%M%S")
        archive_path = "versions/web_static_{}.tgz".format(ft)
        local("tar -cvzf {}  web_static/".format(archive_path))
        return archive_path
    except Exception as e:
        print("An exception occurred: {}".format(e))
        return None


def do_deploy(archive_path):
    """Uploads archive to web servers, deploys to web servers.
    params:
        archive_path (str): The path of the archive to distribute.
    Returns:
        If the file doesn't exist at archive_path or an error occurs - False.
        Otherwise - True.
    """
    if not path.exists(archive_path):
        return False
    try:
        tgz_file = archive_path.split('/')[-1]
        fname = tgz_file.split('.')[0]

        # Upload the archive to /tmp/ directory on the web server
        put(archive_path, '/tmp/{}'.format(tgz_file))

        releases_path = "/data/web_static/releases/{}/".format(fname)
        run("mkdir -p {}".format(releases_path))

        # uncompress archive and delete .tgz
        run("sudo tar -xzf /tmp/{} -C {}".format(tgz_file, releases_path))
        run("sudo rm /tmp/{}".format(tgz_file))

        # Place web_static directory correctly
        run("sudo mv {}/web_static/* {}".format(releases_path, releases_path))
        run("sudo rm -rf {}web_static".format(releases_path))

        # Delete the symbolic link /data/web_static/current if it exists
        run('sudo rm -rf /data/web_static/current')

        # Create a new symbolic link /data/web_static/current
        run('sudo ln -s {} /data/web_static/current'.format(releases_path))
        print("New version deployed!")
        return True
    except Exception as e:
        print("An exception occurred: {}".format(e))
        return False
