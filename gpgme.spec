%define version 1.1.4
%define rel 1
%define release %mkrel %rel

%define major 11
%define libname_orig %mklibname %{name}
%define libname %mklibname %{name} %{major}

%define gpg_version 1.2.2
%define gpgsm_version 1.9.6

Summary:	GnuPG Made Easy (GPGME)
Name:		gpgme
Version:	%{version}
Release:	%{release}
Source0:	ftp://ftp.gnupg.org/%{name}/%{name}-%{version}.tar.bz2
Source1:	ftp://ftp.gnupg.org/%{name}/%{name}-%{version}.tar.bz2.sig
License:	GPL
Group:		File tools
URL:		http://www.gnupg.org/gpgme.html
BuildRequires:	gnupg >= %{gpg_version}
# support for Cryptographic Message Syntax protocol
BuildRequires:	gnupg2 >= %{gpgsm_version}
BuildRequires:	pth-devel >= 2.0.0
BuildRequires:	libgpg-error-devel >= 0.5
%if %mdkversion >= 1020
BuildRequires:	multiarch-utils >= 1.0.3
%endif
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

%description
GnuPG Made Easy (GPGME) is a library designed to make access to GnuPG
easier for applications.

%package	-n %{libname}
Summary:	GnuPG Made Easy (GPGME)
Group:		System/Libraries
Requires:	gnupg >= %{gpg_version}
# support for Cryptographic Message Syntax protocol
Requires:	gnupg2 >= %{gpgsm_version}
Provides:	%{name} = %{version}-%{release}
Provides:	%{libname_orig} = %{version}-%{release}

%description	-n %{libname}
GnuPG Made Easy (GPGME) is a library designed to make access to GnuPG
easier for applications.

%package	-n %{libname}-devel
Summary:	GnuPG Made Easy (GPGME) Header files and libraries for development
Group:		Development/C
Requires:	%{libname} = %{version}
Provides:	%{libname_orig}-devel = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Provides:	lib%{name}-devel = %{version}-%{release}

%description -n %{libname}-devel
GnuPG Made Easy (GPGME) is a library designed to make access to GnuPG
easier for applications.

Install this package if you want to develop applications 
that will use the %{name} library for crypto awareness.

%prep
%setup -q

%build
%configure2_5x --enable-static
%make

make check

%install
rm -rf %{buildroot}
%makeinstall_std

%if %mdkversion >= 1020
%multiarch_binaries %{buildroot}%{_bindir}/gpgme-config
%endif

%clean
rm -rf %{buildroot}

%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig

%post -n %{libname}-devel
%_install_info %{name}.info

%postun -n %{libname}-devel
%_remove_install_info %{name}.info


%files -n %{libname}
%defattr(-,root,root)
%doc COPYING
%{_libdir}/lib*.so.*

%files -n %{libname}-devel
%defattr(-,root,root)
%doc AUTHORS COPYING.LESSER ChangeLog NEWS README THANKS TODO
%if %mdkversion >= 1020
%multiarch %{multiarch_bindir}/gpgme-config
%endif
%{_bindir}/gpgme-config
%{_libdir}/*.a
%{_libdir}/*.la
%{_libdir}/*.so
%{_datadir}/aclocal/*.m4
%{_includedir}/*
%{_infodir}/*
%dir %{_datadir}/common-lisp/source/gpgme
%{_datadir}/common-lisp/source/gpgme/gpgme-package.lisp
%{_datadir}/common-lisp/source/gpgme/gpgme.asd
%{_datadir}/common-lisp/source/gpgme/gpgme.lisp



