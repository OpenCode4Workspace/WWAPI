#!/usr/local/bin/python2.7
# encoding: utf-8
'''
opencode4workspace.CreateMessageInSpace -- Create a new Message in a Watson Space

opencode4workspace.CreateMessageInSpace is a description

It defines classes_and_methods

@author:    Christian Guedemann

@copyright:  2016 WebGate Consulting AG. All rights reserved.

@license:    Apache V2.0

@contact:    Christian.guedemann@webgate.biz
@deffield    updated: Updated
'''

import sys
import os
import json
import requests
import base64

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter

__all__ = []
__version__ = 0.1
__date__ = '2016-10-27'
__updated__ = '2016-10-27'

DEBUG = 0
TESTRUN = 0
PROFILE = 0

class CLIError(Exception):
    '''Generic exception to raise and log different fatal errors.'''
    def __init__(self, msg):
        super(CLIError).__init__(type(self))
        self.msg = "E: %s" % msg
    def __str__(self):
        return self.msg
    def __unicode__(self):
        return self.msg

def main(argv=None): # IGNORE:C0111
    '''Command line options.'''

    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend(argv)
        
    program_name = os.path.basename(sys.argv[0])
    program_version = "v%s" % __version__
    program_build_date = str(__updated__)
    program_version_message = '%%(prog)s %s (%s)' % (program_version, program_build_date)
    program_shortdesc = __import__('__main__').__doc__.split("\n")[1]
    program_license = '''%s

  Created by Christian Guedemann on %s.
  Copyright 2016 WebGate Consulting AG. All rights reserved.

  Licensed under the Apache License 2.0
  http://www.apache.org/licenses/LICENSE-2.0

  Distributed on an "AS IS" basis without warranties
  or conditions of any kind, either express or implied.

USAGE
''' % (program_shortdesc, str(__date__))

    try:
        # Setup argument parser
        parser = ArgumentParser(description=program_license, formatter_class=RawDescriptionHelpFormatter)
        parser = ArgumentParser()
        parser.add_argument("message", help="The message you want to post")
        parser.add_argument("title", help="The title of the message")
        parser.add_argument("-v", "--verbose", action="store_true", help="set verbose")
        parser.add_argument('-V', '--version', action='version', version=program_version_message)
        parser.add_argument('-a', '--appId', dest="appid", help="Application ID from watson workspace")
        parser.add_argument('-k', '--secretKey', dest="secret", help="Application secrete from watson workspace")
        parser.add_argument("-s", "--space", dest="spaceid", help="id of the space you want to post")
        parser.add_argument("-n", "--avatorName", dest="avatarname", help="name of the avatar")
        parser.add_argument("-p", "--avatar", dest="avatar", help="url to the avatar picture")
        parser.add_argument("-u", "--avatarUrl", dest="avatarurl", help="url to the profile of the avatar")
        parser.add_argument("-c", "--color", dest="color", help="color of the message border")
        # Process arguments
        args = parser.parse_args()
        verbose = args.verbose
        appid = args.appid
        appsecret = args.secret
        spaceid = args.spaceid
        message = args.message
        avatarname = args.avatarname;
        avatar = args.avatar
        avatarurl = args.avatarurl
        title = args.title
        color = args.color
        if not appid or not appsecret or not spaceid or not message or not title or not avatar or not avatarname or not avatarurl or not color:
            raise CLIError("Please define all values");
        if verbose:
            print("Verbose mode on")
            print ("AppId = "+ appid)
            print ("Secret= ********")
            print ("SpaceID = " +spaceid)
            print ("Avatar = " +avatar)
            print ("Avatar Url = " +avatarurl)
            print ("Avatar Name = " +avatarname)
            print ("Color = " +color)
            print("Message = "+message)
            print ("Title = " +title)
        appAccessKey = appid +":"+appsecret
        b64App = base64.b64encode(appAccessKey.encode('ascii'))
    
        payload = {"grant_type":"client_credentials"}
        resp = requests.post(url="https://api.watsonwork.ibm.com/oauth/token", headers={"Authorization":"Basic %s" % b64App.decode("ascii"), "content-type":"application/x-www-form-urlencoded"}, data=payload)
        if resp.status_code != 200:
            raise CLIError("Could not authenticate your application")
        data = json.loads(resp.text)
        token =  data['access_token']
        messagePayload = {"type": "appMessage","version": 1.0,"annotations": [{"type": "generic","version": 1.0,"color": color,"title": title,"text": message,"actor": {"name": avatarname,"avatar": avatar,"url": avatarurl}}]}
        respMessage = requests.post(url="https://api.watsonwork.ibm.com/v1/spaces/"+spaceid+"/messages", headers={"Authorization":"Bearer %s" % token, "content-type":"application/json"}, json=messagePayload)
        if respMessage.status_code != 201:
            raise CLIError("Error while posting: %s" % respMessage.text)
        print(respMessage.text)
    except KeyboardInterrupt:
        ### handle keyboard interrupt ###
        return 0
    except Exception as e:
        if DEBUG or TESTRUN:
            raise(e)
        indent = len(program_name) * " "
        sys.stderr.write(program_name + ": " + repr(e) + "\n")
        sys.stderr.write(indent + "  for help use --help")
        return 2

if __name__ == "__main__":
    if DEBUG:
        print("debug mode")
        #sys.argv.append("-h")
        sys.argv.append("-v")
    if TESTRUN:
        import doctest
        doctest.testmod()
    if PROFILE:
        import cProfile
        import pstats
        profile_filename = 'opencode4workspace.CreateMessageInSpace_profile.txt'
        cProfile.run('main()', profile_filename)
        statsfile = open("profile_stats.txt", "wb")
        p = pstats.Stats(profile_filename, stream=statsfile)
        stats = p.strip_dirs().sort_stats('cumulative')
        stats.print_stats()
        statsfile.close()
        sys.exit(0)
    sys.exit(main())