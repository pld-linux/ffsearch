%include	/usr/lib/rpm/macros.perl
Summary:	Fast File Search
Summary(pl):	Szybka wyszukiwarka plików
Name:		ffsearch
Version:	1.1.2
Release:	0.1
License:	GPL v2
Group:		Applications/WWW
Source0:	http://dl.sourceforge.net/ffsearch/%{name}-%{version}.tar.bz2
# Source0-md5:	27296436414f8daf8453b4deee142a29
Source1:	%{name}.crond
URL:		http://www.phpbb.com/
Requires:	php >= 4.0.3
Requires:	webserver
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_phpdir		/home/services/httpd/html/ffsearch

%description
Fast File Search is a crawler for FTP servers and SMB shares that can be found
on Windows or UNIX systems running Samba. It provides a web interface for
searching files. It is optimized for searching files by a wildcard when there
are some normal (not '*' or '?') chars specified in the beginning or in the end
of the mask (for example '*.iso').

%description -l pl
todo

%prep
%setup -q

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_phpdir},%{_sysconfdir},%{_libdir}/%{name}/bin}

cp -r htdocs/ffsearch/*		$RPM_BUILD_ROOT%{_phpdir}
install bin/* makedb.pl		$RPM_BUILD_ROOT%{_libdir}/%{name}/bin
install %{name}.conf		$RPM_BUILD_ROOT%{_sysconfdir}

install -D %{SOURCE1} $RPM_BUILD_ROOT/etc/cron.d/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%pre
if [ -n "`getgid ffsearch`" ]; then
	if [ "`getgid ffsearch`" != "91" ]; then
		echo "Error: group ffsearch doesn't have gid=118. Correct this before installing ffsearch." 1>&2
		exit 1
	fi
else
	/usr/sbin/groupadd -g 118 -r -f ffsearch 1>&2 || :
fi
if [ -n "`id -u ffsearch 2>/dev/null`" ]; then
	if [ "`id -u ffsearch`" != "118" ]; then
		echo "Error: user ffsearch doesn't have uid=118. Correct this before installing ffsearch." 1>&2
		exit 1
	fi
else
	/usr/sbin/useradd -M -o -r -u 118 -s /bin/false \
		-g ffsearch -c "Fast File Search user" -d %{_phpdir} ffsearch 1>&2 || :
fi

%postun
if [ "$1" = "0" ]; then
	/usr/sbin/userdel ffsearch
	/usr/sbin/groupdel ffsearch
fi

%files
%defattr(644,root,root,755)
%doc INSTALL README MAINTAINERS UPGRADE
%attr(750,root,ffsearch) %dir %{_libdir}/%{name}
%attr(750,root,ffsearch) %dir %{_libdir}/%{name}/bin
%attr(750,root,ffsearch) %{_libdir}/%{name}/bin/*.pl
%attr(640,ffsearch,ffsearch) %config(noreplace) %{_sysconfdir}/%{name}.conf
%attr(750,root,http) %dir %{_phpdir}
%attr(640,root,http) %{_phpdir}/*.php
%attr(640,root,http) %{_phpdir}/*.css
%attr(640,root,http) %{_phpdir}/*.gif
%attr(640,root,http) %{_phpdir}/*.png
%attr(640,root,http) %{_phpdir}/flag
%attr(640,root,http) %{_phpdir}/lang
%attr(640,root,root) /etc/cron.d/%{name}
