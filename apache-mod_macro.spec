%define		mod_name	macro
%define 	apxs		/usr/sbin/apxs
Summary:	Apache module to allow macros in apache config files
Summary(pl):	Modu³ do apache pozwalaj±cy u¿ywaæ makr w konfiguracji
Name:		apache-mod_%{mod_name}
Version:	1.1.6
Release:	0.1
License:	Apache
Group:		Networking/Daemons
Source0:	http://www.cri.ensmp.fr/~coelho/mod_macro/mod_%{mod_name}-%{version}.tar.bz2
# Source0-md5:	c79c299f650b35292d3b71da19e42e45
URL:		http://www.cri.ensmp.fr/~coelho/mod_macro/
BuildRequires:	apache-devel
Requires(post,preun):	%{apxs}
Requires:	apache
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR)
%define		_sysconfdir     %(%{apxs} -q SYSCONFDIR)

%description
Apache module to allow macros in apache config files.

%description -l pl
Modu³ do apache pozwalaj±cy u¿ywaæ makr w plikach konfiguracyjnych.

%prep
%setup -q -n mod_%{mod_name}-%{version}

%build
%{apxs} -c mod_%{mod_name}.c

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_pkglibdir}

install .libs/mod_%{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%{apxs} -e -a -n %{mod_name} %{_pkglibdir}/mod_%{mod_name}.so 1>&2
if [ -f /var/lock/subsys/httpd ]; then
	/etc/rc.d/init.d/httpd restart 1>&2
fi

%preun
if [ "$1" = "0" ]; then
	%{apxs} -e -A -n %{mod_name} %{_pkglibdir}/mod_%{mod_name}.so 1>&2
	if [ -f /var/lock/subsys/httpd ]; then
		/etc/rc.d/init.d/httpd restart 1>&2
	fi
fi

%files
%defattr(644,root,root,755)
%doc README CHANGES
%attr(755,root,root) %{_pkglibdir}/*
