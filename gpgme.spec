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
Release:	2
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


%changelog
* Wed Jul 11 2012 Alexander Khrukin <akhrukin@mandriva.org> 1.3.2-1
+ Revision: 808836
- version update 1.3.2

* Tue Jul 05 2011 Lonyai Gergely <aleph@mandriva.org> 1.3.1-3
+ Revision: 688727
- 1.3.1

* Mon May 02 2011 Oden Eriksson <oeriksson@mandriva.com> 1.3.0-3
+ Revision: 661668
- multiarch fixes

* Thu Dec 02 2010 Oden Eriksson <oeriksson@mandriva.com> 1.3.0-2mdv2011.0
+ Revision: 605495
- rebuild

* Mon Jan 11 2010 Lonyai Gergely <aleph@mandriva.org> 1.3.0-1mdv2010.1
+ Revision: 489739
- 1.3.0

* Tue Jun 30 2009 Nicolas Lécureuil <nlecureuil@mandriva.com> 1.2.0-1mdv2010.0
+ Revision: 390789
- Update  to gpgme 1.2.0

* Sun Jan 18 2009 Tomasz Pawel Gajc <tpg@mandriva.org> 1.1.8-1mdv2009.1
+ Revision: 331039
- update to new version 1.1.8

* Sun Nov 16 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 1.1.7-1mdv2009.1
+ Revision: 303835
- update to new version 1.1.7
- fix ur for Source0

* Tue Jun 17 2008 Thierry Vignaud <tv@mandriva.org> 1.1.6-2mdv2009.0
+ Revision: 221100
- rebuild

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Wed Jan 23 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 1.1.6-1mdv2008.1
+ Revision: 157125
- new license policy
- do not package COPYING files
- spec file clean
- new version

* Fri Dec 21 2007 Olivier Blin <blino@mandriva.org> 1.1.5-2mdv2008.1
+ Revision: 136461
- restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Mon Sep 24 2007 Andreas Hasenack <andreas@mandriva.com> 1.1.5-2mdv2008.0
+ Revision: 92576
- added missing buildrequires (glib2-devel) + rebuild

* Wed Aug 01 2007 Tomasz Pawel Gajc <tpg@mandriva.org> 1.1.5-1mdv2008.0
+ Revision: 57324
- new devel library policy
- make use of %%{major}
- add %%check section
- new version

