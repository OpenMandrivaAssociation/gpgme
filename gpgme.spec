%define major 45
%define libname %mklibname %{name}
%define devname %mklibname %{name} -d

# Python module not linked to libpython
%global _disable_ld_no_undefined 1

Summary:	GnuPG Made Easy (GPGME)
Name:		gpgme
Version:	2.0.0
Release:	1
License:	GPLv2+
Group:		File tools
Url:		https://www.gnupg.org/gpgme.html
Source0:	https://gnupg.org/ftp/gcrypt/gpgme/%{name}-%{version}.tar.bz2
#Patch1:		gpgme-1.17.0-python-3.11.patch
#Patch2:		https://src.fedoraproject.org/rpms/gpgme/raw/rawhide/f/0001-don-t-add-extra-libraries-for-linking.patch
#Patch3:		https://src.fedoraproject.org/rpms/gpgme/raw/rawhide/f/0001-fix-stupid-ax_python_devel.patch
#Patch4:		gpgme-1.18.0-pp-export-progress_callback.patch
Patch5:		0001-avoid-identifying-as-beta-FIXED.patch
#Patch6:		gpgme-1.22.0-compile.patch

# support for Cryptographic Message Syntax protocol
BuildRequires:	gnupg
BuildRequires:	pkgconfig(libassuan) >= 2.4.2
BuildRequires:	pkgconfig(gpg-error) >= 1.47
BuildRequires:	pkgconfig(glib-2.0)

%description
GnuPG Made Easy (GPGME) is a library designed to make access to GnuPG
easier for applications.

%package -n %{libname}
Summary:	GnuPG Made Easy (GPGME)
Group:		System/Libraries
Recommends:	gnupg
Provides:	%{name} = %{version}-%{release}
Conflicts:	%{_lib}gpgme11 < 1.3.2-3
%rename %{mklibname gpgme 11}
%ifarch %{x86_64} %{aarch64} %{riscv64}
Provides:	libgpgme.so.11()(64bit)
Provides:	libgpgme.so.11(GPGME_1.0)(64bit)
Provides:	libgpgme.so.11(GPGME_1.1)(64bit)
%else
Provides:	libgpgme.so.11
Provides:	libgpgme.so.11(GPGME_1.0)
Provides:	libgpgme.so.11(GPGME_1.1)
%endif

%description -n %{libname}
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
export CONFIGURE_TOP=`pwd`
mkdir build
cd build
%configure \
	--disable-fd-passing \
	--disable-gpgsm-test

%make_build
cd ..

%install
%make_install -C build

# According to upstream maintainer:
# "Yeah, an ABI break - It would be surprising if anyone is affected"
# Might as well risk it for compatibility with old apps...
# Bumped from 11 to 45 2025-06-03 after 6.0
ln -s libgpgme.so.%{major} %{buildroot}%{_libdir}/libgpgme.so.11

%if 0
%check
%make_build check -C build
%endif

%files -n %{libname}
%{_libdir}/libgpgme.so.%{major}*
%{_libdir}/libgpgme.so.11

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
%{_mandir}/man1/gpgme-json.1*

%files doc
%{_infodir}/*
