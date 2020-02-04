%global buildforkernels akmod
%global debug_package %{nil}

Name:           crystalhd-kmod
Summary:        Kernel module (kmod) for crystalhd
Version:        20170515
Release:        6%{?dist}
License:        GPLv2
URL:            https://github.com/philipl/crystalhd
Source0:        crystalhd-kmod-%{version}.tar.xz
Source1:        crystalhd-Makefile
Source2:        crystalhd-Kconfig
Source11:       crystalhd-kmodtool-excludekernel-filterfile
Patch0:         Linux-4.17-Compatibility.patch
# get the needed BuildRequires (in parts depending on what we build for)
BuildRequires:  %{_bindir}/kmodtool
%{!?kernels:BuildRequires: buildsys-build-rpmfusion-kerneldevpkgs-%{?buildforkernels:%{buildforkernels}}%{!?buildforkernels:current}-%{_target_cpu} }
%{?fedora:BuildRequires: unifdef}
ExclusiveArch:  i686 x86_64


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
%patch0 -p3
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
 chmod u+x %{buildroot}%{_prefix}/lib/modules/*/extra/*/*
done
%{?akmod_install}


%changelog
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

