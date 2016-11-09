%define major 11
%define gpgmepp_major 6
%define libname %mklibname %{name} %{major}
%define libpthread %mklibname %{name}_pthread %{major}
%define libgpgmepp %mklibname %{name}pp %{gpgmepp_major}
%define devname %mklibname %{name} -d

%define gpgsm_version 1.9.6

Summary:	GnuPG Made Easy (GPGME)
Name:		gpgme
Version:	1.7.1
Release:	1
License:	GPLv2+
Group:		File tools
Url:		http://www.gnupg.org/gpgme.html
Source0:	ftp://ftp.gnupg.org/gcrypt/gpgme/%{name}-%{version}.tar.bz2
Source1:	ftp://ftp.gnupg.org/gcrypt/gpgme/%{name}-%{version}.tar.bz2.sig

# support for Cryptographic Message Syntax protocol
BuildRequires:	gnupg >= %{gpgsm_version}
BuildRequires:	libassuan-devel >= 2.0.2
BuildRequires:	pth-devel >= 2.0.0
BuildRequires:	pkgconfig(gpg-error)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(Qt5Core)
BuildRequires:	pkgconfig(Qt5Test)

%description
GnuPG Made Easy (GPGME) is a library designed to make access to GnuPG
easier for applications.

%package -n %{libname}
Summary:	GnuPG Made Easy (GPGME)
Group:		System/Libraries
# support for Cryptographic Message Syntax protocol
Requires:	gnupg >= %{gpgsm_version}
Provides:	%{name} = %{version}-%{release}
Conflicts:	%{_lib}gpgme11 < 1.3.2-3

%description -n %{libname}
GnuPG Made Easy (GPGME) is a library designed to make access to GnuPG
easier for applications.

%package -n %{libpthread}
Summary:	GnuPG Made Easy (GPGME)
Group:		System/Libraries

%description -n %{libpthread}
GnuPG Made Easy (GPGME) is a library designed to make access to GnuPG
easier for applications.

%package -n %{libgpgmepp}
Summary:	GnuPG Made Easy (GPGME)
Group:		System/Libraries

%description -n %{libgpgmepp}
GnuPG Made Easy (GPGME) is a library designed to make access to GnuPG
easier for applications.

%package -n %{devname}
Summary:	GnuPG Made Easy (GPGME) Header files and libraries for development
Group:		Development/C
Requires:	%{libname} = %{EVRD}
Requires:	%{libpthread} = %{EVRD}
Requires:	%{libgpgmepp} = %{EVRD}
Provides:	%{name}-devel = %{EVRD}
Obsoletes:	%{_lib}gpgme-devel-static < 1.7.1

%description -n %{devname}
Install this package if you want to develop applications 
that will use the %{name} library for crypto awareness.

%prep
%setup -q

%build
%configure
%make

#check
#make check

%install
%makeinstall_std

%multiarch_binaries %{buildroot}%{_bindir}/gpgme-config

%files -n %{libname}
%{_libdir}/libgpgme.so.%{major}*

%files -n %{libpthread}
%{_libdir}/libgpgme-pthread.so.%{major}*

%files -n %{libgpgmepp}
%{_libdir}/libgpgmepp.so.%{gpgmepp_major}*

%files -n %{devname}
%doc AUTHORS NEWS README THANKS TODO
%{multiarch_bindir}/gpgme-config
%{_bindir}/gpgme-config
%{_bindir}/gpgme-tool
%{_libdir}/*.so
%{_datadir}/aclocal/*.m4
%{_includedir}/*
%{_infodir}/*
%dir %{_libdir}/cmake/Gpgmepp
%{_libdir}/cmake/Gpgmepp/*.cmake
%dir %{_datadir}/common-lisp/source/gpgme
%{_datadir}/common-lisp/source/gpgme/gpgme-package.lisp
%{_datadir}/common-lisp/source/gpgme/gpgme.asd
%{_datadir}/common-lisp/source/gpgme/gpgme.lisp
