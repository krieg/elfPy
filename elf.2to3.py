--- elf.py	(original)
+++ elf.py	(refactored)
@@ -43,7 +43,7 @@
 
 #Imports
 
-import urllib2
+import urllib.request, urllib.error, urllib.parse
 import json
 #import ssl
 import getpass
@@ -51,14 +51,14 @@
 import sys
 import gzip
 import time
-from StringIO import StringIO
+from io import StringIO
 import base64
 
 # login function
 def login():
     ''' Login to salesforce service using OAuth2 '''
     # prompt for username and password
-    username = raw_input('Username: \n')
+    username = input('Username: \n')
     password = getpass.getpass('Password: \n')
 
     # check to see if anything was entered and if not, default values
@@ -66,11 +66,11 @@
     if len(username) < 1:
         username = 'user@company.com'
         password = 'Passw0rd'
-        print 'Using default username: ' + username
-    else:
-        print 'Using user inputed username: ' + username
-
-    print 'check point'
+        print('Using default username: ' + username)
+    else:
+        print('Using user inputed username: ' + username)
+
+    print('check point')
     # create a new salesforce REST API OAuth request
     url = 'https://login.salesforce.com/services/oauth2/token'
     data = '&grant_type=password&client_id='+CLIENT_ID+'&client_secret='+CLIENT_SECRET+'&username='+username+'&password='+password
@@ -93,8 +93,8 @@
     # urllib2.install_opener(opener)
 
     # call salesforce REST API and pass in OAuth credentials
-    req = urllib2.Request(url, data, headers)
-    res = urllib2.urlopen(req)
+    req = urllib.request.Request(url, data, headers)
+    res = urllib.request.urlopen(req)
 
     # load results to dictionary
     res_dict = json.load(res)
@@ -114,20 +114,20 @@
     # login and retrieve access_token and day
     access_token, instance_url = login()
 
-    day = raw_input('\nDate range (e.g. Last_n_Days:2, Today, Tomorrow):\n')
+    day = input('\nDate range (e.g. Last_n_Days:2, Today, Tomorrow):\n')
 
     # check to see if anything was entered and if not, default values
     if len(day) < 1:
         day = 'Last_n_Days:2'
-        print 'Using default date range: ' + day + '\n'
-    else:
-        print 'Using user inputed date range: ' + day + '\n'
+        print('Using default date range: ' + day + '\n')
+    else:
+        print('Using user inputed date range: ' + day + '\n')
 
     # query Ids from Event Log File
     url = instance_url+'/services/data/v33.0/query?q=SELECT+Id+,+EventType+,+Logdate+From+EventLogFile+Where+LogDate+=+'+day
     headers = {'Authorization' : 'Bearer ' + access_token, 'X-PrettyPrint' : '1'}
-    req = urllib2.Request(url, None, headers)
-    res = urllib2.urlopen(req)
+    req = urllib.request.Request(url, None, headers)
+    res = urllib.request.urlopen(req)
     res_dict = json.load(res)
 
     # capture record result size to loop over
@@ -135,18 +135,18 @@
 
     # provide feedback if no records are returned
     if total_size < 1:
-        print 'No records were returned for ' + day
+        print('No records were returned for ' + day)
         sys.exit()
 
     # create a directory for the output
-    dir = raw_input("Output directory: ")
+    dir = input("Output directory: ")
 
     # check to see if anything
     if len(dir) < 1:
         dir = 'elf'
-        print '\ndefault directory name used: ' + dir
-    else:
-        print '\ndirectory name used: ' + dir
+        print('\ndefault directory name used: ' + dir)
+    else:
+        print('\ndirectory name used: ' + dir)
 
     # If directory doesn't exist, create one
     if not os.path.exists(dir):
@@ -156,15 +156,15 @@
     res.close
 
     # check to see if the user wants to download it compressed
-    compress = raw_input('\nUse compression (y/n)\n').lower()
-    print compress
+    compress = input('\nUse compression (y/n)\n').lower()
+    print(compress)
 
     # check to see if anything
     if len(compress) < 1:
         compress = 'yes'
-        print '\ndefault compression being used: ' + compress
-    else:
-        print '\ncompression being used: ' + compress
+        print('\ndefault compression being used: ' + compress)
+    else:
+        print('\ncompression being used: ' + compress)
 
     # loop over json elements in result and download each file locally
     for i in range(total_size):
@@ -179,22 +179,22 @@
         # provide correct compression header
         if (compress == 'y') or (compress == 'yes'):
             headers = {'Authorization' : 'Bearer ' + access_token, 'X-PrettyPrint' : '1', 'Accept-encoding' : 'gzip'}
-            print 'Using gzip compression\n'
+            print('Using gzip compression\n')
         else:
             headers = {'Authorization' : 'Bearer ' + access_token, 'X-PrettyPrint' : '1'}
-            print 'Not using gzip compression\n'
+            print('Not using gzip compression\n')
 
         # begin profiling
         start = time.time()
 
         # open connection
-        req = urllib2.Request(url, None, headers)
-        res = urllib2.urlopen(req)
-
-        print '********************************'
+        req = urllib.request.Request(url, None, headers)
+        res = urllib.request.urlopen(req)
+
+        print('********************************')
 
         # provide feedback to user
-        print 'Downloading: ' + dates[:10] + '-' + types + '.csv to ' + os.getcwd() + '/' + dir + '\n'
+        print('Downloading: ' + dates[:10] + '-' + types + '.csv to ' + os.getcwd() + '/' + dir + '\n')
 
         # print the response to see the content type
         # print res.info()
@@ -228,7 +228,7 @@
 
         #msecs = secs * 1000  # millisecs
         #print 'elapsed time: %f ms' % msecs
-        print 'Total download time: %f seconds\n' % secs
+        print('Total download time: %f seconds\n' % secs)
 
         file.close
         i = i + 1
