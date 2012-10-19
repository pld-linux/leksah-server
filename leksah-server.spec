Summary:	Leksah is an IDE for Haskell
Name:		leksah-server
Version:	0.12.1.2
Release:	0.1
License:	GPL
Group:		Development/Tools
Source0:	http://hackage.haskell.org/packages/archive/leksah-server/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	7b7838177f3c60e1a15c6451a69b935a
URL:		http://leksah.org/
BuildRequires:	ghc >= 6.12.3
BuildRequires:	rpmbuild(macros) >= 1.608
%requires_releq	ghc
Requires(post,postun):	ghc
#attoparsec >=0.10.0.3 && <0.11,
#attoparsec-enumerator ==0.3.*,
#binary-shared ==0.8.*,
#enumerator >=0.4.14 && <0.5,
BuildRequires:	ghc-hslogger
#ltk >=0.12.1.0 && <0.13,
#strict >=0.3.2 && <0.4
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package provides the interface to GHC-API for leksah.

%prep
%setup -q

%build
runhaskell Setup.lhs configure -v2 --enable-library-profiling \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libexecdir} \
	--docdir=%{_docdir}/%{name}-%{version}

runhaskell Setup.hs build
runhaskell Setup.hs haddock --executables

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d

runhaskell Setup.hs copy --destdir=$RPM_BUILD_ROOT

# work around automatic haddock docs installation
rm -rf %{name}-%{version}-doc
cp -a $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version} %{name}-%{version}-doc

runhaskell Setup.hs register \
	--gen-pkg-config=$RPM_BUILD_ROOT/%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%ghc_pkg_recache

%postun
%ghc_pkg_recache

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/%{name}
%attr(755,root,root) %{_bindir}/leksahecho
%{_datadir}/%{name}-%{version}/data/prefscoll.lkshp
