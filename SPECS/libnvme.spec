# RHEL 8 compatibility
%{!?version_no_tilde: %define version_no_tilde %{shrink:%(echo '%{version}' | tr '~' '-')}}

Name:    libnvme
Summary: Linux-native nvme device management library
Version: 1.4
Release: 7%{?dist}
License: LGPLv2+
URL:     https://github.com/linux-nvme/libnvme
Source0: %{url}/archive/v%{version_no_tilde}/%{name}-%{version_no_tilde}.tar.gz

Patch0:  0001-fabrics-Do-not-pass-unsupported-options-to-kernel.patch
Patch1:  0002-nbft-add-NBFT-v1.0-table-support.patch
Patch2:  0003-nbft-Move-added-symbols-to-LIBNVME_1_5.patch
Patch3:  0004-nbft-Fix-nbft_ssns_flags-endianness-test.patch
Patch4:  0005-nbft-Parse-the-HOSTID-HOSTNQN-_CONFIGURED-flags.patch
Patch5:  0006-nbft-Doc-typo-Use-nvme_nbft_free-instead-of-nbft_fre.patch
Patch6:  0007-NBFT-Remove-documentation-from-nbft.c-since-it-s-als.patch
Patch7:  0008-fabrics-check-genctr-after-getting-discovery-entries.patch
Patch8:  0009-ioctl-fix-RAE-bit-on-last-Get-Log-Page-command.patch

BuildRequires: gcc gcc-c++
BuildRequires: swig
BuildRequires: python3-devel
BuildRequires: meson >= 0.50.0
BuildRequires: json-c-devel >= 0.13
BuildRequires: openssl-devel
BuildRequires: keyutils-libs-devel

Requires: keyutils-libs

%description
Provides type definitions for NVMe specification structures,
enumerations, and bit fields, helper functions to construct,
dispatch, and decode commands and payloads, and utilities to connect,
scan, and manage nvme devices on a Linux system.

%package devel
Summary: Development files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
This package provides header files to include and libraries to link with
for Linux-native nvme device management.
%package doc
Summary: Reference manual for libnvme
BuildArch: noarch
BuildRequires: perl-interpreter
BuildRequires: python3-sphinx
BuildRequires: python3-sphinx_rtd_theme

%description doc
This package contains the reference manual for %{name}.

%package -n python3-libnvme
Summary:  Python3 bindings for libnvme
Requires: %{name}%{?_isa} = %{version}-%{release}
Provides:  python3-nvme = %{version}-%{release}
%{?python_provide:%python_provide python3-libnvme}

%description -n python3-libnvme
This package contains Python bindings for libnvme.

%prep
%autosetup -p1 -n %{name}-%{version_no_tilde}

%build
%meson -Dpython=enabled -Dlibdbus=disabled -Ddocs=all -Ddocs-build=true -Dhtmldir=%{_pkgdocdir}
%meson_build

%install
%meson_install
%{__install} -pm 644 README.md %{buildroot}%{_pkgdocdir}
%{__install} -pm 644 doc/config-schema.json %{buildroot}%{_pkgdocdir}
mv %{buildroot}%{_pkgdocdir}/nvme/html %{buildroot}%{_pkgdocdir}/html
rm -rf %{buildroot}%{_pkgdocdir}/nvme
mv %{buildroot}/usr/*.rst %{buildroot}%{_pkgdocdir}/

%ldconfig_scriptlets

%files
%license COPYING ccan/licenses/*
%{_libdir}/libnvme.so.1
%{_libdir}/libnvme.so.1.4.0
%{_libdir}/libnvme-mi.so.1
%{_libdir}/libnvme-mi.so.1.4.0

%files devel
%{_libdir}/libnvme.so
%{_libdir}/libnvme-mi.so
%{_includedir}/libnvme.h
%{_includedir}/libnvme-mi.h
%dir %{_includedir}/nvme
%{_includedir}/nvme/*.h
%{_libdir}/pkgconfig/*.pc

%files doc
%doc %{_pkgdocdir}
%{_mandir}/man2/*.2*

%files -n python3-libnvme
%dir %{python3_sitearch}/libnvme
%{python3_sitearch}/libnvme/*

%changelog
* Mon Jul 17 2023 John Meneghini <jmeneghi@redhat.com> - 1.4-7
- Fix BZ#2223429

* Mon Jun 05 2023 Maurizio Lombardi <mlombard@redhat.com> - 1.4-6
- Rebuild for BZ2212307

* Tue May 16 2023 Maurizio Lombardi <mlombard@redhat.com> - 1.4-5
- Add support to NBFT (BZ2188516)

* Mon May 08 2023 Maurizio Lombardi <mlombard@redhat.com> - 1.4-4
- Fix BZ#2190206

* Fri May 05 2023 Maurizio Lombardi <mlombard@redhat.com> - 1.4-3
- Fix Jira RHEL-258

* Thu Apr 06 2023 Maurizio Lombardi <mlombard@redhat.com> - 1.4-2
- Rebuild the package

* Mon Apr 03 2023 Maurizio Lombardi <mlombard@redhat.com> - 1.4-1
- Update to version 1.4

* Thu Jan 12 2023 John Meneghini <jmeneghi@redhat.com> - 1.2-2
- Fix BZ2158264

* Fri Nov 04 2022 Maurizio Lombardi <mlombard@redhat.com> - 1.2-1
- Update to upstream version v1.2

* Mon Sep 19 2022 Maurizio Lombardi <mlombard@redhat.com> - 1.1-1
- Update to upstream version v1.1

* Fri Jun 24 2022 Maurizio Lombardi <mlombard@redhat.com> - 1.0-5
- Rebuild for RHEL9.1

* Thu Jun 09 2022 Maurizio Lombardi <mlombard@redhat.com> - 1.0-4
- Add gating tests

* Wed Jun 01 2022 Maurizio Lombardi <mlombard@redhat.com> - 1.0-3
- Rebuild for RHEL 9.1

* Wed Apr 27 2022 Maurizio Lombardi <mlombard@redhat.com> - 1.0-2
-  Porting to RHEL 9

* Mon Apr 11 2022 Tomas Bzatek <tbzatek@redhat.com> - 1.0-1
- Upstream v1.0 release

* Fri Apr 01 2022 Tomas Bzatek <tbzatek@redhat.com> - 1.0~rc8-1
- Upstream v1.0 Release Candidate 8

* Wed Mar 23 2022 Tomas Bzatek <tbzatek@redhat.com> - 1.0~rc7-1
- Upstream v1.0 Release Candidate 7
- Renamed python3-nvme subpackage to python3-libnvme

* Mon Mar 14 2022 Tomas Bzatek <tbzatek@redhat.com> - 1.0~rc6-1
- Upstream v1.0 Release Candidate 6

* Fri Mar 04 2022 Tomas Bzatek <tbzatek@redhat.com> - 1.0~rc5-1
- Upstream v1.0 Release Candidate 5

* Mon Feb 28 2022 Tomas Bzatek <tbzatek@redhat.com> - 1.0~rc4-1
- Upstream v1.0 Release Candidate 4

* Fri Feb 11 2022 Tomas Bzatek <tbzatek@redhat.com> - 1.0~rc3-1
- Upstream v1.0 Release Candidate 3

* Tue Feb 01 2022 Tomas Bzatek <tbzatek@redhat.com> - 1.0~rc2-1
- Upstream v1.0 Release Candidate 2

* Thu Jan 27 2022 Tomas Bzatek <tbzatek@redhat.com> - 1.0~rc1-1
- Upstream v1.0 Release Candidate 1

* Mon Jan 17 2022 Tomas Bzatek <tbzatek@redhat.com> - 1.0~rc0-1
- Upstream v1.0 Release Candidate 0

* Wed Oct 20 2021 Tomas Bzatek <tbzatek@redhat.com> - 0.0.1-1.git1fe38d6
- Initial packaging
