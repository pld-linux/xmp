Summary:	Extended Module Player
Name:		xmp
Version:	2.0.3
Release:	2
URL:		http://xmp.helllabs.org
Group:		Applications/Sound
Group(de):	Applikationen/Laut
Group(pl):	Aplikacje/D¼wiêk
Source0:	http://xmp.helllabs.org/pkg/%{version}/%{name}-%{version}.tar.bz2
License:	GPL
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
BuildRequires:	XFree86-devel

%define		_xbindir	/usr/X11R6/bin
%define		_xmandir	/usr/X11R6/man

%description
xmp is a multi-format module player for UNIX. In machines with GUS or
AWE cards xmp takes advantage of the OSS sequencer to play modules
with virtually no system load. Using software mixing, xmp plays at
sampling rates up to 48kHz in mono or stereo, 8 or 16 bits, signed or
unsigned, little or big endian samples with 32 bit linear
interpolation.

%prep
%setup -q

%build
aclocal
autoconf
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_bindir},%{_xbindir},{%{_mandir},%{_xmandir}}/man1}
install etc/xmp-modules.conf etc/xmp.conf $RPM_BUILD_ROOT%{_sysconfdir}
install src/main/xmp $RPM_BUILD_ROOT%{_bindir}
install src/main/xxmp $RPM_BUILD_ROOT%{_xbindir}
install docs/xmp.1 $RPM_BUILD_ROOT%{_mandir}/man1
install docs/xxmp.1 $RPM_BUILD_ROOT%{_xmandir}/man1

gzip -9nf README docs/{CREDITS,ChangeLog,README.fixloop,README.trackers,README.unsqsh} etc/magic

%clean
rm -rf $RPM_BUILD_ROOT

%post

%files
%defattr(644,root,root,755)
%doc *.gz docs/*.gz etc/*.gz
%config %{_sysconfdir}/*
%attr(755,root,root) %{_bindir}/xmp
%attr(755,root,root) %{_xbindir}/xxmp
%{_mandir}/man1/*
%{_xmandir}/man1/*
