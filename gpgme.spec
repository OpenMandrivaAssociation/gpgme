%define major 45
%define libname %mklibname %{name}
%define devname %mklibname %{name} -d

# Avoid autogen.sh --find-version marking the release tarball as beta
%define _disable_rebuild_configure 1

# Python module not linked to libpython
%global _disable_ld_no_undefined 1

Summary:	GnuPG Made Easy (GPGME)
Name:		gpgme
Version:	2.2.0
Release:	1
License:	GPLv2+
Group:		File tools
Url:		https://www.gnupg.org/gpgme.html
Source0:	https://gnupg.org/ftp/gcrypt/gpgme/%{name}-%{version}.tar.bz2
# Long-lived-context trainer: encrypt/decrypt/sign/verify/keylist on mail-sized data
Source1:	pgo-train.c

BuildSystem:	autotools
BuildOption:	--disable-fd-passing
BuildOption:	--disable-gpgsm-test

BuildRequires:	gnupg
BuildRequires:	pkgconfig(libassuan) >= 2.4.2
BuildRequires:	pkgconfig(gpg-error) >= 1.47

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

%install -a
# According to upstream maintainer:
# "Yeah, an ABI break - It would be surprising if anyone is affected"
# Might as well risk it for compatibility with old apps...
# Bumped from 11 to 45 2025-06-03 after 6.0
ln -s libgpgme.so.%{major} %{buildroot}%{_libdir}/libgpgme.so.11

# Profile the library as a mail/key-manager client, not the regression suite.
# tests/gpg only supplies the demo keyring and dummy pinentry.
%pgo
%make_build -C _OMV_rpm_build/tests/gpg pinentry gpg.conf gpg-agent.conf pubring-stamp LIBTOOL=slibtool-shared
export GNUPGHOME="$PWD/_OMV_rpm_build/tests/gpg"
export GPG_AGENT_INFO=
export LC_ALL=C
# Dummy pinentry (passphrase "abc") so gpgme-json cannot hang on a missing TTY
echo "pinentry-program $PWD/_OMV_rpm_build/tests/gpg/pinentry" >> "$GNUPGHOME/gpg-agent.conf"
echo "allow-loopback-pinentry" >> "$GNUPGHOME/gpg-agent.conf"
"$PWD/tests/start-stop-agent" --start
lib=
for p in _OMV_rpm_build/src/.libs/libgpgme.so _OMV_rpm_build/src/libgpgme.so; do
	[ -e "$p" ] && lib=$p && break
done
test -n "$lib"
export LD_LIBRARY_PATH="$(dirname "$lib")${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
# Do not instrument the trainer; only the just-built libgpgme is shipped
${CC:-%{__cc}} -O2 -I_OMV_rpm_build/src -o pgo-train %{SOURCE1} "$lib" -lgpg-error
./pgo-train
json=
for p in _OMV_rpm_build/src/.libs/gpgme-json _OMV_rpm_build/src/gpgme-json; do
	[ -x "$p" ] && json=$p && break
done
if [ -n "$json" ]; then
	for op in t-keylist t-encrypt t-sign t-verify t-decrypt t-encrypt-sign t-decrypt-verify t-export; do
		f=tests/json/${op}.in.json
		[ -f "$f" ] || continue
		i=0
		while [ $i -lt 8 ]; do
			"$json" --single < "$f" >/dev/null
			i=$((i + 1))
		done
	done
fi
"$PWD/tests/start-stop-agent" --stop

%if ! %{cross_compiling}
%check
%make_build -C _OMV_rpm_build check LIBTOOL=slibtool-shared
%endif

%files
%{_bindir}/gnupg-key-manage

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
