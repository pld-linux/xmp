#
# Conditional build:
# _without_arts	- without aRts audio plugin
# _without_esd	- without EsounD audio output plugin
# _without_nas	- without NAS audio output plugin
# _without_xmms	- without XMP as XMMS plugin
# _with_nonfree	- with ppunpack and fmopl (GPL-incompatible - non-distributable)
#
Summary:	Extended Module Player
Summary(pl):	Rozszerzony odtwarzacz modu³ów
Name:		xmp
Version:	2.0.5
%define	pver	pre3
Release:	0.%{pver}.2
License:	GPL%{?_with_nonfree: with non-commercial additions}
Group:		Applications/Sound
Source0:	http://dl.sourceforge.net/%{name}/%{name}-%{version}%{pver}.tar.bz2
# Source0-md5:	749db9c8da956b403a959b4c8b909447
Patch0:		%{name}-gcc33.patch
Patch1:		%{name}-fix-shared.patch
Patch2:		%{name}-load-fix.patch
Patch3:		%{name}-nondfsg.patch
URL:		http://xmp.sourceforge.net/
BuildRequires:	XFree86-devel
%{!?_without_arts:BuildRequires:	arts-devel}
BuildRequires:	autoconf
BuildRequires:	automake
%{!?_without_esd:BuildRequires:	esound-devel}
%{!?_without_nas:BuildRequires:	nas-devel}
%{!?_without_xmms:BuildRequires:	rpmbuild(macros) >= 1.125}
%{!?_without_xmms:BuildRequires:	xmms-devel}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
xmp is a multi-format module player for UNIX. In machines with GUS or
AWE cards xmp takes advantage of the OSS sequencer to play modules
with virtually no system load. Using software mixing, xmp plays at
sampling rates up to 48kHz in mono or stereo, 8 or 16 bits, signed or
unsigned, little or big endian samples with 32 bit linear
interpolation.

%description -l pl
xmp jest odtwarzaczem modu³ów w wielu formatach. Potrafi obs³u¿yæ
karty GUS i AWE, korzystaj±c z sekwencera OSS, aby nie obci±¿aæ
systemu. U¿ywaj±c programowego miksowania, mo¿e odgrywaæ z
czêstotliwo¶ci± próbkowania do 48kHz mono lub stereo, 8 lub 16 bitów,
próbki ze znakiem lub bez, little- lub big-endian z 32-bitow±
interpolacj±.

%package X11
Summary:	Extended Module Player with GUI
Summary(pl):	Rozszerzony odtwarzacz modu³ów z graficznym interfejsem
Group:		X11/Applications/Sound
Requires:	%{name} = %{version}

%description X11
Extended Module Player with GUI.

%description X11 -l pl
Rozszerzony odtwarzacz modu³ów z graficznym interfejsem.

%package output-arts
Summary:	aRts audio output plugin for XMP
Summary(pl):	Wtyczka wyj¶cia d¼wiêku aRts dla XMP
Group:		Applications/Sound
Requires:	%{name} = %{version}

%description output-arts
aRts audio output plugin for XMP.

%description output-arts -l pl
Wtyczka wyj¶cia d¼wiêku aRts dla XMP.

%package output-esd
Summary:	EsounD audio output plugin for XMP
Summary(pl):	Wtyczka wyj¶cia d¼wiêku EsounD dla XMP
Group:		Applications/Sound
Requires:	%{name} = %{version}

%description output-esd
EsounD audio output plugin for XMP.

%description output-esd -l pl
Wtyczka wyj¶cia d¼wiêku EsounD dla XMP.

%package output-nas
Summary:	NAS audio output plugin for XMP
Summary(pl):	Wtyczka wyj¶cia d¼wiêku NAS dla XMP
Group:		Applications/Sound
Requires:	%{name} = %{version}

%description output-nas
NAS audio output plugin for XMP.

%description output-nas -l pl
Wtyczka wyj¶cia d¼wiêku NAS dla XMP.

%package -n xmms-input-xmp
Summary:	XMMS plugin that uses XMP library to play music modules
Summary(pl):	Wtyczka XMMS odtwarzaj±ca modu³y d¼wiêkowe z u¿yciem XMP
Group:		X11/Applications/Sound
Requires:	%{name}-%{version}
Requires:	xmms

%description -n xmms-input-xmp
XMMS plugin that uses XMP library to play music modules.

%description -n xmms-input-xmp -l pl
Wtyczka XMMS odtwarzaj±ca modu³y d¼wiêkowe z u¿yciem biblioteki XMP.

%prep
%setup -q -n %{name}-%{version}-%{pver}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%{?_with_nonfree:%patch3 -p1}

%build
cp -f /usr/share/automake/config.* scripts
%{__aclocal}
%{__autoconf}
# alsa disabled - only 0.5 supported for now
%configure \
	--disable-alsa \
	%{?_without_arts:--disable-arts} \
	%{?_without_esd:--disable-esd} \
	%{?_without_nas:--disable-nas} \
	%{?_without_xmms:--disable-xmms} \
	--enable-dynamic
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}

%{__make} install \
	DEST_DIR=$RPM_BUILD_ROOT \
	BIN_DIR=$RPM_BUILD_ROOT%{_bindir} \
	LIB_DIR=$RPM_BUILD_ROOT%{_libdir} \
	MAN_DIR=$RPM_BUILD_ROOT%{_mandir}/man1

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README docs/{CREDITS,ChangeLog,README.{awebug,fixloop,ppunpack,trackers,unsqsh},formats} etc/magic
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/xmp*.conf
%attr(755,root,root) %{_bindir}/xmp
%attr(755,root,root) %{_libdir}/lib*.so.*.*.*
%dir %{_libdir}/xmp
%dir %{_libdir}/xmp/drivers
%attr(755,root,root) %{_libdir}/xmp/drivers/oss*.so
%{_mandir}/man1/xmp.1*

%files X11
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/xxmp
%{_mandir}/man1/xxmp.1*

%if 0%{!?_without_arts:1}
%files output-arts
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/xmp/drivers/arts.so
%endif

%if 0%{!?_without_esd:1}
%files output-esd
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/xmp/drivers/esd.so
%endif

%if 0%{!?_without_nas:1}
%files output-nas
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/xmp/drivers/nas.so
%endif

%if 0%{!?_without_xmms:1}
%files -n xmms-input-xmp
%defattr(644,root,root,755)
%attr(755,root,root) %{xmms_input_plugindir}/*.so
%endif
