# YERP: YERP, Everything Runs Perfectly

When someone asks you "Hey, have those network configs been done yet?"

You reply: YERP

YERP is a streamlined way to deploy anything that can interact with an SSH connection. 

There were a handful of design principals.  

* Lightweight - Usable from any computer capable of running python with a network connection
* Usability - Anyone with minimal command line experience should be able to use it
* Security - It shouldn't require anything more than it needs to run, security as the default
* Education - It should educate the user on what it is doing, as it does it

In this line, YERP was developed. It matches most of the design principals, except the education one, which is up to the person who writes the config to document appropriately, and will likely never be successful as a result.  

### Prerequisites
* python 2.7
* [Fabric](http://www.fabfile.org/)

YERP is tested with 2.7, as it is the most common Python install, and it may work with other installs as well.  
As with most python packages, Fabric can be installed using pip:
```bash
pip install fabric
```

### Usage

YERP relies on two things:

* Config file
* Connection Information

The config file contains all of the needed information to go from a default install to a machine that is ready to use in your environment.  

The connection information provides the targets for the configs that you have specified.  

#### Config File Example

```yaml
options:
	# options specifies global options to the host - IPs, gateways, interfaces, subnets, dhcp options, etc.
	# The first value is the variable to substitute for in the file template.
	# The second value is the replacement value for that variable.
	internal_interface: "em0" 
	# all instances of "internal_interface" in the config files would be replaced by em0
	external_interface: "em1"
	dns_server_1: "8.8.8.8"
	dns_server_2: "4.2.2.1"
	sshd_interface: "em0"
	domain_name: "test"
	internal_subnet_dhcp: "192.168.1.0"
	subnet_mask: "255.255.255.0"
	internal_router: "192.168.1.1"
 	dhcpd_range_low: "192.168.1.10"
	dhcpd_range_high: "192.168.1.245"

# tasks cover individual tasks that need to be executed to successfully deploy configurations.
# tasks can configs, commands, or both
setup_router:
  configs:
	# configs control source and destination for config files. Directories are relative to the config file directory.  
    - source: "dhcpd.template"
	  # templates are used to propgate appropriate global settings into config files
      destination: "/etc/dhcpd.conf" 
	  # destination the location on the target machine this file should be placed
      options:
	  	# this allows for specific overrides of options within config files, just in case
        dhcpd_range_high: "192.168.1.150"
  commands:
  	# commands allow you to execute individual commands after config files are placed, such as service restarts
    - "/etc/rc.d/dhcpd restart"

#
file_copy_task:
  configs:
    - source: "credentials.template"
      destination: "/etc/secret_credentials"
      options:
        username: "hax"

only_commands_task:
  commands:
    - "shutdown -r now"

```

#### Config template example

This configuration template will replace the strings %(*variable name*)s with the appropriate variable options from the config file.  

##### dhcpd.template
```
#
# DHCP server options.
# See dhcpd.conf(5) and dhcpd(8) for more information.
#

option  domain-name "%(domain_name)s";
option  domain-name-servers %(dns_server_1)s, %(dns_server_2)s;

subnet %(internal_subnet_dhcp)s netmask %(subnet_mask)s {
    option routers %(internal_router)s;

  range %(dhcpd_range_low)s %(dhcpd_range_high)s;
}
```

### How to YERP
Clone this repository, then:
```bash
cd yerp
fab yerp.deploy_config:config_file=<config file location> -H <target hosts/ips, comma seperated> -u <Username>
```

Really, you should be using this with public/private keys to automate the majesty but hey, no judgement here. Usernames are alright.  

No recourse or refund offered for those who now say "YERP" endlessly.