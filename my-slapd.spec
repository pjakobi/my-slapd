#
# Spec file for comtics-slapd
#
Summary: openldap simplified configuration (ready for Fusion Directory)
Name: my-slapd

%define version 0.0
%define release 1

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




%description
This rpm customizes openldap for the needs of quick installation.
Schemas from Fusion Directory are also necessary.

%prep
%setup -q -n %{name}-%{version}.%{release}



%build
#@./getdc.sh ./root_dse ./slapd.conf.skel ./slapd.conf
#@./getdc.sh ./root_dse ./basedomain.ldif.skel ./basedomain.ldif
root_dse=`cat root_dse`
first_dc_val=`echo $root_dse | sed 's/,/\n/' | sed '2,$d' | sed s/dc=//`
sed s/###ROOT_DSE###/$root_dse/ slapd.conf.skel > slapd.conf
sed s/###ROOT_DSE###/$root_dse/ basedomain.ldif.skel > basedomain.ldif
sed -i s/###FIRST_DC_VAL###/$first_dc_val/ basedomain.ldif
password=`cat ldap.secret`
sed -i s/###PASSWD###/$password/ slapd.conf

%install
install --directory $RPM_BUILD_ROOT/etc
install --directory $RPM_BUILD_ROOT/etc/openldap
install -m 0755 slapd.conf $RPM_BUILD_ROOT/etc/openldap/slapd.conf
install -m 0755 basedomain.ldif $RPM_BUILD_ROOT/etc/openldap/basedomain.ldif
install -m 0600 ldap.secret $RPM_BUILD_ROOT/etc/ldap.secret
install --directory $RPM_BUILD_ROOT/var
install --directory $RPM_BUILD_ROOT/var/lib
install --directory $RPM_BUILD_ROOT/var/lib/ldap
install -m 0755 DB_CONFIG.example $RPM_BUILD_ROOT/var/lib/ldap/DB_CONFIG

%post
# Openldap
rm -rf /etc/openldap/slapd.d/*
slaptest -f /etc/openldap/slapd.conf -F /etc/openldap/slapd.d
chown -R ldap: /etc/openldap/slapd.d
systemctl start slapd
root_dse=`grep suffix /etc/openldap/slapd.conf | sed s/suffix// | sed s/\"//g | sed "s/^[ \t]*//"`
ldapadd -c -x -D cn=Manager,$root_dse -y /etc/ldap.secret -f /etc/openldap/basedomain.ldif
systemctl stop slapd

#%clean
#rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc README.md TODO
%config /etc/openldap/slapd.conf
%config /etc/openldap/basedomain.ldif
%config /etc/ldap.secret
%config /var/lib/ldap/DB_CONFIG

%changelog
* Fri Mar 30 2018  Pascal Jakobi <pascal.jakobi@thalesgroup.com> 0.1.1
- Initial RPM release
