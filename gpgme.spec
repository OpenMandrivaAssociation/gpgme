%define major 11
%define libname_orig %mklibname %{name}
%define libname %mklibname %{name} %{major}
%define develname %mklibname %{name} -d

%define gpg_version 1.2.2
%define gpgsm_version 1.9.6

Summary:	GnuPG Made Easy (GPGME)
Name:		gpgme
Version:	1.3.0
Release:	%mkrel 2
License:	GPLv2+
Group:		File tools
URL:		http://www.gnupg.org/gpgme.html
Source0:	ftp://ftp.gnupg.org/gcrypt/gpgme/%{name}-%{version}.tar.bz2
Source1:	%{SOURCE0}.sig
BuildRequires:	gnupg >= %{gpg_version}
# support for Cryptographic Message Syntax protocol
BuildRequires:	gnupg2 >= %{gpgsm_version}
BuildRequires:	pth-devel >= 2.0.0
BuildRequires:	libassuan-devel
BuildRequires:	libgpg-error-devel >= 0.5
BuildRequires:	libglib2-devel >= 2.0.0
%if %mdkversion >= 1020
BuildRequires:	multiarch-utils >= 1.0.3
%endif
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

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

%if %mdkversion >= 1020
%multiarch_binaries %{buildroot}%{_bindir}/gpgme-config
%endif

%clean
rm -rf %{buildroot}

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%post -n %{develname}
%_install_info %{name}.info

%postun -n %{develname}
%_remove_install_info %{name}.info


%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/lib*.so.%{major}*

%files -n %{develname}
%defattr(-,root,root)
%doc AUTHORS ChangeLog NEWS README THANKS TODO
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
