#!/usr/bin/env python3
import cloudgenix
import argparse
from cloudgenix import jd, jd_detailed, jdout
import cloudgenix_settings
import sys
import logging
import os
import datetime
import time
from datetime import datetime, timedelta
import sys


# Global Vars
TIME_BETWEEN_API_UPDATES = 60       # seconds
REFRESH_LOGIN_TOKEN_INTERVAL = 7    # hours
SDK_VERSION = cloudgenix.version
SCRIPT_NAME = 'CloudGenix: Reboot ION'
SCRIPT_VERSION = "1"

# Set NON-SYSLOG logging to use function name
logger = logging.getLogger(__name__)

####################################################################
# Read cloudgenix_settings file for auth token or username/password
####################################################################

sys.path.append(os.getcwd())
try:
    from cloudgenix_settings import CLOUDGENIX_AUTH_TOKEN

except ImportError:
    # Get AUTH_TOKEN/X_AUTH_TOKEN from env variable, if it exists. X_AUTH_TOKEN takes priority.
    if "X_AUTH_TOKEN" in os.environ:
        CLOUDGENIX_AUTH_TOKEN = os.environ.get('X_AUTH_TOKEN')
    elif "AUTH_TOKEN" in os.environ:
        CLOUDGENIX_AUTH_TOKEN = os.environ.get('AUTH_TOKEN')
    else:
        # not set
        CLOUDGENIX_AUTH_TOKEN = None

def reboot(cgx, element_name) : 
    
    count_down = 10
    while count_down != 0:
        print("Device will reboot in: " + str(count_down) + " seconds")
        count_down -= 1
        time.sleep(1)

    for element in cgx.get.elements().cgx_content['items']:
        if element["name"] == element_name:
            data = {"action":"reboot","parameters":None}
            resp = cgx.post.tenant_element_operations(element_id=element["id"],data=data)
            if not resp:
                print("Error rebooting " + element["name"] + "\n")
                print(str(jd_detailed(resp)))
            else:
                print("Rebooting " + element["name"] + "\n")
        
    
    return
                                 
def go():
    ############################################################################
    # Begin Script, parse arguments.
    ############################################################################

    # Parse arguments
    parser = argparse.ArgumentParser(description="{0}.".format(SCRIPT_NAME))

    # Allow Controller modification and debug level sets.
    config_group = parser.add_argument_group('Name', 'These options change how the configuration is loaded.')
    config_group.add_argument("--name", "-N", help="Element Name", required=True, default=None)
    config_group.add_argument("--hours", "-H", help="How many hours", required=False, default=None)
    controller_group = parser.add_argument_group('API', 'These options change how this program connects to the API.')
    controller_group.add_argument("--controller", "-C",
                                  help="Controller URI, ex. "
                                       "Alpha: https://api-alpha.elcapitan.cloudgenix.com"
                                       "C-Prod: https://api.elcapitan.cloudgenix.com",
                                  default=None)
    controller_group.add_argument("--insecure", "-I", help="Disable SSL certificate and hostname verification",
                                  dest='verify', action='store_false', default=True)
    login_group = parser.add_argument_group('Login', 'These options allow skipping of interactive login')
    login_group.add_argument("--email", "-E", help="Use this email as User Name instead of prompting",
                             default=None)
    login_group.add_argument("--pass", "-PW", help="Use this Password instead of prompting",
                             default=None)
    debug_group = parser.add_argument_group('Debug', 'These options enable debugging output')
    debug_group.add_argument("--debug", "-D", help="Verbose Debug info, levels 0-2", type=int,
                             default=0)
                             
    args = vars(parser.parse_args())
    
    ############################################################################
    # Instantiate API
    ############################################################################
    cgx_session = cloudgenix.API(controller=args["controller"], ssl_verify=args["verify"])

    # set debug
    cgx_session.set_debug(args["debug"])

    ##
    # ##########################################################################
    # Draw Interactive login banner, run interactive login including args above.
    ############################################################################
    print("{0} v{1} ({2})\n".format(SCRIPT_NAME, SCRIPT_VERSION, cgx_session.controller))

    # login logic. Use cmdline if set, use AUTH_TOKEN next, finally user/pass from config file, then prompt.
    # check for token
    if CLOUDGENIX_AUTH_TOKEN and not args["email"] and not args["pass"]:
        cgx_session.interactive.use_token(CLOUDGENIX_AUTH_TOKEN)
        if cgx_session.tenant_id is None:
            print("AUTH_TOKEN login failure, please check token.")
            sys.exit()

    else:
        while cgx_session.tenant_id is None:
            cgx_session.interactive.login(user_email, user_password)
            # clear after one failed login, force relogin.
            if not cgx_session.tenant_id:
                user_email = None
                user_password = None

    ############################################################################
    # End Login handling, begin script..
    ############################################################################

    # get time now.
    curtime_str = datetime.utcnow().strftime('%Y-%m-%d-%H-%M-%S')

    # create file-system friendly tenant str.
    tenant_str = "".join(x for x in cgx_session.tenant_name if x.isalnum()).lower()
    cgx = cgx_session
    
    element_name = args["name"]
    hours = args["hours"]
    
    element_found = False
    for element in cgx.get.elements().cgx_content['items']:
        if element["name"] == element_name:
            element_found = True
            
    if not element_found:
        print("Element not found.")
        sys.exit()
    
    if hours:
        time_wait = int(hours)
        while time_wait != 0:
            print("Waiting " + str(time_wait) + " hours before rebooting " + ". Will report back in 1 hour!!")
            time.sleep(3600)
            time_wait -= 1
        reboot(cgx, element_name)
    else:
        reboot(cgx, element_name) 
    # end of script, run logout to clear session.
    print("End of script. Logout!")
    cgx_session.get.logout()

if __name__ == "__main__":
    go()