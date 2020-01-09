Name:          ipset
Version:       6.11
Release:       3%{?dist}
Summary:       Manage Linux IP sets

Group:         Applications/System
License:       GPLv2
URL:           http://ipset.netfilter.org/
Source0:       http://ipset.netfilter.org/%{name}-%{version}.tar.bz2
Source1:       ipset.init
BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: autoconf automake libtool
BuildRequires: libmnl-devel
BuildRequires: kernel-headers

%description
IP sets are a framework inside the Linux 2.4.x and 2.6.x kernel, which can be
administered by the ipset utility. Depending on the type, currently an IP set
may store IP addresses, (TCP/UDP) port numbers or IP addresses with MAC
addresses in a way, which ensures lightning speed when matching an entry
against a set.

If you want to:
 - store multiple IP addresses or port numbers and match against the collection
   by iptables at one swoop;
 - dynamically update iptables rules against IP addresses or ports without
   performance penalty;
 - express complex IP address and ports based rulesets with one single iptables
   rule and benefit from the speed of IP sets
then ipset may be the proper tool for you.


%package devel
Summary:       Development files for %{name}
Requires:      %{name}%{?_isa} == %{version}-%{release}
Requires:      kernel-devel

%description devel
This package contains the files required to develop software using the %{name}
libraries.


%prep
%setup -q


%build
autoreconf -i
%configure --enable-static=no --with-kmod=no

# Prevent libtool from defining rpath
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot}
find %{buildroot} -name '*.la' -exec rm -f '{}' \;

# install init scripts and configuration files
install -d -m 755 %{buildroot}/etc/rc.d/init.d
install -c -m 755 %{SOURCE1} %{buildroot}/etc/rc.d/init.d/ipset


%clean
rm -rf %{buildroot}


%post
/sbin/ldconfig
/sbin/chkconfig --add ipset


%postun -p /sbin/ldconfig


%preun
if [ "$1" = 0 ]; then
        /sbin/chkconfig --del ipset
fi

%files
%defattr(-,root,root,-)
%doc COPYING ChangeLog
%attr(0755,root,root) /etc/rc.d/init.d/ipset
%doc %{_mandir}/man8/%{name}.8.gz
%{_sbindir}/%{name}
%{_libdir}/lib%{name}.so.*

%files devel
%defattr(-,root,root,-)
%doc COPYING
%dir %{_includedir}/libipset
%{_includedir}/libipset/*.h
%{_libdir}/lib%{name}.so


%changelog
* Tue Aug 26 2014 Thomas Woerner <twoerner@redhat.com> - 6.11-3
- fixed init script according to according to rhbz#1130570 and rhbz#888571#c28

* Fri Jun 13 2014 Thomas Woerner <twoerner@redhat.com> - 6.11-2
- added ipset init script (rhbz#888571)

* Fri Feb 10 2012 Thomas Woerner <twoerner@redhat.com> - 6.11-1
- new version 6.11 with so library version 2, includes
- cleaned up spec file for 6.11, dropped patch, no kernel will be built
- adapted for RHEL-6: added clean tag, BuildRoot

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.9.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Sep 16 2011 Mathieu Bridon <bochecha@fedoraproject.org> - 6.9.1-2
- Some fixes based on Pierre-Yves' review feedback.

* Wed Sep 14 2011 Mathieu Bridon <bochecha@fedoraproject.org> - 6.9.1-1
- Initial packaging.
