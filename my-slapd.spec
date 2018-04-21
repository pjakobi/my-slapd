#
# Spec file for comtics-slapd
#
Summary: openldap simplified configuration (ready for Fusion Directory)
Name: my-slapd

%define version 0.0
%define release 2

%define _topdir /home/utilisateur/Soft/rpmbuild
%define _tmppath %{_topdir}/tmp

Version: %{version}
Release: %{release}
License: LGPL
BuildArch: noarch
Group: System Environment/Daemons
Source0: %{name}-%{version}.%{release}.tar.gz
Vendor: Thales Communications & Security
Packager: Pascal Jakobi <pascal.jakobi@thalesgroup.com>
BuildRoot: %{_tmppath}/%{name}-buildroot
BuildRequires: git
BuildRequires: sed
BuildRequires: wget
Requires: openldap-servers
Requires: openldap-clients
Requires: fusiondirectory-plugin-systems-schema
Requires: fusiondirectory-schema
Requires: schema2ldif
Requires: cyrus-sasl-ldap



%description
This rpm customizes openldap for the needs of quick installation.
Schemas from Fusion Directory are also necessary.

%prep
%setup -q -n %{name}-%{version}.%{release}



%build
#
# Create rootpw lines for mdb and config databases
# (rootpw < qslappassd result = encrypted password >
#
root_dse=`cat root_dse`
sed s/###ROOT_DSE###/$root_dse/ slapd.conf.skel > slapd.conf

tmpfile=`mktemp %{_tmppath}/ldap_secret.XXXX`
export tmpfile
scrfile=`mktemp %{_tmppath}/ldap_scr.XXXX`
export scrfile

echo -n "rootpw " > ${tmpfile}
cat ldap.secret >> $tmpfile
echo -n '/###PASSWD###/r ' > $scrfile 
echo $tmpfile >> $scrfile
echo '/###PASSWD###/d' >> $scrfile

sed -i -f ${scrfile} slapd.conf
rm -f ${tmpfile} ${scrfile}

#
# Set the first domain component value ('x' if DSE='dc=x,dc=y,dc=z)
#
first_dc_val=`echo $root_dse | sed 's/,/\n/' | sed '2,$d' | sed s/dc=//`
sed s/###ROOT_DSE###/$root_dse/ basedomain.ldif.skel > basedomain.ldif
sed -i s/###FIRST_DC_VAL###/$first_dc_val/ basedomain.ldif


%install
install --directory $RPM_BUILD_ROOT/etc
install --directory $RPM_BUILD_ROOT/etc/rsyslog.d
install --directory $RPM_BUILD_ROOT/etc/logrotate.d
install --directory $RPM_BUILD_ROOT/etc/openldap
install -m 0755 slapd.conf $RPM_BUILD_ROOT/etc/openldap/slapd.conf
install -m 0755 basedomain.ldif $RPM_BUILD_ROOT/etc/openldap/basedomain.ldif
install -m 0600 ldap.secret $RPM_BUILD_ROOT/etc/ldap.secret
install --directory $RPM_BUILD_ROOT/var
install --directory $RPM_BUILD_ROOT/var/lib
install --directory $RPM_BUILD_ROOT/var/lib/ldap
install -m 0755 DB_CONFIG.example $RPM_BUILD_ROOT/var/lib/ldap/DB_CONFIG
install --directory $RPM_BUILD_ROOT/var/log
install --directory $RPM_BUILD_ROOT/var/log/openldap
install -m 0644 openldap_logging $RPM_BUILD_ROOT/etc/rsyslog.d/openldap_logging
install -m 0644 openldap_logrotate $RPM_BUILD_ROOT/etc/logrotate.d/openldap_logrotate

%post
# Prepare configuration
rm -rf /etc/openldap/slapd.d/*
slaptest -f /etc/openldap/slapd.conf -F /etc/openldap/slapd.d
chown -R ldap: /etc/openldap/slapd.d

# Create initial values in Openldap
systemctl start slapd
root_dse=`grep suffix /etc/openldap/slapd.conf | sed s/suffix// | sed s/\"//g | sed "s/^[ \t]*//"`

password=`cat /etc/ldap.secret`
export password
ldapadd -c -x -D cn=Manager,$root_dse -w $password -f /etc/openldap/basedomain.ldif
systemctl stop slapd

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc README.md TODO
%config /etc/openldap/slapd.conf
%config /etc/openldap/basedomain.ldif
/etc/ldap.secret
%config /var/lib/ldap/DB_CONFIG
%config /etc/rsyslog.d/openldap_logging
%config /etc/logrotate.d/openldap_logrotate

%changelog
* Thu Apr 19 2018  Pascal Jakobi <pascal.jakobi@thalesgroup.com> 0.0.2
- Prepare logging
* Fri Mar 30 2018  Pascal Jakobi <pascal.jakobi@thalesgroup.com> 0.0.1
- Initial RPM release
