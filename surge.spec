Name:           surge
Version:        1.8.1
Release:        1%{?dist}
Summary:        Subtractive hybrid synthesizer virtual instrument

# /LICENSE: GPLv3
# /vst3sdk: GPLv3
# /vstgui.surge: BSD
License:        GPLv3 and BSD
URL:            https://surge-synth-team.org

Source0:        https://github.com/surge-synthesizer/releases/releases/download/%{version}/SurgeSrc_%{version}.tgz

BuildRequires:  cmake >= 3.15
BuildRequires:  /usr/bin/g++
BuildRequires:  which
BuildRequires:  python3
BuildRequires:  xcb-util-keysyms-devel
BuildRequires:  cairo-devel
BuildRequires:  libxkbcommon-x11-devel
BuildRequires:  xcb-util-cursor-devel
BuildRequires:  xcb-util-devel
BuildRequires:  libsndfile-devel
BuildRequires:  /usr/bin/pathfix.py python-unversioned-command

%global common_desc \
Surge is an Open Source Digital Synthesizer.

%description
%common_desc

%package -n lv2-%{name}-plugins
Summary:        Surge plugin in LV2 format
Requires:	%{name} = %{version}-%{release}

%description -n lv2-%{name}-plugins
%common_desc

This package contains the LV2 plugin.

%package -n vst3-%{name}-plugins
Summary:        Surge plugin in VST3 format
Requires:	%{name} = %{version}-%{release}

%description -n vst3-%{name}-plugins
%common_desc

This package contains the VST3 plugin.

%prep
%autosetup -n surge

%build
pathfix.py -pni "%{__python3} %{py3_shbang_opts}" .

# Disable code-quality-pipeline-checks
sed -i '/add_custom_target(code-quality-pipeline-checks)/s/^/#/' CMakeLists.txt
sed -i '/add_dependencies(code-quality-pipeline-checks download-extra-content)/s/^/#/' CMakeLists.txt

%if 0%{?fedora}
%cmake -DBUILD_SHARED_LIBS:BOOL=OFF
%cmake_build
%else
%cmake -S . -B %{_vpath_builddir} -DBUILD_SHARED_LIBS:BOOL=OFF
%__cmake --build %{_vpath_builddir} %{?_smp_mflags} --verbose
%endif

%install
install -Dp ./*/surge-headless %{buildroot}%{_bindir}/surge-headless
install --directory %{buildroot}%{_datadir}/surge
cp -r resources/data/. %{buildroot}%{_datadir}/surge/

install --directory %{buildroot}%{_libdir}/vst3
cp -r ./*/surge_products/Surge.vst3 %{buildroot}%{_libdir}/vst3/

install --directory %{buildroot}%{_libdir}/lv2
cp -r ./*/surge_products/Surge.lv2 %{buildroot}%{_libdir}/lv2/

%files
%license LICENSE
%doc README.md AUTHORS
%{_bindir}/surge-headless
%{_datadir}/surge

%files -n lv2-%{name}-plugins
%{_libdir}/lv2/Surge.lv2

%files -n vst3-%{name}-plugins
%{_libdir}/vst3/Surge.vst3

%changelog
* Mon Mar 01 2021 Mattias Ohlsson <mattias.ohlsson@inprose.com> - 1.8.1-1
- Update to 1.8.1

* Tue Apr 14 2020 Mattias Ohlsson <mattias.ohlsson@inprose.com> - 1.6.6-1
- Initial build
