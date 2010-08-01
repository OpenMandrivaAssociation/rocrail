
Requires:	railroad-lsb >= 0


BuildRequires:	gcc-c++
BuildRequires:	wxGTK-devel >= 2.6 bzr

AutoReqProv:	On
%define oname	Rocrail
%define svnrel	Act

Name:		rocrail
License:	GPL
Group:		Networking/Other
Summary:	Model Railroad Control System
Summary(de):	Steuersystem für Modelleisenbahnen
Version:	1.2.6
Release:	%mkrel 1
URL:		http://www.rocrail.net/
BuildRoot:	%{_tmppath}/build-%{name}-%{version}-%{svnrel}
Source:		%{oname}-%{svnrel}-%{version}.tar.bz2

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
%setup -q -n Rocrail-Act-1.2

%build
%{__make} fromtar

%install
%{__rm} -rf "%{buildroot}"
mkdir -p $RPM_BUILD_ROOT%{_libdir}/rocrail
mkdir -p $RPM_BUILD_ROOT%{_libdir}/rocrail/default
mkdir -p $RPM_BUILD_ROOT%{_libdir}/rocrail/icons
mkdir -p $RPM_BUILD_ROOT%{_libdir}/rocrail/svg
mkdir -p $RPM_BUILD_ROOT%{_libdir}/rocrail/stylesheets
mkdir -p $RPM_BUILD_ROOT%{_libdir}/rocrail/symbols
mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
mkdir -p $RPM_BUILD_ROOT%{_datadir}/desktop-directories
mkdir -p $RPM_BUILD_ROOT/etc/init.d

install -s -m 755 unxbin/rocrail $RPM_BUILD_ROOT%{_libdir}/rocrail/rocrail
install -s -m 755 unxbin/lcdriver.so $RPM_BUILD_ROOT%{_libdir}/rocrail/lcdriver.so
install -s -m 755 unxbin/barjut.so $RPM_BUILD_ROOT%{_libdir}/rocrail/barjut.so
install -s -m 755 unxbin/hsi88.so $RPM_BUILD_ROOT%{_libdir}/rocrail/hsi88.so
install -s -m 755 unxbin/p50.so $RPM_BUILD_ROOT%{_libdir}/rocrail/p50.so
install -s -m 755 unxbin/p50x.so $RPM_BUILD_ROOT%{_libdir}/rocrail/p50x.so
install -s -m 755 unxbin/srcp.so $RPM_BUILD_ROOT%{_libdir}/rocrail/srcp.so
install -s -m 755 unxbin/dinamo.so $RPM_BUILD_ROOT%{_libdir}/rocrail/dinamo.so
install -s -m 755 unxbin/om32.so $RPM_BUILD_ROOT%{_libdir}/rocrail/om32.so
install -s -m 755 unxbin/lenz.so $RPM_BUILD_ROOT%{_libdir}/rocrail/lenz.so
install -s -m 755 unxbin/roco.so $RPM_BUILD_ROOT%{_libdir}/rocrail/roco.so
install -s -m 755 unxbin/zimo.so $RPM_BUILD_ROOT%{_libdir}/rocrail/zimo.so
install -s -m 755 unxbin/ddx.so $RPM_BUILD_ROOT%{_libdir}/rocrail/ddx.so
install -s -m 755 unxbin/slx.so $RPM_BUILD_ROOT%{_libdir}/rocrail/slx.so
install -s -m 755 unxbin/loconet.so $RPM_BUILD_ROOT%{_libdir}/rocrail/loconet.so
install -s -m 755 unxbin/opendcc.so $RPM_BUILD_ROOT%{_libdir}/rocrail/opendcc.so
install -s -m 755 unxbin/rocgui $RPM_BUILD_ROOT%{_libdir}/rocrail/rocgui
install -s -m 755 unxbin/virtual.so $RPM_BUILD_ROOT%{_libdir}/rocrail/virtual.so

install -g users -m 666 rocrail/package/Rocrail.directory $RPM_BUILD_ROOT%{_datadir}/desktop-directories
install -g users -m 666 rocrail/package/Roc*.desktop $RPM_BUILD_ROOT%{_datadir}/applications

install -m 755 rocrail/package/roc*.sh $RPM_BUILD_ROOT%{_libdir}/rocrail
install -g users -m 666 rocrail/package/rocraild.png $RPM_BUILD_ROOT%{_libdir}/rocrail
install -g users -m 666 rocrail/package/rocraild $RPM_BUILD_ROOT/etc/init.d
install -g users -m 666 rocrail/package/rocrail.xpm $RPM_BUILD_ROOT%{_libdir}/rocrail
install -g users -m 666 rocrail/package/roc*.ini $RPM_BUILD_ROOT%{_libdir}/rocrail/default
install -g users -m 666 rocrail/package/plan.xml $RPM_BUILD_ROOT%{_libdir}/rocrail/default
install -g users -m 666 rocrail/package/neustadt.xml $RPM_BUILD_ROOT%{_libdir}/rocrail/default

install -g users -m 666 rocgui/icons/*.* $RPM_BUILD_ROOT%{_libdir}/rocrail/icons
install -g users -m 666 stylesheets/*.* $RPM_BUILD_ROOT%{_libdir}/rocrail/stylesheets
install -d -g users -m 666 rocgui/svg/* $RPM_BUILD_ROOT%{_libdir}/rocrail/svg
install -g users -m 666 symbols/*.* $RPM_BUILD_ROOT%{_libdir}/rocrail/symbols

%clean
#rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc

%{_libdir}/rocrail/rocrail
%{_libdir}/rocrail/lcdriver.so
%{_libdir}/rocrail/hsi88.so
%{_libdir}/rocrail/p50.so
%{_libdir}/rocrail/p50x.so
%{_libdir}/rocrail/srcp.so
%{_libdir}/rocrail/dinamo.so
%{_libdir}/rocrail/om32.so
%{_libdir}/rocrail/zimo.so
%{_libdir}/rocrail/lenz.so
%{_libdir}/rocrail/roco.so
%{_libdir}/rocrail/ddx.so
%{_libdir}/rocrail/virtual.so
%{_libdir}/rocrail/slx.so
%{_libdir}/rocrail/barjut.so
%{_libdir}/rocrail/loconet.so
%{_libdir}/rocrail/opendcc.so
%{_libdir}/rocrail/rocgui
%{_libdir}/rocrail/default/plan.xml
%{_libdir}/rocrail/default/neustadt.xml
%{_libdir}/rocrail/default/rocrail.ini
%{_libdir}/rocrail/default/rocgui.ini
%{_libdir}/rocrail/rocrail.sh
%{_libdir}/rocrail/rocgui.sh
%{_libdir}/rocrail/rocraild.png
/etc/init.d/rocraild
%{_libdir}/rocrail/rocrail.xpm
%{_libdir}/rocrail/icons/*.*
%{_libdir}/rocrail/stylesheets/*.*
%{_libdir}/rocrail/svg
%{_libdir}/rocrail/symbols/*.*
%{_datadir}/desktop-directories/Rocrail.directory
%{_datadir}/applications/Rocrail.desktop
%{_datadir}/applications/RocrailGUI.desktop



