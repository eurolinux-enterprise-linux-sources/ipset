# service legacy actions
%define legacy_actions %{_libexecdir}/initscripts/legacy-actions

Name:             ipset
Version:          6.38
Release:          2%{?dist}
Summary:          Manage Linux IP sets

License:          GPLv2
URL:              http://ipset.netfilter.org/
Source0:          http://ipset.netfilter.org/%{name}-%{version}.tar.bz2
Source1:          %{name}.service
Source2:          %{name}.start-stop
Source3:          %{name}-config
Source4:          %{name}.save-legacy

BuildRequires:    libmnl-devel

# An explicit requirement is needed here, to avoid cases where a user would
# explicitly update only one of the two (e.g 'yum update ipset')
Requires:         %{name}-libs%{?_isa} = %{version}-%{release}

%description
IP sets are a framework inside the Linux kernel since version 2.4.x, which can
be administered by the ipset utility. Depending on the type, currently an IP
set may store IP addresses, (TCP/UDP) port numbers or IP addresses with MAC
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


%package libs
Summary:       Shared library providing the IP sets functionality

%description libs
This package contains the libraries which provide the IP sets funcionality.


%package devel
Summary:       Development files for %{name}
Requires:      %{name}-libs%{?_isa} == %{version}-%{release}
Requires:      kernel-devel

%description devel
This package contains the files required to develop software using the %{name}
libraries.


%package service
Summary:          %{name} service for %{name}s
Requires:         %{name} = %{version}-%{release}
BuildRequires:    systemd
Requires:         iptables-services
Requires(post):   systemd
Requires(preun):  systemd
Requires(postun): systemd
BuildArch:        noarch

%description service
This package provides the service %{name} that is split
out of the base package since it is not active by default.


%prep
%setup -q


%build
%configure --enable-static=no --with-kmod=no

# Just to make absolutely sure we are not building the bundled kernel module
# I have to do it after the configure run unfortunately
rm -fr kernel

# Prevent libtool from defining rpath
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot}
find %{buildroot} -name '*.la' -exec rm -f '{}' \;

# install systemd unit file
install -d -m 755 %{buildroot}/%{_unitdir}
install -c -m 644 %{SOURCE1} %{buildroot}/%{_unitdir}

# install supporting script
install -d -m 755 %{buildroot}%{_libexecdir}/%{name}
install -c -m 755 %{SOURCE2} %{buildroot}%{_libexecdir}/%{name}

# install ipset-config
install -d -m 755 %{buildroot}%{_sysconfdir}/sysconfig
install -c -m 600 %{SOURCE3} %{buildroot}%{_sysconfdir}/sysconfig/%{name}-config

# install legacy actions for service command
install -d %{buildroot}/%{legacy_actions}/ipset
install -c -m 755 %{SOURCE4} %{buildroot}/%{legacy_actions}/ipset/save

# Create directory for configuration
mkdir -p %{buildroot}%{_sysconfdir}/%{name}


%preun
if [[ $1 -eq 0 && -n $(lsmod | grep "^xt_set ") ]]; then
    rmmod xt_set 2>/dev/null
    [[ $? -ne 0 ]] && echo Current iptables configuration requires ipsets && exit 1
fi


%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig


%post service
%systemd_post %{name}.service

%preun service
if [[ $1 -eq 0 && -n $(lsmod | grep "^xt_set ") ]]; then
    rmmod xt_set 2>/dev/null
    [[ $? -ne 0 ]] && echo Current iptables configuration requires ipsets && exit 1
fi
%systemd_preun %{name}.service

%postun service
%systemd_postun_with_restart %{name}.service

%triggerin service -- ipset-service < 6.38-1%{?dist}
# Before 6.38-1, ipset.start-stop keeps a backup of previously saved sets, but
# doesn't touch the /etc/sysconfig/ipset.d/.saved flag. Remove the backup on
# upgrade, so that we use the current version of saved sets
rm -f /etc/sysconfig/ipset.save || :
exit 0

%triggerun service -- ipset-service < 6.38-1%{?dist}
# Up to 6.29-1, ipset.start-stop uses a single data file
for f in /etc/sysconfig/ipset.d/*; do
    [ "${f}" = "/etc/sysconfig/ipset.d/*" ] && break
    cat ${f} >> /etc/sysconfig/ipset || :
done
exit 0

%files
%doc COPYING ChangeLog
%doc %{_mandir}/man8/%{name}.8.gz
%{_sbindir}/%{name}

%files libs
%doc COPYING
%{_libdir}/lib%{name}.so.11*

%files devel
%{_includedir}/lib%{name}
%{_libdir}/lib%{name}.so
%{_libdir}/pkgconfig/lib%{name}.pc

%files service
%{_unitdir}/%{name}.service
%dir %{_libexecdir}/%{name}
%config(noreplace) %attr(0600,root,root) %{_sysconfdir}/sysconfig/ipset-config
%ghost %config(noreplace) %attr(0600,root,root) %{_sysconfdir}/sysconfig/ipset
%attr(0755,root,root) %{_libexecdir}/%{name}/%{name}.start-stop
%dir %{legacy_actions}/ipset
%{legacy_actions}/ipset/save


%changelog
* Wed Jun 27 2018 Stefano Brivio <sbrivio@redhat.com> - 6.38-2
- Fix upgrade and downgrade triggers in specfile (RHBZ#1594722)

* Mon Apr 16 2018 Stefano Brivio <sbrivio@redhat.com> - 6.38-1
- Rebase to 6.38 (RHBZ#1557600):
  - hash:ipmac type support added to ipset, userspace part (Tomasz Chilinski)
- Refactor /etc/sysconfig/ipset.start-stop
- Fixes:
  - IPSet Service Monolithic Operation (RHBZ#1440741)
  - "systemctl start ipset" doesn't handle existing ipset's having counters
    (RHBZ#1502212)

* Wed Feb  1 2017 Thomas Woerner <twoerner@redhat.com> - 6.29-1
- Rebase to 6.29 (RHBZ#1351299)
- Fixes:
  - Backport ipset capability to run in namespaces (RHBZ#1226051)
  - Fix service save with empty ipset list and existing ipset save file
    (RHBZ#1377621)
  - Fix internal error at printing to output buffer (RHBZ#1395865)

* Wed Aug 17 2016 Thomas Woerner <twoerner@redhat.com> - 6.19-6
- Use /etc/sysconfig/ipset-config in service as EnvironmentFile (RHBZ#1136257)
- Use /etc/sysconfig/ipset for data as in RHEL-6 (RHBZ#1136257)
- No save on reload, but legacy save action (RHBZ#1136257)

* Wed Jun 29 2016 Thomas Woerner <twoerner@redhat.com> - 6.19-5
- New service sub package to provide the ipset service (RHBZ#1136257)
  Service and start-stop script from F-24
- Fixed ipset package summary (RHBZ#1195171)
  Spec file derived from F-24

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 6.19-4
- Mass rebuild 2014-01-24

* Tue Jan 14 2014 Thomas Woerner <twoerner@redhat.com> - 6.19-3
- fixed failed rmdiff testing (RHBZ#884500)

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 6.19-2
- Mass rebuild 2013-12-27

* Thu Aug 15 2013 Mathieu Bridon <bochecha@fedoraproject.org> - 6.19
- New upstream release.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.16.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.16.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Sep 26 2012 Mathieu Bridon <bochecha@fedoraproject.org> - 6.16.1-1
- New upstream release.
- Fix a requirement.

* Wed Sep 26 2012 Mathieu Bridon <bochecha@fedoraproject.org> - 6.14-1
- New upstream release.
- Fix scriptlets, ldconfig is needed for the libs subpackage, not the main one.

* Mon Jul 30 2012 Mathieu Bridon <bochecha@fedoraproject.org> - 6.13-1
- New upstream release.
- Split out the library in its own subpackage.

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Feb 06 2012 Mathieu Bridon <bochecha@fedoraproject.org> - 6.11-1
- New upstream release.
- Removed our patch, it has been integrated upstream. As such, we also don't
  need to re-run autoreconf any more.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.9.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Sep 16 2011 Mathieu Bridon <bochecha@fedoraproject.org> - 6.9.1-2
- Some fixes based on Pierre-Yves' review feedback.

* Wed Sep 14 2011 Mathieu Bridon <bochecha@fedoraproject.org> - 6.9.1-1
- Initial packaging.
