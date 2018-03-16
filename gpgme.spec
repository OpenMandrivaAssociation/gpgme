%define major 11
%define gpgmepp_major 6
%define qgpgme_major 7
%define libname %mklibname %{name} %{major}
%define libgpgmepp %mklibname %{name}pp %{gpgmepp_major}
%define devgpgmepp %mklibname %{name}pp -d
%define libqgpgme %mklibname qgpgme %{qgpgme_major}
%define devqgpgme %mklibname qgpgme -d
%define devname %mklibname %{name} -d
# Doesn't exist anymore, but needs to be obsoleted
%define libpthread %mklibname %{name}_pthread 11

%define gpgsm_version 1.9.6

Summary:	GnuPG Made Easy (GPGME)
Name:		gpgme
Version:	1.10.0
Release:	3
License:	GPLv2+
Group:		File tools
Url:		http://www.gnupg.org/gpgme.html
Source0:	ftp://ftp.gnupg.org/gcrypt/gpgme/%{name}-%{version}.tar.bz2
Patch0:		gpgme-1.8.0-fix-gpgmepp-cmake-linkage.patch

# support for Cryptographic Message Syntax protocol
BuildRequires:	gnupg >= %{gpgsm_version}
BuildRequires:	libassuan-devel >= 2.0.2
BuildRequires:	pth-devel >= 2.0.0
BuildRequires:	pkgconfig(gpg-error)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(Qt5Core)
BuildRequires:	pkgconfig(Qt5Test)

# OK to disable for bootstrapping
# Just causes QGpgme docs to be nicer
BuildRequires:	graphviz

%description
GnuPG Made Easy (GPGME) is a library designed to make access to GnuPG
easier for applications.

%package -n %{libname}
Summary:	GnuPG Made Easy (GPGME)
Group:		System/Libraries
# support for Cryptographic Message Syntax protocol
Recommends:	gnupg >= %{gpgsm_version}
Provides:	%{name} = %{version}-%{release}
Conflicts:	%{_lib}gpgme11 < 1.3.2-3
Obsoletes:	%{libpthread} < %{EVRD}

%description -n %{libname}
GnuPG Made Easy (GPGME) is a library designed to make access to GnuPG
easier for applications.

%package -n %{libgpgmepp}
Summary:	GnuPG Made Easy (GPGME)
Group:		System/Libraries
Obsoletes:	%{_lib}GppMePp-devel

%description -n %{libgpgmepp}
GnuPG Made Easy (GPGME) is a library designed to make access to GnuPG
easier for applications.

%package -n %{libqgpgme}
Summary:	Qt bindings to GnuPG Made Easy (GPGME)
Group:		System/Libraries

%description -n %{libqgpgme}
Qt bindings to GnuPG Made Easy (GPGME), a library designed to make access
to GnuPG easier for applications.

%package -n %{devgpgmepp}
Summary:	GnuPG Made Easy (GPGME) Header files and libraries for development
Group:		Development/C++
Requires:	%{devname} = %{EVRD}
Requires:	%{libgpgmepp} = %{EVRD}
Provides:	%{name}pp-devel = %{EVRD}
Provides:	%{name}++-devel = %{EVRD}
Conflicts:	kdepimlibs4-devel >= 3:4.14.10
Obsoletes:	%{_lib}GpgMePp-devel

%description -n %{devgpgmepp}
GnuPG Made Easy (GPGME) is a library designed to make access to GnuPG
easier for applications.

Install this package if you want to develop applications that will use
the %{name} library for crypto awareness.

%package -n %{devqgpgme}
Summary:	GnuPG Made Easy (GPGME) Header files and libraries for development
Group:		Development/C++
Requires:	%{devname} = %{EVRD}
Requires:	%{libqgpgme} = %{EVRD}
Conflicts:	kdepimlibs4-devel

%description -n %{devqgpgme}
GnuPG Made Easy (GPGME) is a library designed to make access to GnuPG
easier for applications.

Install this package if you want to develop applications that will use
the %{name} library for crypto awareness.

%package -n %{devname}
Summary:	GnuPG Made Easy (GPGME) Header files and libraries for development
Group:		Development/C
Requires:	%{libname} = %{EVRD}
Provides:	%{name}-devel = %{EVRD}
Obsoletes:	%{_lib}gpgme-devel-static < 1.7.1

%description -n %{devname}
Install this package if you want to develop applications 
that will use the %{name} library for crypto awareness.

%package -n python-gpg
Summary:	Python bindings to GPG encryption
Group:		Development/Python
Requires:	%{libname} = %{EVRD}
BuildRequires:	pkgconfig(python3)
BuildRequires:	swig

%description -n python-gpg
Python bindings to GPG encryption

%package -n python2-gpg
Summary:	Python 2.x bindings to GPG encryption
Group:		Development/Python
Requires:	%{libname} = %{EVRD}
BuildRequires:	pkgconfig(python2)
BuildRequires:	swig

%description -n python2-gpg
Python 2.x bindings to GPG encryption

%package doc
Summary:	Documentation for GnuPG Made Easy (GPGME)
Group:		Books/Computer books
Requires:	%{libname} = %{EVRD}

%description doc
Documentation for GnuPG Made Easy (GPGME).

%prep
%setup -q
%apply_patches

%build
%configure
%make

#check
#make check

%install
%makeinstall_std

%if %{mdvver} <= 3000000
%multiarch_binaries %{buildroot}%{_bindir}/gpgme-config
%endif

# Likely we don't need it
rm -rf %{buildroot}%{_libdir}/libgpgmepp.a

%files -n %{libname}
%{_libdir}/libgpgme.so.%{major}*

%files -n %{libgpgmepp}
%{_libdir}/libgpgmepp.so.%{gpgmepp_major}*

%files -n %{libqgpgme}
%{_libdir}/libqgpgme.so.%{qgpgme_major}*

%files -n %{devgpgmepp}
%{_includedir}/gpgme++/*
%{_libdir}/libgpgmepp.so
%dir %{_libdir}/cmake/Gpgmepp/
%{_libdir}/cmake/Gpgmepp/*

%files -n %{devqgpgme}
%dir %{_includedir}/qgpgme
%dir %{_includedir}/QGpgME
%{_includedir}/qgpgme/*
%{_includedir}/QGpgME/*
%{_libdir}/libqgpgme.so
%{_libdir}/cmake/QGpgme

%files -n %{devname}
%doc AUTHORS NEWS README THANKS TODO
%if %{mdvver} <= 3000000
%{multiarch_bindir}/gpgme-config
%endif
%{_bindir}/gpgme-config
%{_bindir}/gpgme-tool
%{_libdir}/libgpgme.so
%{_datadir}/aclocal/*.m4
%{_includedir}/*.h
%dir %{_datadir}/common-lisp/source/gpgme
%{_datadir}/common-lisp/source/gpgme/gpgme-package.lisp
%{_datadir}/common-lisp/source/gpgme/gpgme.asd
%{_datadir}/common-lisp/source/gpgme/gpgme.lisp

%files -n python-gpg
%{py_platsitedir}/gpg*

%files -n python2-gpg
%{py2_platsitedir}/gpg*

%files doc
%{_infodir}/*
