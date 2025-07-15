#
# Conditional build:
%bcond_without	apidocs		# gi-docgen based API documentation
%bcond_with	libsoup2	# libsoup 2.x instead of libsoup3 (discouraged, better use rest 0.7 for soup2)
%bcond_without	static_libs	# static library

%define		apiver	1.0
Summary:	A library for access to RESTful web services
Summary(pl.UTF-8):	Biblioteka dostępu do REST-owych serwisów WWW
Name:		rest1
Version:	0.9.1
Release:	4
License:	LGPL v2
Group:		Libraries
Source0:	https://download.gnome.org/sources/rest/0.9/rest-%{version}.tar.xz
# Source0-md5:	b997b83232be3814a1b78530c5700df9
URL:		https://www.gnome.org/
BuildRequires:	glib2-devel >= 1:2.44
BuildRequires:	gobject-introspection-devel >= 0.6.7
%{?with_apidocs:BuildRequires:	gi-docgen >= 2021.6}
BuildRequires:	json-glib-devel
%if %{with libsoup2}
BuildRequires:	libsoup-devel >= 2.42
%else
BuildRequires:	libsoup3-devel >= 3.0
%endif
BuildRequires:	libxml2-devel >= 2
BuildRequires:	meson >= 0.56
BuildRequires:	ninja >= 1.5
BuildRequires:	pkgconfig
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 2.029
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	glib2 >= 1:2.44
%if %{with libsoup2}
Requires:	libsoup >= 2.42
%else
Requires:	libsoup3 >= 3.0
%endif
Suggests:	ca-certificates
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This library was designed to make it easier to access web services
that claim to be "RESTful". A RESTful service should have URLs that
represent remote objects, which methods can then be called on. The
majority of services don't actually adhere to this strict definition.
Instead, their RESTful end point usually has an API that is just
simpler to use compared to other types of APIs they may support
(XML-RPC, for instance). It is this kind of API that this library is
attempting to support.

%description -l pl.UTF-8
Ta biblioteka została zaprojektowana, aby ułatwić dostęp do serwisów
WWW, które uznają się za "REST-owe". Serwis REST-owy powinien mieć
URL-e reprezentujące zdalne obiekty, na których można wywoływać
metody. Większość serwisów nie jest w pełni zgodna z tą definicją, ale
ich REST-owy interfejs zwykle ma API prostsze od innych (np. XML-RPC).
Ten rodzaj API próbuje obsłużyć ta biblioteka.

%package devel
Summary:	Header files for rest library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki rest
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	glib2-devel >= 1:2.44
Requires:	json-glib-devel
%if %{with libsoup2}
Requires:	libsoup-devel >= 2.42
%else
Requires:	libsoup3-devel >= 3.0
%endif
Requires:	libxml2-devel >= 2

%description devel
Header files for rest library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki rest.

%package static
Summary:	Static rest library
Summary(pl.UTF-8):	Statyczna biblioteka rest
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static rest library.

%description static -l pl.UTF-8
Statyczna biblioteka rest.

%package apidocs
Summary:	rest API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki rest
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for rest library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki rest.

%prep
%setup -q -n rest-%{version}

%build
%meson build \
	%{!?with_static_libs:--default-library=shared} \
	-Dexamples=false \
	%{!?with_apidocs:-Dgtk_doc=false} \
	%{?with_libsoup2:-Dsoup2=true}

# -Dvapi=true not enabled, rest-1.0 is included in vala 0.56

%ninja_build -C build

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

%if %{with apidocs}
install -d $RPM_BUILD_ROOT%{_gidocdir}
%{__mv} $RPM_BUILD_ROOT%{_docdir}/librest-1.0 $RPM_BUILD_ROOT%{_gidocdir}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS NEWS README.md
%attr(755,root,root) %{_libdir}/librest-%{apiver}.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/librest-%{apiver}.so.0
%attr(755,root,root) %{_libdir}/librest-extras-%{apiver}.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/librest-extras-%{apiver}.so.0
%{_libdir}/girepository-1.0/Rest-%{apiver}.typelib
%{_libdir}/girepository-1.0/RestExtras-%{apiver}.typelib

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/librest-%{apiver}.so
%attr(755,root,root) %{_libdir}/librest-extras-%{apiver}.so
%{_datadir}/gir-1.0/Rest-%{apiver}.gir
%{_datadir}/gir-1.0/RestExtras-%{apiver}.gir
%{_includedir}/rest-%{apiver}
%{_pkgconfigdir}/rest-%{apiver}.pc
%{_pkgconfigdir}/rest-extras-%{apiver}.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/librest-%{apiver}.a
%{_libdir}/librest-extras-%{apiver}.a
%endif

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gidocdir}/librest-%{apiver}
%endif
