
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
# Source1:	%{name}-1.0.0-locxpms.tar.bz2
# Source10:	%{name}-suse-ext.tar.bz2
# Patch1:		%{name}-1.1.0svn3770-fix_paths.patch

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


# remove (pre-)installed but unused binaries

%build
%{__make} fromtar

%install
%{__rm} -rf "%{buildroot}"
#
#
##### CONVENTIONS IN CONTRAST TO THE ORIGINAL PROJECT DEFAULTS
#
# /opt/rocrail			  !!!!!! unused !!!!!!
#
# /usr/bin			  binaries
# /etc/rocrail			  ini files
# /usr/share/rocrail		  run-time ressources, like libraries and images
# /var/lib/rocrail		  run-time working directory, like track plans and traces
# /var/log/rocrail		  symbolig link to /var/lib/rocrail (Linux FSH conformance)
# /var/tmp/webcam		  optional webcam store
# /etc/init.d			  sysv init script
# /etc/sysconfig		  sysv configuration files
# /usr/share/applications	  desktop parameter files
# /usr/share/desktop-directories  desktop directory files
#
#
##### CREATE MY OWN FILELIST
>%{name}.filelist
#
#
##### BINARIES
echo "%dir %{_bindir}" >>%{name}.filelist
%{__install} -D -m 0755 "unxbin/rocrail" "%{buildroot}%{_bindir}/rocrail"
echo "%{_bindir}/rocrail" >>%{name}.filelist
# %{__install} -D -m 0755 "unxbin/rocgui" "%{buildroot}%{_bindir}/rocgui.bin"
# echo "%{_bindir}/rocgui.bin" >>%{name}.filelist
cat >rocgui.sh <<EOF
#!/bin/sh
if [ ! -e ~/rocrail ] ; then
  mkdir ~/rocrail
fi
if [ ! -r ~/rocrail/rocgui.ini ] ; then
  cp %{_sysconfdir}/rocrail/rocgui.ini ~/rocrail/rocgui.ini
fi
umask 0002
exec %{_bindir}/rocgui.bin -i ~/rocrail/rocgui.ini
EOF
%{__install} -D -m 0755 "rocgui.sh" "%{buildroot}%{_bindir}/rocgui"
echo "%{_bindir}/rocgui" >>%{name}.filelist
#
#
##### LIBRARIES (plug-ins)
echo "%dir %{_datadir}/rocrail" >>%{name}.filelist
for file in unxbin/*.so; do
  %{__install} -D -m 0755 "${file}" "%{buildroot}%{_datadir}/rocrail/$(basename ${file})"
  echo "%{_datadir}/rocrail/$(basename ${file})" >>%{name}.filelist
done
#
#
##### INI FILES (my own too)
echo "%dir %attr(2775,railroad,railroad) %{_sysconfdir}/rocrail" >>%{name}.filelist
%{__install} -D -m 0664 "rocrail/package/rocgui.ini" "%{buildroot}%{_sysconfdir}/rocrail/rocgui.ini"
echo "%config(noreplace) %attr(0664,railroad,railroad) %{_sysconfdir}/rocrail/rocgui.ini" >>%{name}.filelist
%{__install} -D -m 0664 "rocrail/package/rocrail.ini" "%{buildroot}%{_sysconfdir}/rocrail/rocrail-p50.ini"
echo "%config %attr(0664,railroad,railroad) %{_sysconfdir}/rocrail/rocrail-p50.ini" >>%{name}.filelist
%{__install} -D -m 0664 "rocrail/package/rocrail-rci.ini" "%{buildroot}%{_sysconfdir}/rocrail/rocrail-rci.ini"
echo "%config %attr(0664,railroad,railroad) %{_sysconfdir}/rocrail/rocrail-rci.ini" >>%{name}.filelist
# OpenDCC as default ini file for the rocrail daemon
cat >rocrail.ini <<EOF
<rocrail planfile="plan.xml">
  <http/>
  <trace file="rocrail" debug="false" automatic="true" monitor="true"/>
  <digint iid="OpenDCC" lib="opendcc" ptsupport="true" stress="false" device="/dev/ttyUSB0" bps="19200"/>
</rocrail>
EOF
%{__install} -D -m 0664 "rocrail.ini" "%{buildroot}%{_sysconfdir}/rocrail/rocrail-opendcc.ini"
echo "%config %attr(0664,railroad,railroad) %{_sysconfdir}/rocrail/rocrail-opendcc.ini" >>%{name}.filelist
%{__install} -D -m 0664 "rocrail.ini" "%{buildroot}%{_sysconfdir}/rocrail/rocrail.ini"
echo "%config(noreplace) %attr(0664,railroad,railroad) %{_sysconfdir}/rocrail/rocrail.ini" >>%{name}.filelist
#
#
##### TRACE FILE STORE (in /var/log/rocrail symbolic linked to /var/lib/rocrail)
%{__mkdir_p} "%{buildroot}%{_localstatedir}/log"
echo "%dir %{_localstatedir}/log" >>%{name}.filelist
%{__ln_s} "%{_localstatedir}/lib/rocrail" "%{buildroot}%{_localstatedir}/log/rocrail"
echo "%{_localstatedir}/log/rocrail" >>%{name}.filelist
#
#
##### WEBCAM STORE (optional usage)
echo "%dir %{_localstatedir}/tmp" >>%{name}.filelist
echo "%dir %{_localstatedir}/tmp/webcam" >>%{name}.filelist
%{__mkdir_p} "%{buildroot}%{_localstatedir}/tmp/webcam"
#
#
##### TRACK PLANS (primary it is /var/lib/rocrail/plan.xml)
echo "%dir %{_localstatedir}/lib" >>%{name}.filelist
echo "%dir %attr(2775,railroad,railroad) %{_localstatedir}/lib/rocrail" >>%{name}.filelist
for file in rocrail/package/*.xml; do
  %{__install} -D -m 0664 "${file}" "%{buildroot}%{_localstatedir}/lib/rocrail/$(basename ${file})"
  echo "%attr(0664,railroad,railroad) %{_localstatedir}/lib/rocrail/$(basename ${file})" >>%{name}.filelist
done
%{__cp} "%{buildroot}%{_localstatedir}/lib/rocrail/plan.xml" "%{buildroot}%{_localstatedir}/lib/rocrail/plan-orig.xml"
echo "%attr(0664,railroad,railroad) %{_localstatedir}/lib/rocrail/plan-orig.xml" >>%{name}.filelist
#
#
##### CREATE THE OCCUPATION FILE
echo "<modocc/>" > "occ.xml"
%{__install} -D -m 0664 "occ.xml" "%{buildroot}%{_localstatedir}/lib/rocrail/occ.xml"
echo "%attr(0664,railroad,railroad) %{_localstatedir}/lib/rocrail/occ.xml" >>%{name}.filelist
#
#
##### APPLICATION STYLESHEETS
echo "%dir %{_datadir}/rocrail" >>%{name}.filelist
echo "%dir %{_datadir}/rocrail/stylesheets" >>%{name}.filelist
for file in stylesheets/*.xsl; do
  %{__install} -D -m 0644 "${file}" "%{buildroot}%{_datadir}/rocrail/stylesheets/$(basename ${file})"
  echo "%{_datadir}/rocrail/stylesheets/$(basename ${file})" >>%{name}.filelist
done
#
#
##### APPLICATION TRACK THEMES
echo "%dir %{_datadir}/rocrail" >>%{name}.filelist
echo "%dir %{_datadir}/rocrail/svg" >>%{name}.filelist
echo "%dir %{_datadir}/rocrail/svg/themes" >>%{name}.filelist
for dir in rocgui/svg/themes/*; do
  echo "%dir %{_datadir}/rocrail/svg/themes/$(basename ${dir})" >>%{name}.filelist
  for file in ${dir}/*.svg; do
    %{__install} -D -m 0644 "${file}" "%{buildroot}%{_datadir}/rocrail/svg/themes/$(basename ${dir})/$(basename ${file})"
    echo "%{_datadir}/rocrail/svg/themes/$(basename ${dir})/$(basename ${file})" >>%{name}.filelist
  done
done
#
#
##### APPLICATION LOGO
%{__install} -D -m 0644 "rocrail/package/rocraild.png" "%{buildroot}%{_datadir}/rocrail/rocraild.png"
echo "%{_datadir}/rocrail/rocraild.png" >>%{name}.filelist
%{__install} -D -m 0644 "rocrail/package/rocrail.xpm" "%{buildroot}%{_datadir}/rocrail/rocrail.xpm"
echo "%{_datadir}/rocrail/rocrail.xpm" >>%{name}.filelist
#
#
##### APPLICATION ICONS
echo "%dir %{_datadir}/rocrail" >>%{name}.filelist
echo "%dir %{_datadir}/rocrail/icons" >>%{name}.filelist
for file in rocgui/icons/*.png; do
  %{__install} -D -m 0644 "${file}" "%{buildroot}%{_datadir}/rocrail/icons/$(basename ${file})"
  echo "%{_datadir}/rocrail/icons/$(basename ${file})" >>%{name}.filelist
done
#
#
##### APPLICATION SYMBOLS
echo "%dir %{_datadir}/rocrail/symbols" >>%{name}.filelist
for file in rocrail/symbols/*.*; do
  %{__install} -D -m 0644 "${file}" "%{buildroot}%{_datadir}/rocrail/symbols/$(basename ${file})"
  echo "%{_datadir}/rocrail/symbols/$(basename ${file})" >>%{name}.filelist
done
#
#
##### APPLICATION IMAGES (locomotives and more)
echo "%dir %{_datadir}/rocrail/images" >>%{name}.filelist
for file in xpm/locxpm/*.xpm; do
  %{__install} -D -m 0644 "${file}" "%{buildroot}%{_datadir}/rocrail/images/$(basename ${file})"
  echo "%{_datadir}/rocrail/images/$(basename ${file})" >>%{name}.filelist
done
#
#
##### SYSV INIT SCRIPTS
echo "%dir %{_sysconfdir}/init.d" >>%{name}.filelist
%{__install} -D -m 0755 "suse/init.rocrail" "%{buildroot}%{_sysconfdir}/init.d/rocrail"
echo "%{_sysconfdir}/init.d/rocrail" >>%{name}.filelist
%{__mkdir_p} "%{buildroot}%{_sbindir}"
%{__ln_s} "%{_sysconfdir}/init.d/rocrail" "%{buildroot}%{_sbindir}/rcrocrail"
echo "%{_sbindir}/rcrocrail" >>%{name}.filelist
#
#
##### SYSTEM SETUP CONFIGURATION
%if 0%{?suse_version} > 1020
echo "%dir /var/adm/fillup-templates" >>%{name}.filelist
%{__install} -D -m 644 "suse/sysconfig.rocrail" "%{buildroot}/var/adm/fillup-templates/sysconfig.rocrail"
echo "/var/adm/fillup-templates/sysconfig.rocrail" >>%{name}.filelist
%endif
#
#
##### LOG FILE ROTATION
echo "%dir %{_sysconfdir}/logrotate.d" >>%{name}.filelist
%{__install} -D -m 0644 "suse/logrotate.rocrail" "%{buildroot}%{_sysconfdir}/logrotate.d/rocrail"
echo "%{_sysconfdir}/logrotate.d/rocrail" >>%{name}.filelist
#
#
##### SuSE FIREWALL CONFIGURATION
%if 0%{?suse_version} > 1020
echo "%dir %{_sysconfdir}/sysconfig/SuSEfirewall2.d/services" >>%{name}.filelist
%{__install} -D -m 0644 "suse/SuSEfirewall.rocrail" "%{buildroot}%{_sysconfdir}/sysconfig/SuSEfirewall2.d/services/rocrail"
echo "%{_sysconfdir}/sysconfig/SuSEfirewall2.d/services/rocrail" >>%{name}.filelist
%endif
#
#
##### DESKTOP INTEGRATION
#{__install} -D -m 0644 rocrail/package/Rocrail.directory	\
#			"%{buildroot}%{_datadir}/desktop-directories/Rocrail.directory"
#{__install} -D -m 0644 rocrail/package/Rocrail.desktop	\
#			"%{buildroot}%{_datadir}/applications/Rocrail.desktop"
#{__install} -D -m 0644 rocrail/package/RocrailGUI.desktop	\
#			"%{buildroot}%{_datadir}/applications/RocrailGUI.desktop"
echo "%dir %{_datadir}/applications" >>%{name}.filelist
%{__install} -D -m 0644 suse/rocgui.desktop	\
			"%{buildroot}%{_datadir}/applications/rocgui.desktop"
echo "%{_datadir}/applications/rocgui.desktop" >>%{name}.filelist
#
#
##### DOCUMENTS
echo "%doc %attr(0644,root,root) README COPYING changelog.txt" >>%{name}.filelist
echo "%doc %attr(0644,root,root) howto-crosscompile.txt build.html" >>%{name}.filelist
echo "%doc %attr(0644,root,root) roclcdr/doc/lcdriver.dia" >>%{name}.filelist

%clean
%{__rm} -rf "%{buildroot}"

%if 0%{?suse_version}
%post
%{fillup_and_insserv -n rocrail rocrail}
%endif

%preun
%stop_on_removal srcpd

%postun
%restart_on_update rocrail
%insserv_cleanup

%files -f %{name}.filelist
%defattr(-,root,root)

