%define major 11
%define libname_orig %mklibname %{name}
%define libname %mklibname %{name} %{major}
%define develname %mklibname %{name} -d
%define develnamest %mklibname %{name} -d -s

%define gpg_version 1.2.2
%define gpgsm_version 1.9.6

Summary:	GnuPG Made Easy (GPGME)
Name:		gpgme
Version:	1.3.2
Release:	1
License:	GPLv2+
Group:		File tools
URL:		http://www.gnupg.org/gpgme.html
Source0:	ftp://ftp.gnupg.org/gcrypt/gpgme/%{name}-%{version}.tar.bz2
Source1:	ftp://ftp.gnupg.org/gcrypt/gpgme/%{name}-%{version}.tar.bz2.sig
BuildRequires:	gnupg >= %{gpg_version}
# support for Cryptographic Message Syntax protocol
BuildRequires:	gnupg2 >= %{gpgsm_version}
BuildRequires:	pth-devel >= 2.0.0
BuildRequires:	libassuan-devel >= 2.0.2
BuildRequires:	libgpg-error-devel >= 0.5
BuildRequires:	glib2-devel >= 2.0.0

%description
GnuPG Made Easy (GPGME) is a library designed to make access to GnuPG
easier for applications.

%package -n %{libname}
Summary:	GnuPG Made Easy (GPGME)
Group:		System/Libraries
Requires:	gnupg >= %{gpg_version}
# support for Cryptographic Message Syntax protocol
Requires:	gnupg2 >= %{gpgsm_version}
Provides:	%{name} = %{version}-%{release}
Provides:	%{libname_orig} = %{version}-%{release}

%description -n %{libname}
GnuPG Made Easy (GPGME) is a library designed to make access to GnuPG
easier for applications.

%package -n %{develname}
Summary:	GnuPG Made Easy (GPGME) Header files and libraries for development
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	%{libname_orig}-devel = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Provides:	lib%{name}-devel = %{version}-%{release}
Obsoletes:	%mklibname %{name} 11 -d

%description -n %{develname}
GnuPG Made Easy (GPGME) is a library designed to make access to GnuPG
easier for applications.

Install this package if you want to develop applications 
that will use the %{name} library for crypto awareness.


%package -n %{develnamest}
Summary:	GnuPG Made Easy (GPGME) Header files and libraries for development
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Requires:	%{name}-devel = %{version}-%{release}
Provides:	%{libname_orig}-devel-static = %{version}-%{release}
Provides:	%{name}-devel-static = %{version}-%{release}
Provides:	lib%{name}-devel-static = %{version}-%{release}


%description -n %{develnamest}
GnuPG Made Easy (GPGME) is a library designed to make access to GnuPG
easier for applications.

Install this package if you want to develop applications 
that will use the %{name} library for crypto awareness.
It's static  lib.

%prep
%setup -q

%build
%configure2_5x \
	--enable-static
%make

%check
make check

%install
rm -rf %{buildroot}
%makeinstall_std

%multiarch_binaries %{buildroot}%{_bindir}/gpgme-config

%post -n %{develname}
%_install_info %{name}.info

%postun -n %{develname}
%_remove_install_info %{name}.info


%files -n %{libname}
%{_libdir}/lib*.so.%{major}*

%files -n %{develnamest}

%files -n %{develname}
%doc AUTHORS ChangeLog NEWS README THANKS TODO
%{multiarch_bindir}/gpgme-config
%{_bindir}/gpgme-config
%{_libdir}/*.a
%{_libdir}/*.so
%{_datadir}/aclocal/*.m4
%{_includedir}/*
%{_infodir}/*
%dir %{_datadir}/common-lisp/source/gpgme
%{_datadir}/common-lisp/source/gpgme/gpgme-package.lisp
%{_datadir}/common-lisp/source/gpgme/gpgme.asd
%{_datadir}/common-lisp/source/gpgme/gpgme.lisp
