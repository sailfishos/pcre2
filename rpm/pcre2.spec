%define keepstatic 1

# Add readline edditing in pcre2test tool
%bcond_without pcre2_enables_readline

# Disable SELinux-frindly JIT allocator because it seems not to be fork-safe,
# https://bugs.exim.org/show_bug.cgi?id=1749#c45
%bcond_with pcre2_enables_sealloc

Name:       pcre2
Version:    10.42
Release:    1
Summary:    Perl-compatible regular expression library
# the library:                          BSD with exceptions
# pcre2test (linked to GNU readline):   BSD (linked to GPLv3+)
# COPYING:                              see LICENCE file
# LICENSE:                              BSD text with exceptions and
#                                       Public Domain declaration
#                                       for testdata
#Bundled
# src/sljit:                            BSD
#Not distributed in any binary package
# aclocal.m4:                           FSFULLR and GPLv2+ with exception
# ar-lib:                               GPLv2+ with exception
# cmake/COPYING-CMAKE-SCRIPTS:          BSD
# compile:                              GPLv2+ with exception
# config.guess:                         GPLv3+ with exception
# config.sub:                           GPLv3+ with exception
# configure:                            FSFUL and GPLv2+ with exception
# depcomp:                              GPLv2+ with exception
# INSTALL:                              FSFAP
# install-sh:                           MIT
# ltmain.sh:                            GPLv2+ with exception and (MIT or GPLv3+)
# m4/ax_pthread.m4:                     GPLv3+ with exception
# m4/libtool.m4:                        FSFUL and FSFULLR and
#                                       GPLv2+ with exception
# m4/ltoptions.m4:                      FSFULLR
# m4/ltsugar.m4:                        FSFULLR
# m4/ltversion.m4:                      FSFULLR
# m4/lt~obsolete.m4:                    FSFULLR
# m4/pcre2_visibility.m4:               FSFULLR
# Makefile.in:                          FSFULLR
# missing:                              GPLv2+ with exception
# test-driver:                          GPLv2+ with exception
# testdata:                             Public Domain
License:    BSD-3-Clause
URL:        https://www.pcre.org/
Source0:    https://github.com/PCRE2Project/pcre2/releases/download/pcre2-%{version}/pcre2-%{version}.tar.bz2
# Do no set RPATH if libdir is not /usr/lib
Patch0:     0001-Fix-multilib.patch
# Upstream commits:
# https://github.com/PCRE2Project/pcre2/commit/794245ecc296724b52f5030831e58bedbffa2452
# https://github.com/PCRE2Project/pcre2/commit/457c0e69a8f78d32bc7d4b6422cd01e396a4cf5d
Patch1:     0002-match-also-restore-originally-unset-entries-in-recur.patch
Patch2:     0003-Add-more-examples-fixed-by-300-update-ChangeLog.patch

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  coreutils
BuildRequires:  gnupg2
BuildRequires:  libtool
BuildRequires:  make
%if %{with pcre2_enables_readline}
BuildRequires:  readline-devel
%endif
BuildRequires:  sed
Provides:       bundled(sljit)

%description
PCRE2 is a re-working of the original PCRE (Perl-compatible regular
expression) library to provide an entirely new API.

PCRE2 is written in C, and it has its own API. There are three sets of
functions, one for the 8-bit library, which processes strings of bytes, one
for the 16-bit library, which processes strings of 16-bit values, and one for
the 32-bit library, which processes strings of 32-bit values. There are no C++
wrappers. This package provides support for strings in 8-bit and UTF-8
encodings. Install %{name}-utf16 or %{name}-utf32 packages for the other ones.

The distribution does contain a set of C wrapper functions for the 8-bit
library that are based on the POSIX regular expression API (see the pcre2posix
man page). These can be found in a library called libpcre2posix. Note that
this just provides a POSIX calling interface to PCRE2; the regular expressions
themselves still follow Perl syntax and semantics. The POSIX API is
restricted, and does not give full access to all of PCRE2's facilities.

%package utf16
Summary:    UTF-16 variant of PCRE2
Provides:   bundled(sljit)

%description utf16
This is PCRE2 library working on UTF-16 strings.

%package utf32
Summary:    UTF-32 variant of PCRE2
Provides:   bundled(sljit)

%description utf32
This is PCRE2 library working on UTF-32 strings.

%package devel
Summary:    Development files for %{name}
Requires:   %{name} = %{version}-%{release}
Requires:   %{name}-utf16 = %{version}-%{release}
Requires:   %{name}-utf32 = %{version}-%{release}

%description devel
Development files (headers, libraries for dynamic linking, documentation)
for %{name}.  The header file for the POSIX-style functions is called
pcre2posix.h.

%package static
Summary:    Static library for %{name}
Requires:   %{name}-devel = %{version}-%{release}
Provides:   bundled(sljit)

%description static
Library for static linking for %{name}.

%package doc
Summary:    Documentation for PCRE2
BuildArch:  noarch

%description doc
This is a set of manual pages that document the PCRE2 library the syntax of
the regular expressions implemented by it.

%package tools
Summary:    Auxiliary utilities for %{name}
# pcre2test (linked to GNU readline):   BSD (linked to GPLv3+)
License:    BSD and GPLv3+
Requires:   %{name} = %{version}-%{release}

%description tools
Utilities demonstrating PCRE2 capabilities like pcre2grep or pcre2test.

%prep
%autosetup -p1 -n %{name}-%{version}/%{name}

%build
%reconfigure \
    --enable-jit \
    --enable-pcre2grep-jit \
    --disable-bsr-anycrlf \
    --disable-coverage \
    --disable-ebcdic \
    --disable-fuzz-support \
%if %{with pcre2_enables_sealloc}
    --enable-jit-sealloc \
%else
    --disable-jit-sealloc \
%endif
    --disable-never-backslash-C \
    --enable-newline-is-lf \
    --enable-pcre2-8 \
    --enable-pcre2-16 \
    --enable-pcre2-32 \
    --enable-pcre2grep-callout \
    --enable-pcre2grep-callout-fork \
    --disable-pcre2grep-libbz2 \
    --disable-pcre2grep-libz \
    --disable-pcre2test-libedit \
%if %{with pcre2_enables_readline}
    --enable-pcre2test-libreadline \
%else
    --disable-pcre2test-libreadline \
%endif
    --enable-percent-zt \
    --disable-rebuild-chartables \
    --enable-shared \
    --disable-silent-rules \
    --enable-static \
    --enable-unicode \
    --disable-valgrind
%make_build

%install
%make_install

# Get rid of unneeded *.la files
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

# These are handled by %%doc in %%files
rm -rf $RPM_BUILD_ROOT%{_docdir}/pcre2

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%post utf16 -p /sbin/ldconfig
%postun utf16 -p /sbin/ldconfig

%post utf32 -p /sbin/ldconfig
%postun utf32 -p /sbin/ldconfig

%files
%license COPYING LICENCE
%{_libdir}/libpcre2-8.so.0*
%{_libdir}/libpcre2-posix.so.3*

%files utf16
%license COPYING LICENCE
%{_libdir}/libpcre2-16.so.0*

%files utf32
%license COPYING LICENCE
%{_libdir}/libpcre2-32.so.0*

%files devel
%{_libdir}/*.so
%{_libdir}/pkgconfig/*
%{_includedir}/*.h
%{_bindir}/pcre2-config

%files static
%license COPYING LICENCE
%{_libdir}/*.a

%files doc
%defattr(-,root,root,-)
%license COPYING LICENCE
%doc AUTHORS ChangeLog NEWS
%doc doc/*.txt doc/html
%doc README HACKING ./src/pcre2demo.c
%{_mandir}/man1/pcre2*
%{_mandir}/man3/pcre2*

%files tools
%{_bindir}/pcre2grep
%{_bindir}/pcre2test
