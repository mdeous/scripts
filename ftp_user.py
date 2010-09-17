#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Add/del/list vsftpd users using MySQL
#
# dependencies:
# - python-mysqldb
#

import sys
import MySQLdb
from getpass import getpass

def usage():
    print("Usage: %s {{add|del <user>}|list}" % sys.argv[0])
    sys.exit(1)

def adduser(username):
    try:
        db_pass = getpass("MySQL password for vsftpd: ")
        db = MySQLdb.connect("localhost", "vsftpd", db_pass, "vsftpd")
        cursor = db.cursor()
        passwd = getpass("Password for new user (%s): " % username)
        query = "INSERT INTO users (NAME, PASS, CRYPT) VALUES('%s', '%s', 'ENCRYPT')" % \
                (username, passwd)
        cursor.execute(query)
        cursor.close()
        db.close()
        print("User successfully added\n" % username)
    except MySQLdb.OperationalError, err:
        print("Error: %s" % err[1])

def deluser(username):
    try:
        db_pass = getpass("MySQL password for vsftpd: ")
        db = MySQLdb.connect("localhost", "vsftpd", db_pass, "vsftpd")
        cursor = db.cursor()
        query = "DELETE FROM users WHERE NAME='%s'" % username
        cursor.execute(query)
        cursor.close()
        db.close()
        print("User successfully removed (%s)\n" % username)
    except MySQLdb.OperationalError, err:
        print("Error: %s" % err[1])

def listusers():
    try:
        db_pass = getpass("MySQL password for vsftpd: ")
        db = MySQLdb.connect("localhost", "vsftpd", db_pass, "vsftpd")
        cursor = db.cursor()
        cursor.execute("SELECT NAME FROM users")
        names = [row[0] for row in cursor.fetchall()]
        cursor.close()
        db.close()
        print("\n## Users ###########")
        for name in names:
            print("%d - %s" % (names.index(name)+1, name))
        print("#"*20)
    except MySQLdb.OperationalError, err:
        print("Error: %s" % err[1])

if len(sys.argv) == 2:
    mode = sys.argv[1].lower()
    if mode == "list":
        listusers()
    else:
        usage()
elif len(sys.argv) == 3:
    mode, user = sys.argv[1].lower(), sys.argv[2]
    if mode == "add":
        adduser(user)
    elif mode == "del":
        deluser(user)
    else:
        usage()
else:
    usage()
sys.exit(0)
