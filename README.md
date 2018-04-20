# my-slapd

This is a spec file that may be used to install quickly an openldap instance (rpm format). The rpm comes with a few configuration files that are necessary. The spec file also lists the various dependencies that are necessary, including fusion directory.

## Preparation
* As usual with RPMs, a build environment is necessary, typically `_somewhere_/rpmbuild/{SPECS, SOURCES, RPMS, ...}` (see rpm documentation).

* Also, you need to know your `version.release`. This is to be found at the beginning of the spec file on gitHub (my-slapd.spec) :
    `%define version 0.0`
and
    `%define release 1`

* Once you have it, download the complete repo :
    `git clone git://github.com/pjakobi/my-slapd my-slapd-0.0.1`

* In the my-slapd-0.0.1/myslapd.spec file, set the _topdir_ to `_somewhere_/rpmbuild`. Save it into the `_somewhere_/rpmbuild/SPECS` directory
    

* At last, create a tar.gz file; it should reside in the SOURCES subdir of the RPM build system :
    `tar cvfz SOURCES/my-slapd-0.0.1.tar.gz my-slapd-0.0.1/*`

## LDAP Set up

In order to use this feature, the yum repositories are also to be set correctly (CentOS base, etc.). For Fusion directory repos, refer to the site's documentation.

2 parameters are to be set : the directory password and the root DSE, the directory "root". 

Regarding the password, a value is to be provided, without encryption, in the "ldap.secret" file (see example). 

The root DSE is the "base of the Directory" : `dc=gouv,dc=fr` or `dc=google, dc=com`, etc. It has to be set in the `root_dse` file 

## Building the RPM

Then, just run `rpmbuild -ba my-slapd.spec` in the SPECS directory. You should then have the rpm file built into `RPMS/noarch/my-slapd-version.release.noarch.rpm`. 

## Installing openldap
Normally, it becomes as simple as runing `yum localinstall my-slapd-version.noarch.rpm`.... 
Important security notice : 
- it is highly recommended to remove the /etc/ldap.secret file after installation.
- also, change the default password for the config and mdb database. Normally, you should use an encrypted password (see `man slappasswd` or use a GUI such as Apache Directory Studio).
