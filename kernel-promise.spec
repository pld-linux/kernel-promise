#
# Conditional build:
# _without_dist_kernel	- without kernel from distribution
#
Summary:	Kernel Promise driver
Summary(pl):	Sterownik Promise dla Linuksa
Name:		kernel-promise
Version:	20021113
%define	rel	2
Release:	%{rel}@%{_kernel_ver_str}
License:	BSD-like with partial source only
Group:		Base/Kernel
#Based on http://www.promise.com/support/file/fasttrak_source.zip
Source0:	promise-20021113.tar.bz2
# Source0-md5:	69e3896805a6a3d00808cf73d6af0039
Patch1:		promise-Makefile.patch
%{!?_without_dist_kernel:BuildRequires:	kernel-source}
%{!?_without_dist_kernel:%requires_releq_kernel_up}
Requires(post,postun):	/sbin/depmod
ExclusiveArch:	%{ix86}
Buildroot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Kernel Promise driver.

%description -l pl
Sterownik Promise dla Linuksa.

%package -n kernel-smp-promise
Summary:	Kernel SMP Promise driver
Summary(pl):	Sterownik Promise dla Linuksa SMP
Release:	%{rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{!?_without_dist_kernel:%requires_releq_kernel_up}
Requires(post,postun):	/sbin/depmod

%description -n kernel-smp-promise
Kernel SMP Promise driver.

%description -n kernel-smp-promise -l pl
Sterownik Promise dla Linuksa SMP.

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

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/depmod -a %{!?_without_dist_kernel:-F /boot/System.map-%{_kernel_ver} }%{_kernel_ver}

%postun
/sbin/depmod -a %{!?_without_dist_kernel:-F /boot/System.map-%{_kernel_ver} }%{_kernel_ver}

%post	-n kernel-smp-promise
/sbin/depmod -a %{!?_without_dist_kernel:-F /boot/System.map-%{_kernel_ver}smp }%{_kernel_ver}smp

%postun	-n kernel-smp-promise
/sbin/depmod -a %{!?_without_dist_kernel:-F /boot/System.map-%{_kernel_ver}smp }%{_kernel_ver}smp

%files
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/drivers/ide/ft.o*

%files -n kernel-smp-promise
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}smp/drivers/ide/ft.o*
