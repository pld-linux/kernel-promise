
%define		no_install_post_compress_modules	1

Summary:	Kernel Promise driver
Summary(pl):	Sterownik Promise dla kernela
Name:		kernel-promise
Version:	20021113
Release:	1@%{_kernel_ver_str}
Copyright:	GPL
Group:		Base/Kernel
#Based on http://www.promise.com/support/file/fasttrak_source.zip
Source0:	promise-20021113.tar.bz2
#BuildRequires:	kernel-sources
#Requires:
Patch1:		promise-Makefile.patch
Buildroot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

#%define	_prefix	/usr

%description

%description -l pl

%package -n kernel-smp-promise
Summary:	Kernel SMP Promise driver
Group:		Base/Kernel
Release:	1@%{_kernel_ver_str}
%description -n kernel-smp-promise
%description -l pl -n kernel-smp-promise

%prep 
%setup -q -n promise-%{version}

%patch1 -p1

%build
%{__make} SMP="-D__SMP__ -D_KERNEL_SMP=1"
mv ft.o ft.smp
%{__make} clean
%{__make} SMP=""

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}{,smp}/drivers/ide/

install ft.o $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/drivers/ide
install ft.smp $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/drivers/ide/ft.o

%post
/sbin/depmod -a

%post -n kernel-smp-promise
/sbin/depmod -a

%postun
/sbin/depmod -a

%postun -n kernel-smp-promise
/sbin/depmod -a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%attr(600,root,root) /lib/modules/%{_kernel_ver}/drivers/ide/ft.o

%files -n kernel-smp-promise
%attr(600,root,root) /lib/modules/%{_kernel_ver}smp/drivers/ide/ft.o
