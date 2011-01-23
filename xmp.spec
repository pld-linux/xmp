# TODO: bmp, audacious plugins
#
# Conditional build:
%bcond_with	arts		# aRts audio driver
%bcond_with	esd		# EsounD audio output driver
%bcond_without	nas		# NAS audio output driver
%bcond_without	pulseaudio	# PulseAudio audio output driver
%bcond_without	xmms		# XMP as XMMS plugin
%bcond_with	nonfree		# with recent fmopl (GPL-incompatible - non-distributable)
#
Summary:	Extended Module Player
Summary(pl.UTF-8):	Rozszerzony odtwarzacz modułów
Name:		xmp
Version:	3.3.0
Release:	1
License:	GPL%{?with_nonfree: with non-commercial additions}
Group:		Applications/Sound
Source0:	http://downloads.sourceforge.net/xmp/%{name}-%{version}.tar.gz
# Source0-md5:	0ac15cdb68cf0a08f418d37b4c1843bd
Patch0:		%{name}-nondfsg.patch
URL:		http://xmp.sourceforge.net/
%{?with_arts:BuildRequires:	arts-devel}
BuildRequires:	autoconf
BuildRequires:	automake
%{?with_esd:BuildRequires:	esound-devel}
%{?with_nas:BuildRequires:	nas-devel}
BuildRequires:	pkgconfig
%{?with_pulseaudio:BuildRequires:	pulseaudio-devel}
%{?with_xmms:BuildRequires:	rpmbuild(macros) >= 1.125}
%{?with_xmms:BuildRequires:	xmms-devel}
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXt-devel
Obsoletes:	xmp-X11
Obsoletes:	xmp-output-arts
Obsoletes:	xmp-output-esd
Obsoletes:	xmp-output-nas
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
xmp is a multi-format module player for UNIX. In machines with GUS or
AWE cards xmp takes advantage of the OSS sequencer to play modules
with virtually no system load. Using software mixing, xmp plays at
sampling rates up to 48kHz in mono or stereo, 8 or 16 bits, signed or
unsigned, little or big endian samples with 32 bit linear
interpolation.

%description -l pl.UTF-8
xmp jest odtwarzaczem modułów w wielu formatach. Potrafi obsłużyć
karty GUS i AWE, korzystając z sekwencera OSS, aby nie obciążać
systemu. Używając programowego miksowania, może odgrywać z
częstotliwością próbkowania do 48kHz mono lub stereo, 8 lub 16 bitów,
próbki ze znakiem lub bez, little- lub big-endian z 32-bitową
interpolacją.

%package -n xmms-input-xmp
Summary:	XMMS plugin that uses XMP library to play music modules
Summary(pl.UTF-8):	Wtyczka dla XMMS-a odtwarzająca moduły dźwiękowe z użyciem XMP
Group:		X11/Applications/Sound
Requires:	%{name} = %{version}-%{release}
Requires:	xmms

%description -n xmms-input-xmp
XMMS plugin that uses XMP library to play music modules.

%description -n xmms-input-xmp -l pl.UTF-8
Wtyczka dla XMMS-a odtwarzająca moduły dźwiękowe z użyciem biblioteki
XMP.

%prep
%setup -q
%{?with_nonfree:%patch0 -p1}

%build
cp -f /usr/share/automake/config.* scripts
%{__aclocal}
%{__autoconf}
%configure \
	%{?with_arts:--enable-arts} \
	%{?with_esd:--enable-esd} \
	%{?with_nas:--enable-nas} \
	%{?with_pulseaudio:--enable-pulseaudio} \
	%{?with_xmms:--enable-xmms-plugin}
%{__make} -j1 \
	V=1

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
%doc README docs/{CREDITS,ChangeLog,README.{awebug,fixloop,trackers,unsqsh},formats}
%dir %{_sysconfdir}/xmp
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/xmp/modules.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/xmp/xmp.conf
%attr(755,root,root) %{_bindir}/xmp
%{_mandir}/man1/xmp.1*

%if %{with xmms}
%files -n xmms-input-xmp
%defattr(644,root,root,755)
%attr(755,root,root) %{xmms_input_plugindir}/xmp-xmms.so
%endif
