#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>
#
###########################################
__app__ = "GetProxy"
__version__ = "0.5"
__author__ = "MatToufoutu"
###########################################
#TODO: sort proxies by speed

import os
import re
import socket
import sys
import urllib2

# put here your own proxy list urls if they display proxies the "ip:port" style
custom_sites = []

proxyfile = "proxylist.txt"
useragent = "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.1.6) Gecko/20091218 Firefox/3.5.6"
timeout = 5
socket.setdefaulttimeout(timeout)
regex_ip = re.compile(r"(?:\d{1,3}\.){3}\d{1,3}")
regex_proxy = re.compile(r"(?:\d{1,3}\.){3}\d{1,3}:\d{1,5}")

class GetProxies:
    """Get/sort/check proxies collected from various websites
    """
    def __init__(self):
        self.trueIP = self.get_true_ip()
        if __name__ == '__main__':
            print("[+] True IP address: %s"% self.trueIP)
        self.codeenlist = []
        self.elitelist = []
        self.anonlist = []
        self.transplist = []
        self.otherlist = []

    def write_proxy(self, proxy):
        """write a proxy to a text file"""
        with open(proxyfile, 'a') as ofile:
            ofile.write(proxy + '\n')
        return

    def get_true_ip(self):
        """get the machine's true IP address"""
        opener = urllib2.build_opener()
        opener.addheaders = [('User-agent', useragent)]
        return opener.open('http://www.whatismyip.com/automation/n09230945.asp').read()

    def check(self, proxy):
        """check if <proxy> is anonymous"""
        re_pxtype = re.compile(r'You are using (?:<b>)?<font color="#[a-f0-9]{6}">(?: <b>)?(.+ proxy)(?:</b>)?</font>')
        re_ip = re.compile(r'IP detected: <font color="#[a-f0-9]{6}">((\d{1,3}\.){3}\d{1,3})')
        handler = urllib2.ProxyHandler({'http':proxy})
        opener = urllib2.build_opener(handler)
        opener.addheaders = [('User-agent', useragent)]
        try:
            html = opener.open('http://checker.samair.ru/').read()
            result = re_pxtype.search(html)
            if result:
                pxtype = result.groups()[0]
                ip = re_ip.search(html).groups()[0]
                if pxtype == 'high-anonymous (elite) proxy':
                    if ip == self.trueIP:
                        print(" - %s > TRANSPARENT" % proxy)
                        self.transplist.append(proxy)
                    else:
                        print(" - %s > ELITE" % proxy)
                        self.write_proxy(proxy)
                        self.elitelist.append(proxy)
                elif pxtype == 'anonymous proxy':
                    print(" - %s > ANONYMOUS" % proxy)
                    self.anonlist.append(proxy)
                else:
                    if "CoDeeN" in html:
                        print(" - %s > CODEEN" % proxy)
                        self.codeenlist.append(proxy.split(":")[0])
                    else:
                        print(" - %s > UNDEFINED" % proxy)
                        self.otherlist.append(proxy)
            opener.close()
        except KeyboardInterrupt:
            opener.close()
            clean_exit()
        except:
            opener.close()

    def get_codeen(self, retried=False):
        """get a list of CoDeeN proxies"""
        try:
            print(" - Gathering a list of known CoDeeN proxies...")
            opener = urllib2.build_opener()
            html = opener.open('http://fall.cs.princeton.edu/codeen/tabulator.cgi?table=table_all').read()
            proxies = regex_ip.findall(html)
            for proxy in proxies:
                self.codeenlist.append(proxy)
            opener.close()
            return self.codeenlist
        except (urllib2.URLError, socket.timeout):
            if retried:
                print(" - Site unavailable: Aborting")
                opener.close()
                return []
            else:
                print(" - Site unavailable: Retrying")
                opener.close()
                self.get_codeen(True)

    def getfrom_multi(self):
        """get a list from various websites providing small proxy lists"""
        sites = custom_sites
        proxylist = []
        opener = urllib2.build_opener()
        opener.addheaders = [('User-agent', useragent)]
        for site in sites:
            try:
                print(" - Gathering proxy list from %s" % site)
                html = opener.open(site).read()
                proxylist.extend(regex_proxy.findall(html))
            except (urllib2.URLError, socket.timeout):
                print(" - Site unavailable: Aborting")
                pass
        opener.close()
        return proxylist

    def getfrom_ipadress(self, retried=False):
        """get a proxy list from http://www.ip-adress.com/"""
        print(" - Gathering proxy list from http://www.ip-adress.com/proxy_list/")
        proxylist = []
        opener = urllib2.build_opener()
        opener.addheaders = [('User-agent', useragent)]
        try:
            html = opener.open('http://www.ip-adress.com/proxy_list/').read()
            proxylist.extend(regex_proxy.findall(html))
            opener.close()
            return proxylist
        except (urllib2.URLError, socket.timeout):
            if retried:
                print(" - Site unavailable: Aborting")
                opener.close()
                return []
            else:
                print(" - Site unavailable: Retrying")
                opener.close()
                self.getfrom_ipadress(True)

    def getfrom_samair(self, retried=False):
        """get a proxy list from http://samair.ru/"""
        print(" - Gathering proxy list from http://www.samair.ru/proxy/")
        hackregex1 = re.compile(r'(([a-z])=(\d);)+')
        hackregex2 = re.compile(r'((\d{1,3}\.){3}\d{1,3})<script type="text/javascript">document\.write\(":"((\+[a-z])+)\)')
        token, maxpages = 1, 20
        proxylist = []
        try:
            while token <= maxpages:
                opener = urllib2.build_opener()
                opener.addheaders = [('User-agent', useragent)]
                if token < 10:
                    html = opener.open('http://www.samair.ru/proxy/proxy-0%d.htm' % token).read()
                else:
                    html = opener.open('http://www.samair.ru/proxy/proxy-%d.htm' % token).read()
                hackdict = dict([x.split("=") for x in hackregex1.search(html).group().split(";")][:-1])
                iplist = [(x[0], x[2].split("+")[1:]) for x in hackregex2.findall(html)]
                for ip, letters in iplist:
                    ip += ":"
                    for letter in letters:
                        ip += hackdict[letter]
                    proxylist.append(ip)
                token += 1
                opener.close()
            return proxylist
        except (urllib2.URLError, socket.timeout):
            if retried:
                print(" - Site unavailable: Aborting")
                opener.close()
                return []
            else:
                print(" - Site unavailable: Retrying")
                opener.close()
                self.getfrom_samair(True)

    def getfrom_proxylist(self, retried=False):
        """get a proxy list from http://www.proxylist.net"""
        print(" - Gathering proxy list from http://www.proxylist.net")
        baseurl = "http://www.proxylist.net/list/0/0/3/0/"
        token, maxpages = 0, 15
        proxylist = []
        try:
            while token <= maxpages:
                opener = urllib2.build_opener()
                opener.addheaders = [('User-agent', useragent)]
                html = opener.open(baseurl+str(token)).read()
                proxylist.extend(regex_proxy.findall(html))
                token += 1
                opener.close()
            return proxylist
        except (urllib2.URLError, socket.timeout):
            if retried:
                print(" - Site unavailable: Aborting")
                opener.close()
                return []
            else:
                print(" - Site unavailable: Retrying")
                opener.close()
                self.getfrom_proxylist(True)

    def get_all(self):
        """get a proxy list from all possible websites"""
        getfuncs = [self.getfrom_multi, self.getfrom_ipadress,
                    self.getfrom_samair, self.getfrom_proxylist]
        proxylist = []
        codeenlist = self.get_codeen()
        for get_proxy in getfuncs:
            try:
                proxylist.extend(get_proxy())
            except TypeError:
                pass
        return proxylist

def clean_exit():
    """display the proxy list path and exit"""
    print("\n[+] Aborted by user !")
    print(" - List path: %s\n" % os.path.join(os.getcwd(), proxyfile))
    sys.exit(0)

import pdb
pdb.set_trace()
if __name__ == "__main__":
    try:
        if os.name == 'posix':
            os.system('clear')
        elif os.name == 'nt':
            os.system('cls')
        print(76*"#")
        print("\t\t\t[ GetProxy List Maker v%s ]\n" % __version__)
        print(76*"#"+"\n")
        collector = GetProxies()
        if os.path.exists(os.path.join(os.getcwd(), proxyfile)):
            os.remove(proxyfile)
        collector.write_proxy("### GetProxy Elite Proxies List ###\n")
        print("[+] Downloading proxy lists")
        proxylist1 = collector.get_all()
        proxylist = []
        for proxy in proxylist1:
            if (proxy not in proxylist) and (proxy not in collector.codeenlist):
                proxylist.append(proxy)
        print(" - Total proxies: %d\n[+] Checking proxies" % len(proxylist))
        for proxy in proxylist:
            collector.check(proxy)
        print("[+] FINISHED !")
        print(" - Total elite proxies: %d" % len(collector.elitelist))
        print(" - List path: %s\n" % os.path.join(os.getcwd(), proxyfile))
        sys.exit(0)
    except KeyboardInterrupt:
        clean_exit()
