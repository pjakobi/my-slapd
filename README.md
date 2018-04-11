# comtics-slapd
# comtics-slapd
This is a spec file that may be used to install quickly an openldap instance (rpm format). The rpm comes with a few configuration files that are necessary. The spec file also lists the various dependencies that are necessary, including fusion directory.

## Set up
As usual with RPMs, a build environment is necessary, typically rpmbuild/{SPECS, SOURCES, RPMS, ...} (see rpm documentation).

In order to use this feature, the yum repositories are also to be set correctly (CentOS base, etc.). For Fusion directory repos, refer to the site's documentation.

At last, 3 parameters are to be set in the spec file : the directory password, the root DSE, the directory first value. 

Regarding the password, a default value is provided, without encryption. A good idea is to leave it as is and change both the configuration and directory database password after installation, thanks to slappassword and ldapmodify (Apache Directory Studio does it perfectly as well).

The root DSE is the "base of the Directory" : dc=gouv,dc=fr or dc=google, dc=com, etc. In these examples, the "Directory First Value" would be "gouv" or "google".

## Building the RPM
Before building, the sources (tar.gz) are to be installed in the SOURCES directory : wget https://github.com/pjakobi/comtics-slapd/archive/version.tar.gz (version = 0.1.6 or equivalent).

Then, just run "rpmbuild -ba comtics-slapd.spec" in the SPECS directory. You should then have the rpm file built into RPMS/noarch/comtics-slapd-varsion.noarch.rpm.

## Installing openldap
Normally, it becomes as simple as runing "yum localinstall comtics-slapd-varsion.noarch.rpm"....
