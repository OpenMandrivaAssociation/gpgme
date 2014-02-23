%define major 11
%define libname %mklibname %{name} %{major}
%define libpthread %mklibname %{name}_pthread %{major}
%define devname %mklibname %{name} -d

%define gpgsm_version 1.9.6

Summary:	GnuPG Made Easy (GPGME)
Name:		gpgme
Version:	1.4.3
Release:	6
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

%package -n %{devname}
Summary:	GnuPG Made Easy (GPGME) Header files and libraries for development
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Requires:	%{libpthread} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	%{_lib}gpgme-devel-static = %{version}-%{release}

%description -n %{devname}
Install this package if you want to develop applications 
that will use the %{name} library for crypto awareness.

%prep
%setup -q

%build
%configure2_5x
%make

%check
make check

%install
%makeinstall_std

%multiarch_binaries %{buildroot}%{_bindir}/gpgme-config

%files -n %{libname}
%{_libdir}/libgpgme.so.%{major}*

%files -n %{libpthread}
%{_libdir}/libgpgme-pthread.so.%{major}*

%files -n %{devname}
%doc AUTHORS ChangeLog NEWS README THANKS TODO
%{multiarch_bindir}/gpgme-config
%{_bindir}/gpgme-config
%{_libdir}/*.so
%{_datadir}/aclocal/*.m4
%{_includedir}/*
%{_infodir}/*
%dir %{_datadir}/common-lisp/source/gpgme
%{_datadir}/common-lisp/source/gpgme/gpgme-package.lisp
%{_datadir}/common-lisp/source/gpgme/gpgme.asd
%{_datadir}/common-lisp/source/gpgme/gpgme.lisp

