%define underscore() %(echo %1 | sed 's/-/_/g')

Summary:       ARGO probe that checks JSON response given the URL
Name:          argo-probe-json
Version:       0.1.1
Release:       1%{?dist}
Source0:       %{name}-%{version}.tar.gz
License:       ASL 2.0
Group:         Development/System
BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Prefix:        %{_prefix}
BuildArch:     noarch

BuildRequires: python3-devel
Requires: python3-requests


%description
ARGO probe that checks JSON response given the URL


%prep
%setup -q


%build
%{py3_build}


%install
%{py3_install "--record=INSTALLED_FILES" }


%clean
rm -rf $RPM_BUILD_ROOT


%files -f INSTALLED_FILES
%defattr(-,root,root)
%dir %{python3_sitelib}/%{underscore %{name}}/
%{python3_sitelib}/%{underscore %{name}}/*.py


%changelog
* Thu Apr 10 2025 Katarina Zailac <kzailac@srce.hr> - 0.1.1-1
- ARGO-4976 Avoid displaying of URL in probe results
- ARGO-4970 Check if value is true/false in generic json probe
- ARGO-4810 Create json parser probe
