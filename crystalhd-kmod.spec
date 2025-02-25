%global buildforkernels akmod
%global debug_package %{nil}

Name:           crystalhd-kmod
Summary:        Kernel module (kmod) for crystalhd
Version:        20220825
Release:        5%{?dist}
License:        GPLv2
URL:            https://github.com/kwizart/crystalhd
Source0:        crystalhd-kmod-%{version}.tar.xz
Source1:        crystalhd-Makefile
Source2:        crystalhd-Kconfig
Source11:       crystalhd-kmodtool-excludekernel-filterfile
# get the needed BuildRequires (in parts depending on what we build for)
BuildRequires:  %{_bindir}/kmodtool
%{!?kernels:BuildRequires: buildsys-build-rpmfusion-kerneldevpkgs-%{?buildforkernels:%{buildforkernels}}%{!?buildforkernels:current}-%{_target_cpu} }
%{?fedora:BuildRequires: unifdef}
ExclusiveArch:  i686 x86_64

BuildRequires: gcc
BuildRequires: make
BuildRequires: elfutils-libelf-devel


# kmodtool does its magic here
%{expand:%(kmodtool --target %{_target_cpu} --repo rpmfusion --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null) }

%description
CrystalHD extra modules.

%prep
# error out if there was something wrong with kmodtool
%{?kmodtool_check}
# print kmodtool output for debugging purposes:
kmodtool  --target %{_target_cpu} --repo rpmfusion --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null

%setup -q -c
#Copied from kernel sources
install -pm 0644 %{SOURCE1} drivers/staging/crystalhd/Makefile
install -pm 0644 %{SOURCE2} drivers/staging/crystalhd/Kconfig

pushd drivers/staging/crystalhd/
echo "Nothing to patch"
popd

for kernel_version in %{?kernel_versions} ; do
        cp -a drivers/staging/crystalhd _kmod_build_${kernel_version%%___*}
done


%build
for kernel_version  in %{?kernel_versions} ; do
%make_build -C ${kernel_version##*___} \
  M=${PWD}/_kmod_build_${kernel_version%%___*} \
  CONFIG_CRYSTALHD=m \
  V=1\
  modules
done


%install
for kernel_version in %{?kernel_versions}; do
 mkdir -p ${RPM_BUILD_ROOT}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/
 install -D -m 755 -t ${RPM_BUILD_ROOT}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/ $(find _kmod_build_${kernel_version%%___*}/ -name '*.ko')
done
%{?akmod_install}


%changelog
* Tue Jan 28 2025 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 20220825-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Aug 01 2024 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 20220825-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Feb 03 2024 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 20220825-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Aug 02 2023 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 20220825-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Aug 25 2022 Nicolas Chauvet <kwizart@gmail.com> - 20220825-1
- Update snapshot

* Sun Aug 07 2022 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 20170515-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild and ffmpeg
  5.1

* Wed Feb 09 2022 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 20170515-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Aug 02 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 20170515-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Feb 05 2021 Nicolas Chauvet <kwizart@gmail.com> - 20170515-9
- Fix build with 5.10 kernel

* Wed Feb 03 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 20170515-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Aug 17 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 20170515-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Feb 04 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 20170515-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Aug 09 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 20170515-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Mar 04 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 20170515-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 26 2018 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 20170515-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jul 23 2018 Nicolas Chauvet <kwizart@gmail.com> - 20170515-2
- Add patch for 4.17

* Wed May 17 2017 Nicolas Chauvet <kwizart@gmail.com> - 20170515-1
- Update to 20170515

* Fri Feb 10 2017 Nicolas Chauvet <kwizart@gmail.com> - 20170210-1
- Update to 20170210

* Sat Nov 14 2015 Nicolas Chauvet <kwizart@gmail.com> - 20131018-4
- Rebuilt for f23

* Sun Mar 01 2015 Nicolas Chauvet <kwizart@gmail.com> - 20131018-3.5
- Rebuilt for kmod

* Tue Jan 20 2015 Nicolas Chauvet <kwizart@gmail.com> - 20131018-2.5
- Rebuilt for kernel

* Wed Mar 12 2014 Nicolas Chauvet <kwizart@gmail.com> - 20131018-2.4
- Rebuilt for kernel

* Sat Mar 01 2014 Nicolas Chauvet <kwizart@gmail.com> - 20131018-2.3
- Rebuilt for kernel

* Mon Feb 10 2014 Nicolas Chauvet <kwizart@gmail.com> - 20131018-2.2
- Rebuilt for kernel

* Sun Jan 26 2014 Nicolas Chauvet <kwizart@gmail.com> - 20131018-2.1
- Rebuilt for kernel

* Wed Jan 15 2014 Nicolas Chauvet <kwizart@gmail.com> - 20131018-2
- Disable ARM

* Wed Jan 16 2013 Nicolas Chauvet <kwizart@gmail.com> - 20130106-1
- Initial spec file

