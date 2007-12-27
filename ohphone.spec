%define	snap	20071226

Summary:	Initiate, or receive, a H.323 IP telephony call
Name:		ohphone
Version:	1.4.6
Release:	%mkrel 0.%{snap}.1
License:	MPL
Group:		Networking/Other
URL:		http://openh323.sourceforge.net/
Source0:	%{name}-%{snap}.tar.lzma
Patch0:		ohphone-1.2.11-openh323path.patch
# Define NO_H323_VIDEO so it doesn't try to build video code, which
# uses codecs openh323 / h323plus haven't supported for a while
Patch1:		ohphone-1.4.6-novideo.patch
# The variable this code tries to use doesn't exist in h323plus /
# pwlib any more, so disable it
Patch2:		ohphone-1.4.6-missingvar.patch
BuildRequires:	openh323-devel
BuildRequires:	pwlib-devel
BuildRequires:	libxext-static-devel
BuildRequires:	libx11-static-devel
BuildRequires:	x11-proto-devel
BuildConflicts:	svgalib-devel
Epoch:		1
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description 
ohphone is a command line application that can be used to listen for
incoming H.323 calls, or to initiate a call to a remote host. Although
originally intended as a test harneess for the OpenH323 project (see
http://www.openh323.org) it has developed into a fully functional
H.323 endpoint application.

%prep
%setup -q -n %{name}
%patch0 -p1 -b .openh323path
%patch1 -p1 -b .novideo
%patch2 -p1 -b .missingvar

%build
# Fix X location, avoid patch
perl -pi -e 's,/usr/X11R6/include/,%{_includedir},g' Makefile
perl -pi -e 's,/usr/X11R6/lib/,%{_libdir},g' Makefile

export CFLAGS="%{optflags} -DLDAP_DEPRECATED"
export CXXFLAGS="%{optflags} -DLDAP_DEPRECATED"

%make \
    OPTCCFLAGS="%{optflags}" \
    PWLIBDIR=%{_datadir}/pwlib \
    OPENH323DIR=%{_prefix} \
    PREFIX=%{_prefix} \
    PWLIB_BUILD=1 \
    OH323_LIBDIR=%{_libdir} \
    NO_H323_VIDEO=1 \
    optshared

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -d %{buildroot}{%{_bindir},%{_mandir}/man1}
%ifarch %ix86
install -m0755 obj_linux_x86_?/%{name} %{buildroot}%{_bindir}
%else
%ifarch alpha
install -m0755 obj_linux_%{_arch}-*/%{name} %{buildroot}%{_bindir}
%else
install -m0755 obj_linux_%{_arch}_*/%{name} %{buildroot}%{_bindir}
%endif
%endif
install -m0644 %{name}.1 %{buildroot}%{_mandir}/man1

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(0644,root,root,0755)
%doc ReadMe.txt
%attr(0755,root,root) %{_bindir}/*
%{_mandir}/man*/*
