%include	/usr/lib/rpm/macros.perl
Summary:	Fast File Search
Summary(pl):	Szybka wyszukiwarka plików
Name:		ffsearch
Version:	1.1.8
Release:	1
License:	GPL v2
Group:		Applications/WWW
Source0:	http://dl.sourceforge.net/ffsearch/%{name}-%{version}.tar.bz2
# Source0-md5:	b634646e8b8fc13d316a7656d24e392d
Source1:	%{name}.crond
URL:		http://ffsearch.sf.net/
BuildRequires:	rpm-perlprov >= 4.1-13
Requires(pre):	/usr/bin/getgid
Requires(pre):	/bin/id
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires:	php >= 4.0.3
Requires:	webserver
Requires:	perl-DBD-mysql
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_phpdir		/home/services/httpd/html/ffsearch

%description
Fast File Search is a crawler for FTP servers and SMB shares that can
be found on Windows or UNIX systems running Samba. It provides a web
interface for searching files. It is optimized for searching files by
a wildcard when there are some normal (not '*' or '?') chars specified
in the beginning or in the end of the mask (for example '*.iso').

%description -l pl
Fast File Search (szybka wyszukiwarka plików) jest skryptem
zbieraj±cym informacje o udostêpnianych zasobach FTP i SMB. Udostêpnia
przyjemny interfejs WWW do wyszukiwania plików. Jest zoptymalizowana
do wyszukiwania plików przez podanie masek plików ze sta³± czê¶ci± na
pocz±tku lub koñcu nazwy (na przyk³ad *.iso).

%prep
%setup -q

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_phpdir},%{_sysconfdir},%{_libdir}/%{name}/bin,/var/{log/{,archiv/}%{name},lock/%{name}}}
rm -rf {bin,flag,lang,htdocs/ffsearch/{,flag,lang},doc}/CVS

cp -r htdocs/ffsearch/*		$RPM_BUILD_ROOT%{_phpdir}
install bin/*			$RPM_BUILD_ROOT%{_libdir}/%{name}/bin
install makedb.pl		$RPM_BUILD_ROOT%{_libdir}/%{name}
install %{name}.conf		$RPM_BUILD_ROOT%{_sysconfdir}

install -D %{SOURCE1} $RPM_BUILD_ROOT/etc/cron.d/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%pre
if [ -n "`getgid ffsearch`" ]; then
	if [ "`getgid ffsearch`" != "118" ]; then
		echo "Error: group ffsearch doesn't have gid=118. Correct this before installing ffsearch." 1>&2
		exit 1
	fi
else
	/usr/sbin/groupadd -g 118 -r -f ffsearch 1>&2
fi
if [ -n "`id -u ffsearch 2>/dev/null`" ]; then
	if [ "`id -u ffsearch`" != "118" ]; then
		echo "Error: user ffsearch doesn't have uid=118. Correct this before installing ffsearch." 1>&2
		exit 1
	fi
else
	/usr/sbin/useradd -M -o -r -u 118 -s /bin/false \
		-g ffsearch -c "Fast File Search user" -d %{_libdir}/%{name} ffsearch 1>&2
fi

%postun
if [ "$1" = "0" ]; then
	/usr/sbin/userdel ffsearch
	/usr/sbin/groupdel ffsearch
fi

%files
%defattr(644,root,root,755)
%doc INSTALL README MAINTAINERS UPGRADE AUTHORS ChangeLog doc/*
%attr(750,root,ffsearch) %dir %{_libdir}/%{name}
%attr(750,root,ffsearch) %dir %{_libdir}/%{name}/bin
%attr(750,root,ffsearch) %{_libdir}/%{name}/bin/*.pl
%attr(750,root,ffsearch) %{_libdir}/%{name}/*.pl
%attr(640,ffsearch,ffsearch) %verify(not md5 size mtime) %config(noreplace) %{_sysconfdir}/%{name}.conf
%attr(640,ffsearch,http) %verify(not md5 size mtime) %config(noreplace) %{_phpdir}/config.php
%attr(750,root,http) %dir %{_phpdir}
%attr(640,root,http) %{_phpdir}/a*.php
%attr(640,root,http) %{_phpdir}/body.php
%attr(640,root,http) %{_phpdir}/browse.php
%attr(640,root,http) %{_phpdir}/colors.php
%attr(640,root,http) %{_phpdir}/comment*.php
%attr(640,root,http) %{_phpdir}/db.php
%attr(640,root,http) %{_phpdir}/f*.php
%attr(640,root,http) %{_phpdir}/h*.php
%attr(640,root,http) %{_phpdir}/index.php
%attr(640,root,http) %{_phpdir}/lang.php
%attr(640,root,http) %{_phpdir}/menu*.php
%attr(640,root,http) %{_phpdir}/s*.php
%attr(640,root,http) %{_phpdir}/t*.php
%attr(640,root,http) %{_phpdir}/vars.php
%attr(640,root,http) %{_phpdir}/*.css
%attr(640,root,http) %{_phpdir}/*.gif
%attr(640,root,http) %{_phpdir}/*.png
%attr(750,root,http) %{_phpdir}/flag
%attr(750,root,http) %{_phpdir}/lang
%attr(640,root,root) /etc/cron.d/%{name}
%attr(750,ffsearch,ffsearch) %dir /var/lock/%{name}
%attr(750,ffsearch,ffsearch) %dir /var/log/%{name}
%attr(750,ffsearch,ffsearch) %dir /var/log/archiv/%{name}
