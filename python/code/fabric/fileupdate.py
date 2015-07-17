#! /usr/bin/python
# coding:utf-8

from fabric.api import *
from fabric.context_managers import *
from  fabric.contrib.console import confirm

__author__ = 'hgf'

env.user = 'root'
env.hosts = ['192.168.122.190', '192.168.122.8']
env.password = 'hgfgood'


@task
@runs_once
def tar_task():
    with lcd('/home/hgf'):
        local('tar -zcf 国重.tar.gz 国重')

@task
def put_task():
    run("mkdir -p /data/bak")
    with cd("/data/bak"):
        with settings(warn_only=True):
            result = put("/home/hgf/国重.tar.gz", "/data/bak")
        if result.failed and not confirm("put file failed, Continue[Y/N]?"):
            abort("Aborting file put task!")

@task
def check_task():
    with settings(warn_only=True):
        lmd5 = local("md5sum /home/hgf/国重.tar.gz", capture=True).split(' ')[0]
        rmd5 = run("md5sum /home/hgf/国重.tar.gz").split(' ')[0]
    if lmd5 == rmd5:
        print("OK")
    else:
        print("ERROR")