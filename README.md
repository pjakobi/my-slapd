# comtics-slapd

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

At last, 3 parameters are to be set in the spec file : the directory password, the root DSE, the directory first value. 

Regarding the password, a default value is provided, without encryption. A good idea is to leave it as is and change both the configuration and directory database password after installation, thanks to `slappasswd` and `ldapmodify` (Apache Directory Studio does it perfectly as well).

The root DSE is the "base of the Directory" : `dc=gouv,dc=fr` or `dc=google, dc=com`, etc. In these examples, the "Directory First Value" would be "gouv" or "google".

## Building the RPM

Then, just run `rpmbuild -ba my-slapd.spec` in the SPECS directory. You should then have the rpm file built into `RPMS/noarch/comtics-slapd-version.release.noarch.rpm`.

## Installing openldap
Normally, it becomes as simple as runing `yum localinstall comtics-slapd-version.noarch.rpm`....
