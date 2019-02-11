#!/usr/local/bin/python3
'''
# 3.x script to download EventLogFiles, original by @atorman (https://github.com/atorman/elfPy)
# Refactored from Python 2.7.9 by richard.krieg@gmail.com using 2to3
# Modified by @krieg to use command-line args in lieu of interactive prompts
'''

import argparse
import base64
import getpass
import gzip
from io import StringIO
import json
import os
import sys
import time
import urllib.request, urllib.error, urllib.parse

parser = argparse.ArgumentParser(description='Download Salesforce event log files')
parser.add_argument('username', metavar='U', help='Salesforce username')
parser.add_argument('password', metavar='P', help='Salesforce password')
parser.add_argument('client', metavar='C', help='Salesforce client ID')
parser.add_argument('secret', metavar='S', help='Salesforce client secret')
parser.add_argument('--dates', default='Last_n_Days:2', help='Range of dates to download')
parser.add_argument('--host', default='login.salesforce.com', help='Production or sandbox org')
parser.add_argument('--path', default='./', help='Directory path for results')
args = parser.parse_args()

def login():
    # create a new salesforce REST API OAuth request
    url = 'https://%s/services/oauth2/token' % (args.host)
    dataDict = {'grant_type':'password', 'client_id':args.client, 'client_secret':args.secret, 'username':args.username, 'password':args.password}
    data = urllib.parse.urlencode(dataDict).encode('utf-8')
    headers = {'X-PrettyPrint' : '1'}

    # call salesforce REST API and pass in OAuth credentials
    req = urllib.request.Request(url, data, headers)
    res = urllib.request.urlopen(req)

    # load results to dictionary
    res_dict = json.load(res)

    res.close()

    # return OAuth access token necessary for additional REST API calls
    access_token = res_dict['access_token']
    instance_url = res_dict['instance_url']

    return access_token, instance_url

# download function
def download_elf():
    ''' Query salesforce service using REST API '''
    # login and retrieve access_token and day
    access_token, instance_url = login()

    # query Ids from Event Log File,
    url = instance_url+'/services/data/v44.0/query?q=SELECT+Id+,+EventType+,+Logdate+From+EventLogFile+Where+LogDate+=+'+args.dates
    headers = {'Authorization' : 'Bearer ' + access_token, 'X-PrettyPrint' : '1'}
    req = urllib.request.Request(url, None, headers)
    res = urllib.request.urlopen(req)
    res_dict = json.load(res)

    # capture record result size to loop over
    total_size = res_dict['totalSize']

    # provide feedback if no records are returned
    if total_size < 1:
        print('No records were returned for ' + args.dates)
        sys.exit()

    # If directory doesn't exist, create one
    if not os.path.exists(args.path):
        os.makedirs(args.path)

    res.close

    # loop over json elements in result and download each file locally
    for i in range(total_size):
        # pull attributes out of JSON for file naming
        ids = res_dict['records'][i]['Id']
        types = res_dict['records'][i]['EventType']
        dates = res_dict['records'][i]['LogDate']

        # create REST API request
        url = instance_url+'/services/data/v44.0/sobjects/EventLogFile/'+ids+'/LogFile'

        # provide correct compression header
        headers = {'Authorization' : 'Bearer ' + access_token, 'X-PrettyPrint' : '1', 'Accept-encoding' : 'gzip'}

        # begin profiling
        start = time.time()

        # open connection
        req = urllib.request.Request(url, None, headers)
        res = urllib.request.urlopen(req)

        print('********************************')

        # provide feedback to user
        print('Downloading: ' + dates[:10] + '-' + types + '.csv to ' + os.getcwd() + '/' + args.path + '\n')

        # print the response to see the content type
        # print(res.info())

        # if the response is gzip-encoded as expected
        # compression code from http://bit.ly/pyCompression
        if res.info().get('Content-Encoding') == 'gzip':
            # buffer results
            buf = StringIO(res.read())
            # gzip decode the response
            f = gzip.GzipFile(fileobj=buf)
            # print data
            data = f.read()
            # close buffer
            buf.close()
        else:
            # buffer results
            buf = StringIO(res.read())
            # get the value from the buffer
            data = buf.getvalue()
            #print data
            buf.close()

        # write buffer to CSV with following naming convention yyyy-mm-dd-eventtype.csv
        file = open(args.path + '/' +dates[:10]+'-'+types+'.csv', 'w')
        file.write(data)

        # end profiling
        end = time.time()
        secs = end - start

        msecs = secs * 1000  # millisecs
        print('elapsed time: %f ms' % (msecs))
        print('Total download time: %f seconds\n' % (secs))

        file.close
        i = i + 1
        res.close

download_elf()