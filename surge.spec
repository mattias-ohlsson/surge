%define debug_package %{nil}

Name:           surge
Version:        1.6.6
Release:        1%{?dist}
Summary:        Surge Synthesizer

# /LICENSE: GPLv3
# /vst3sdk @ 10287bc: GPLv3
# /vstgui.surge @ 313faee: BSD
License:        GPLv3 and BSD
URL:            https://surge-synthesizer.github.io

# Build source commands:
# VERSION=$(grep ^Version *.spec | cut -d' ' -f9)
# grep "^#    " *.spec | sed 's|#    ||' | sed "s|VERSION|$VERSION|g" | bash

# Build source script:
#    #!/bin/bash
#    git clone https://github.com/surge-synthesizer/surge.git --branch release/VERSION --single-branch surge-VERSION
#    cd surge-VERSION
#    git submodule update --init --recursive
#    rm -rf .git
#    cd ..
#    tar cvjf surge-VERSION.tar.gz surge-VERSION

Source0:        %{name}-%{version}.tar.gz

BuildRequires:  /usr/bin/premake5 /usr/bin/g++ cmake which python3
BuildRequires:  cairo-devel libxkbcommon-x11-devel xcb-util-cursor-devel xcb-util-keysyms-devel xcb-util-devel
BuildRequires:  libsndfile-devel
BuildRequires:  rsync
BuildRequires:  /usr/bin/pathfix.py

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
%autosetup

%build

sed -i "s|/usr/lib/vst|%{buildroot}%{_libdir}/vst|" build-linux.sh
sed -i "s|/usr/lib/vst3|%{buildroot}%{_libdir}/vst3|" build-linux.sh
sed -i "s|/usr/lib/lv2|%{buildroot}/%{_libdir}/lv2|" build-linux.sh
sed -i "s|/usr/bin|%{buildroot}%{_bindir}|" build-linux.sh
sed -i "s|/usr/share/Surge|%{buildroot}%{_datadir}/Surge|" build-linux.sh

pathfix.py -pni "%{__python3} %{py3_shbang_opts}" .
pathfix.py -pni "%{__python3} %{py3_shbang_opts}" libs/lv2/waf
pathfix.py -pni "%{__python3} %{py3_shbang_opts}" libs/lv2/waflib/waf
pathfix.py -pni "%{__python3} %{py3_shbang_opts}" scripts/linux/generate-lv2-ttl.py
sed -i 's|python|python3|g' premake5.lua CMakeLists.txt

./build-linux.sh build

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_datadir}

./build-linux.sh install

mv %{buildroot}%{_bindir}/Surge-Headless/Surge/Surge-Headless %{buildroot}%{_bindir}/surge-headless
rm -rf %{buildroot}%{_bindir}/Surge-Headless

%files
%license LICENSE
%doc README.md AUTHORS

%{_bindir}/surge-headless
%{_datadir}/Surge

%files -n lv2-%{name}-plugins
%{_libdir}/lv2/Surge.lv2

%files -n vst3-%{name}-plugins
%{_libdir}/vst3/Surge.vst3

%changelog
* Tue Apr 14 2020 Mattias Ohlsson <mattias.ohlsson@inprose.com> - 1.6.6-1
- Initial build
