# linodeDynDNS
A python3 script to run on a *nix server to update a linode domain name with the current IP Address  of the server (creating a dynamic DNS)

#Instructions

Make sure that you have the python libraries requests and json installed:

```
pip install requests
pip install json
```

Edit the python script with the details required at the top. A token to access your linode can be generated [here](https://cloud.linode.com/profile/tokens). Check the script works, then set up a cron job to run the script as often as you feel is rquired.

This script does minimum error checking. It will be updated at some point to support IPv6.