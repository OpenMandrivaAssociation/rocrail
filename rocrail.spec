# FIXME: str fmt check is temporarily disabled
# as priority is to get package working even somehow (wally 08/2010)
%define Werror_cflags %nil

%define _provides_exceptions .\\+\\.so$

%define oname	Rocrail
%define rname	air
%define revno	986
%define rel	1

Name:		rocrail
License:	GPLv2+
Group:		Networking/Other
Summary:	Model Railroad Control System
Version:	1.3
Release:	%mkrel -c rev%{revno} %{rel}
URL:		http://www.rocrail.net/
BuildRoot:	%{_tmppath}/build-%{name}-%{version}-%{svnrel}
Source:		%{name}-%{version}-%{rname}-revno%{revno}.tar.gz
Patch1:		rocrail-fix_makefile.patch
BuildRequires:  gcc-c++
BuildRequires:  wxGTK-devel >= 2.6
BuildRequires:  bzr
Requires(post):	rpm-helper
Requires(preun):	rpm-helper

%description
RocRail is a C/C++ control viewing program for a digital
model railroad in manual and automatic mode. Supported
multiple controllers:
     * Marklin 6050
     * IntelliBox P50x
     * SRCP
     * HSI88
     * Dinamo
     * OM32
     * Lenz
     * Selectrix
     * Zimo
     * ECoS
     * Loconet
     * OpenDCC

RocRail is a 2 tier application written for Linux and Windows
in C/C++ based on the wxWidgets class library.

%prep
%setup -q -n %{oname}-Air
%patch1 -p1

%build
#fix filename
mv "rocview/svg/themes/DB/signaldistant -2.svg" rocview/svg/themes/DB/signaldistant-2.svg

#fix build flags
find . -name "makefile" -exec sed -i -e 's|CC_EXTRA_FLAGS=.*|CC_EXTRA_FLAGS=-fPIC %{optflags}|g' {} \;
find . -name "makefile" -exec sed -i -e 's|LNK_FLAGS=|LNK_FLAGS+=|g' {} \;
find . -name "makefile" -exec sed -i -e 's|DEBUG=.*|DEBUG=|g' {} \;

export LNK_FLAGS="%{ldflags}"

#fix init script
sed -i -e 's,rocraild_BIN=.*,rocraild_BIN=%{_libdir}/%{name}/rocrail,g' rocrail/package/rocraild
sed -i -e 's,rocraild_PID=.*,rocraild_PID=%{_var}/run/rocraild.pid,g' rocrail/package/rocraild
sed -i -e 's,rocraild_SH=.*,rocraild_SH=%{_libdir}/%{name}/rocraild.sh,g' rocrail/package/rocraild

%make fromtar

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot}%{_libdir}/%{name} install

#install files which install doesn't handle
mkdir -p %{buildroot}%{_datadir}/applications
mkdir -p %{buildroot}%{_datadir}/desktop-directories
mkdir -p %{buildroot}%{_initrddir}
mkdir -p %{buildroot}%{_iconsdir}
mkdir -p %{buildroot}%{_bindir}

install -m 755 rocrail/package/rocraild $RPM_BUILD_ROOT%{_initrddir}/rocraild

mv	%{buildroot}%{_libdir}/%{name}/%{name}.xpm \
	%{buildroot}%{_libdir}/%{name}/rocraild.png \
	%{buildroot}%{_iconsdir}

#desktop files
cat > %{buildroot}%{_datadir}/applications/rocrail.desktop << EOF
[Desktop Entry]
Type=Application
Terminal=true
Exec=%{name}
Icon=rocraild
Name=Rocrail
Categories=Utility;
EOF

cat > %{buildroot}%{_datadir}/applications/rocview.desktop << EOF
[Desktop Entry]
Type=Application
Exec=rocview
Icon=%{name}
Name=Rocview
Categories=Utility;
EOF

#binary scripts
cat > %{buildroot}%{_bindir}/rocrail << EOF
#!/bin/sh
if [ ! -e ~/.rocrail ] ; then
	mkdir ~/.rocrail
fi

cd ~/.rocrail

if pidof rocrail
  then
    echo "rocrail is running"
  else
    echo "rocrail is not running. start..."
    %{_libdir}/rocrail/rocrail -console -l %{_libdir}/rocrail
fi
EOF

cat > %{buildroot}%{_bindir}/rocview << EOF
#!/bin/sh
if [ ! -e ~/.rocrail ] ; then
	mkdir ~/.rocrail
fi

if [ ! -e ~/.rocrail/rocview.ini ] ; then
	cp %{_libdir}/rocrail/plan.xml ~/.rocrail
fi

if [ ! -e ~/.rocrail/svg ] ; then
	ln -s %{_libdir}/rocrail/svg ~/.rocrail/svg
fi

if [ ! -e ~/.rocrail/images ] ; then
	ln -s %{_libdir}/rocrail/images ~/.rocrail/images
fi

cd ~/.rocrail

%{_libdir}/rocrail/rocview -sp %{_libdir}/rocrail -themespath . $1 $2 $3
EOF

cat > %{buildroot}%{_libdir}/%{name}/rocraild.sh << EOF
#!/bin/sh
cd %{_libdir}/rocrail/
rm -f nohup.out
nohup ./rocrail -l %{_libdir}/rocrail&
EOF

#ugly workaround
echo 'echo "$!" > /var/run/rocraild.pid' >> %{buildroot}%{_libdir}/%{name}/rocraild.sh

#fix rights
chmod 644 %{buildroot}%{_libdir}/%{name}/plan.xml
chmod 755 %{buildroot}%{_libdir}/%{name}/rocraild.sh

#clean empty files
find %{buildroot}%{_libdir}/%{name} -size 0 -type f -exec rm -rf {} \;

%clean
rm -rf %{buildroot}

%post
%_post_service rocraild

%preun
%_preun_service rocraild

%files
%defattr(-,root,root)
%doc README
%{_libdir}/%{name}
%attr(755,root,root) %{_bindir}/roc*
%{_datadir}/applications/roc*.desktop
%{_initrddir}/rocraild
%{_iconsdir}/roc*
