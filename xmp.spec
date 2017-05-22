#
# Conditional build:
%bcond_without	pulseaudio	# PulseAudio audio output driver
#
Summary:	Extended Module Player
Summary(pl.UTF-8):	Extended Module Player - rozszerzony odtwarzacz modułów
Name:		xmp
Version:	4.1.0
Release:	1
License:	GPL v2+
Group:		Applications/Sound
Source0:	http://downloads.sourceforge.net/xmp/%{name}-%{version}.tar.gz
# Source0-md5:	d9661b0be1a7ec79fd6185b166c4e9dd
URL:		http://xmp.sourceforge.net/
BuildRequires:	alsa-lib-devel
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	libxmp-devel >= 4.4
BuildRequires:	pkgconfig
%{?with_pulseaudio:BuildRequires:	pulseaudio-devel}
Requires:	libxmp >= 4.4
Obsoletes:	xmp-X11
Obsoletes:	xmp-output-arts
Obsoletes:	xmp-output-esd
Obsoletes:	xmp-output-nas
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is the Extended Module Player, a portable module player that
plays over 90 mainstream and obscure module formats, including
Protracker MOD, Fasttracker II XM, Scream Tracker 3 S3M and Impulse
Tracker IT files.

%description -l pl.UTF-8
XMP (Extended Module Player - rozszerzony odtwarzacz modułów) to
przenośny odtwarzacz modułów muzycznych, znający ponad 90 głównych i
mniej znanych formatów, w tym: Protracker (MOD), Scream Tracker 3
(S3M), Fast Tracker II (XM) oraz Impulse Tracker (IT).

%prep
%setup -q

%build
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	%{!?with_pulseaudio:--disable-pulseaudio} \
	--disable-silent-rules

%{__make}
# -j1 \
#	V=1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc CREDITS Changelog README
%dir %{_sysconfdir}/xmp
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/xmp/modules.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/xmp/xmp.conf
%attr(755,root,root) %{_bindir}/xmp
%{_mandir}/man1/xmp.1*
