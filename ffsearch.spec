%include	/usr/lib/rpm/macros.perl
Summary:	Fast File Search
Summary(pl):	Szybka wyszukiwarka plików
Name:		ffsearch
Version:	1.1.12
Release:	3
License:	GPL v2
Group:		Applications/WWW
Source0:	http://dl.sourceforge.net/ffsearch/%{name}-%{version}.tar.bz2
# Source0-md5:	37fd70f94431c70198f5fa2031b4f9ac
Source1:	%{name}.crond
Patch0:		%{name}-config.patch
URL:		http://ffsearch.sourceforge.net/
BuildRequires:	rpm-perlprov >= 4.1-13
BuildRequires:	rpmbuild(macros) >= 1.202
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires:	perl-DBD-mysql
Requires:	php >= 4.0.3
Requires:	webserver
Provides:	group(ffsearch)
Provides:	user(ffsearch)
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_phpdir		%{_datadir}/%{name}/www

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
%patch0 -p1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_phpdir},%{_sysconfdir}/%{name},%{_datadir}/%{name}/bin,/var/{log/{,archiv/}%{name},lock/%{name}}}
rm -rf {bin,flag,lang,htdocs/ffsearch/{,flag,lang},doc}/CVS

cp -r htdocs/ffsearch/*		$RPM_BUILD_ROOT%{_phpdir}
install bin/*			$RPM_BUILD_ROOT%{_datadir}/%{name}/bin
install makedb.pl		$RPM_BUILD_ROOT%{_datadir}/%{name}
install %{name}.conf		$RPM_BUILD_ROOT%{_sysconfdir}

mv $RPM_BUILD_ROOT%{_phpdir}/config.php $RPM_BUILD_ROOT%{_sysconfdir}/%{name}
ln -sf %{_sysconfdir}/%{name}/config.php $RPM_BUILD_ROOT%{_phpdir}/config.php

install -D %{SOURCE1} $RPM_BUILD_ROOT/etc/cron.d/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g 118 ffsearch
%useradd -u 118 -s /bin/false -g ffsearch -c "Fast File Search user" -d %{_datadir}/ffsearch ffsearch

%postun
if [ "$1" = "0" ]; then
	%userremove ffsearch
	%groupremove ffsearch
fi

%files
%defattr(644,root,root,755)
%doc INSTALL README MAINTAINERS UPGRADE AUTHORS ChangeLog doc/*
%attr(750,root,ffsearch) %dir %{_datadir}/%{name}
%attr(750,root,ffsearch) %dir %{_datadir}/%{name}/bin
%attr(750,root,ffsearch) %{_datadir}/%{name}/bin/*.pl
%attr(750,root,ffsearch) %{_datadir}/%{name}/*.pl
%attr(640,ffsearch,ffsearch) %verify(not md5 mtime size) %config(noreplace) %{_sysconfdir}/%{name}.conf
%attr(640,ffsearch,http) %verify(not md5 mtime size) %config(noreplace) %{_sysconfdir}/%{name}/config.php
%{_phpdir}/config.php
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
