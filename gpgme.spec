%define major 11
%define gpgmepp_major 6
%define qgpgme_major 15
%define libname %mklibname %{name} %{major}
%define libgpgmepp %mklibname %{name}pp %{gpgmepp_major}
%define devgpgmepp %mklibname %{name}pp -d
%define libqgpgme %mklibname qgpgme %{qgpgme_major}
%define devqgpgme %mklibname qgpgme -d
%define devname %mklibname %{name} -d
# Doesn't exist anymore, but needs to be obsoleted
%define libpthread %mklibname %{name}_pthread 11

# Python module not linked to libpython
%global _disable_ld_no_undefined 1

%define gpgsm_version 1.9.6
%bcond_without qt5

Summary:	GnuPG Made Easy (GPGME)
Name:		gpgme
Version:	1.23.1
Release:	1
License:	GPLv2+
Group:		File tools
Url:		http://www.gnupg.org/gpgme.html
Source0:	ftp://ftp.gnupg.org/gcrypt/gpgme/%{name}-%{version}.tar.bz2
#Patch1:		gpgme-1.17.0-python-3.11.patch
Patch2:		https://src.fedoraproject.org/rpms/gpgme/raw/rawhide/f/0001-don-t-add-extra-libraries-for-linking.patch
Patch3:		https://src.fedoraproject.org/rpms/gpgme/raw/rawhide/f/0001-fix-stupid-ax_python_devel.patch
Patch4:		gpgme-1.18.0-pp-export-progress_callback.patch
Patch5:		0001-avoid-identifying-as-beta-FIXED.patch
Patch6:		gpgme-1.22.0-compile.patch

# support for Cryptographic Message Syntax protocol
BuildRequires:	gnupg >= %{gpgsm_version}
BuildRequires:	pkgconfig(libassuan) >= 2.4.2
BuildRequires:	pkgconfig(gpg-error) >= 1.47
BuildRequires:	pkgconfig(glib-2.0)
%if %{with qt5}
BuildRequires:	pkgconfig(Qt5Core)
BuildRequires:	pkgconfig(Qt5Test)
%endif

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
Obsoletes:	%{_lib}GppMePp-devel < 1.19.0-3

%description -n %{libgpgmepp}
GnuPG Made Easy (GPGME) is a library designed to make access to GnuPG
easier for applications.

%if %{with qt5}
%package -n %{libqgpgme}
Summary:	Qt bindings to GnuPG Made Easy (GPGME)
Group:		System/Libraries

%description -n %{libqgpgme}
Qt bindings to GnuPG Made Easy (GPGME), a library designed to make access
to GnuPG easier for applications.

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
%endif

%package -n %{devgpgmepp}
Summary:	GnuPG Made Easy (GPGME) Header files and libraries for development
Group:		Development/C++
Requires:	%{devname} = %{EVRD}
Requires:	%{libgpgmepp} = %{EVRD}
Requires:	%{devqgpgme} = %{EVRD}
Provides:	%{name}pp-devel = %{EVRD}
Provides:	%{name}++-devel = %{EVRD}
Conflicts:	kdepimlibs4-devel >= 3:4.14.10
Obsoletes:	%{_lib}GpgMePp-devel < 1.19.0-3

%description -n %{devgpgmepp}
GnuPG Made Easy (GPGME) is a library designed to make access to GnuPG
easier for applications.

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
Requires:	gnupg >= 2.0
Provides:	python3-gpg

%description -n python-gpg
Python bindings to GPG encryption

%package doc
Summary:	Documentation for GnuPG Made Easy (GPGME)
Group:		Books/Computer books
Requires:	%{libname} = %{EVRD}

%description doc
Documentation for GnuPG Made Easy (GPGME).

%prep
%autosetup -p1
# (tpg) this is neededf for patch 5
./autogen.sh

%build
%configure \
	--disable-fd-passing \
	--disable-gpgsm-test

%make_build

#check
#make check

%install
# (tpg) 2023-04-12 fix fir TEST FAILED: /builddir/build/BUILDROOT/gpgme-1.19.0-2.x86_64/usr/lib64/python3.11/site-packages/ does NOT support .pth files
export SETUPTOOLS_USE_DISTUTILS=stdlib
%make_install

# For some reason, make install gets the python 3.x (x >= 10)
# install paths completely wrong
export top_builddir="$(pwd)"
cd lang/python
python setup.py install --prefix=%{_prefix} --root=%{buildroot}

# Likely we don't need it
rm -rf %{buildroot}%{_libdir}/libgpgmepp.a

%files -n %{libname}
%{_libdir}/libgpgme.so.%{major}*

%files -n %{libgpgmepp}
%{_libdir}/libgpgmepp.so.%{gpgmepp_major}*

%if %{with qt5}
%files -n %{libqgpgme}
%{_libdir}/libqgpgme.so.%{qgpgme_major}*

%files -n %{devqgpgme}
%dir %{_includedir}/qgpgme
%dir %{_includedir}/QGpgME
%{_includedir}/qgpgme/*
%{_includedir}/QGpgME/*
%{_libdir}/libqgpgme.so
%{_libdir}/cmake/QGpgme
%endif

%files -n %{devgpgmepp}
%{_includedir}/gpgme++/*
%{_libdir}/libgpgmepp.so
%dir %{_libdir}/cmake/Gpgmepp/
%{_libdir}/cmake/Gpgmepp/*

%files -n %{devname}
%doc AUTHORS NEWS README THANKS TODO
%{_bindir}/gpgme-config
%{_bindir}/gpgme-tool
%{_bindir}/gpgme-json
%{_libdir}/libgpgme.so
%{_datadir}/aclocal/*.m4
%{_includedir}/*.h
%{_libdir}/pkgconfig/gpgme*.pc
%dir %{_datadir}/common-lisp/source/gpgme
%{_datadir}/common-lisp/source/gpgme/gpgme-package.lisp
%{_datadir}/common-lisp/source/gpgme/gpgme.asd
%{_datadir}/common-lisp/source/gpgme/gpgme.lisp
%{_datadir}/common-lisp/source/gpgme/gpgme-grovel.lisp

%files -n python-gpg
%{py_platsitedir}/gpg*

%files doc
%{_infodir}/*
