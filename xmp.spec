#
# Conditional build:
%bcond_without	arts		# without aRts audio plugin
%bcond_without	esd		# without EsounD audio output plugin
%bcond_without	nas		# without NAS audio output plugin
%bcond_without	xmms		# without XMP as XMMS plugin
%bcond_with	nonfree		# with ppunpack and fmopl (GPL-incompatible - non-distributable)
#
Summary:	Extended Module Player
Summary(pl):	Rozszerzony odtwarzacz modu��w
Name:		xmp
Version:	2.0.5
%define	pver	pre3
Release:	0.%{pver}.2
License:	GPL%{?with_nonfree: with non-commercial additions}
Group:		Applications/Sound
Source0:	http://dl.sourceforge.net/%{name}/%{name}-%{version}%{pver}.tar.bz2
# Source0-md5:	749db9c8da956b403a959b4c8b909447
Patch0:		%{name}-gcc33.patch
Patch1:		%{name}-fix-shared.patch
Patch2:		%{name}-load-fix.patch
Patch3:		%{name}-nondfsg.patch
URL:		http://xmp.sourceforge.net/
BuildRequires:	XFree86-devel
%{?with_arts:BuildRequires:	arts-devel}
BuildRequires:	autoconf
BuildRequires:	automake
%{?with_esd:BuildRequires:	esound-devel}
%{?with_nas:BuildRequires:	nas-devel}
%{?with_xmms:BuildRequires:	rpmbuild(macros) >= 1.125}
%{?with_xmms:BuildRequires:	xmms-devel}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
xmp is a multi-format module player for UNIX. In machines with GUS or
AWE cards xmp takes advantage of the OSS sequencer to play modules
with virtually no system load. Using software mixing, xmp plays at
sampling rates up to 48kHz in mono or stereo, 8 or 16 bits, signed or
unsigned, little or big endian samples with 32 bit linear
interpolation.

%description -l pl
xmp jest odtwarzaczem modu��w w wielu formatach. Potrafi obs�u�y�
karty GUS i AWE, korzystaj�c z sekwencera OSS, aby nie obci��a�
systemu. U�ywaj�c programowego miksowania, mo�e odgrywa� z
cz�stotliwo�ci� pr�bkowania do 48kHz mono lub stereo, 8 lub 16 bit�w,
pr�bki ze znakiem lub bez, little- lub big-endian z 32-bitow�
interpolacj�.

%package X11
Summary:	Extended Module Player with GUI
Summary(pl):	Rozszerzony odtwarzacz modu��w z graficznym interfejsem
Group:		X11/Applications/Sound
Requires:	%{name} = %{version}

%description X11
Extended Module Player with GUI.

%description X11 -l pl
Rozszerzony odtwarzacz modu��w z graficznym interfejsem.

%package output-arts
Summary:	aRts audio output plugin for XMP
Summary(pl):	Wtyczka wyj�cia d�wi�ku aRts dla XMP
Group:		Applications/Sound
Requires:	%{name} = %{version}

%description output-arts
aRts audio output plugin for XMP.

%description output-arts -l pl
Wtyczka wyj�cia d�wi�ku aRts dla XMP.

%package output-esd
Summary:	EsounD audio output plugin for XMP
Summary(pl):	Wtyczka wyj�cia d�wi�ku EsounD dla XMP
Group:		Applications/Sound
Requires:	%{name} = %{version}

%description output-esd
EsounD audio output plugin for XMP.

%description output-esd -l pl
Wtyczka wyj�cia d�wi�ku EsounD dla XMP.

%package output-nas
Summary:	NAS audio output plugin for XMP
Summary(pl):	Wtyczka wyj�cia d�wi�ku NAS dla XMP
Group:		Applications/Sound
Requires:	%{name} = %{version}

%description output-nas
NAS audio output plugin for XMP.

%description output-nas -l pl
Wtyczka wyj�cia d�wi�ku NAS dla XMP.

%package -n xmms-input-xmp
Summary:	XMMS plugin that uses XMP library to play music modules
Summary(pl):	Wtyczka XMMS odtwarzaj�ca modu�y d�wi�kowe z u�yciem XMP
Group:		X11/Applications/Sound
Requires:	%{name}-%{version}
Requires:	xmms

%description -n xmms-input-xmp
XMMS plugin that uses XMP library to play music modules.

%description -n xmms-input-xmp -l pl
Wtyczka XMMS odtwarzaj�ca modu�y d�wi�kowe z u�yciem biblioteki XMP.

%prep
%setup -q -n %{name}-%{version}-%{pver}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%{?with_nonfree:%patch3 -p1}

%build
cp -f /usr/share/automake/config.* scripts
%{__aclocal}
%{__autoconf}
# alsa disabled - only 0.5 supported for now
%configure \
	--disable-alsa \
	%{!?with_arts:--disable-arts} \
	%{!?with_esd:--disable-esd} \
	%{!?with_nas:--disable-nas} \
	%{!?with_xmms:--disable-xmms} \
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

%if %{with arts}
%files output-arts
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/xmp/drivers/arts.so
%endif

%if %{with esd}
%files output-esd
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/xmp/drivers/esd.so
%endif

%if %{with nas}
%files output-nas
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/xmp/drivers/nas.so
%endif

%if %{with xmms}
%files -n xmms-input-xmp
%defattr(644,root,root,755)
%attr(755,root,root) %{xmms_input_plugindir}/*.so
%endif
