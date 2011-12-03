%define pkg docbook-slides
Summary: DocBook Slides document type and stylesheets
Name: docbook-slides
Version: 3.4.0
Release: 9%{?dist}
License: MIT
Group: Applications/Text
URL: http://sourceforge.net/projects/docbook
Source0: http://downloads.sourceforge.net/docbook/%{name}-%{version}.tar.gz
Source1: %{name}.xml
Source2: %{name}.cat
Source3: %{name}.README.redhat
#tests update and buildtools could be downloaded at upstream svn ... e.g.
#http://docbook.svn.sourceforge.net/viewvc/docbook/trunk/slides/tests/
Source4: %{name}-tests.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch: noarch
Requires: docbook-dtds
Requires: docbook-xsl
Requires: docbook-simple
Requires: sgml-common
Requires(post): sed
Requires(post): libxml2 >= 2.4.8
Requires(postun): libxml2 >= 2.4.8


%description
DocBook Slides provides customization layers of the both the
Simplified and the full DocBook XML DTD, as well as the DocBook XSL
Stylesheets. This package contains the XML document type definition
and stylesheets for processing DocBook Slides XML. The slides doctype
and stylesheets are for generating presentations, primarily in HTML.

%prep
%setup -q -n %{pkg}-%{version}
tar xf %{SOURCE4}

%build

%install
rm -rf $RPM_BUILD_ROOT

DESTDIR=$RPM_BUILD_ROOT%{_datadir}/xml/docbook/slides/%{version}
mkdir -p $DESTDIR
cp -a browser $DESTDIR
cp -a graphics $DESTDIR
cp -a schema $DESTDIR
cp -a xsl $DESTDIR
cp -a VERSION $DESTDIR
cp -a catalog.xml $DESTDIR

## Install package catalogs into /etc/*ml/ ##

XML_CAT_DIR=$RPM_BUILD_ROOT%{_sysconfdir}/xml
mkdir -p $XML_CAT_DIR
install -p -m 644 %{SOURCE1} $XML_CAT_DIR

SGML_CAT_DIR=$RPM_BUILD_ROOT%{_sysconfdir}/sgml
mkdir -p $SGML_CAT_DIR
install -p -m 644 %{SOURCE2} $SGML_CAT_DIR

cp -p %{SOURCE3} ./README.redhat

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-,root,root, -)
%doc doc
%doc tests
%doc README
%doc NEWS
%doc README.redhat
%dir %{_datadir}/xml/docbook/slides/
%{_datadir}/xml/docbook/slides/%{version}
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/sgml/docbook-slides.cat
%config(noreplace) %{_sysconfdir}/xml/docbook-slides.xml


%post

##################  XML catalog registration #######################

## Define handy variables ##

ROOT_XML_CATALOG=%{_sysconfdir}/xml/catalog
PKG_XML_CATALOG=%{_sysconfdir}/xml/docbook-slides.xml
#LOCAL_XML_CATALOG=/usr/share/xml/docbook/slides/3.4.0/catalog.xml

#
# Register it in the super catalog with the appropriate delegates
#
if [ -w $ROOTCATALOG ]
then
        %{_bindir}/xmlcatalog --noout --add "delegatePublic" \
                "-//Norman Walsh//DTD Slides" \
                "file://$PKG_XML_CATALOG" $ROOT_XML_CATALOG

        %{_bindir}/xmlcatalog --noout --add "delegateSystem" \
                "http://docbook.sourceforge.net/release/slides" \
                "file://$PKG_XML_CATALOG" $ROOT_XML_CATALOG
        %{_bindir}/xmlcatalog --noout --add "delegateURI" \
                "http://docbook.sourceforge.net/release/slides" \
                "file://$PKG_XML_CATALOG" $ROOT_XML_CATALOG
fi
####################################################################


#################  SGML catalog registration  ######################

ROOT_SGML_CATALOG=%{_sysconfdir}/sgml/catalog
PKG_SGML_CATALOG=%{_sysconfdir}/sgml/docbook-slides.cat

#### Root SGML Catalog Entries ####
#### "Delegate" appropriate lookups to package catalog ####

############## use install-catalog ######################

if [ -w $ROOT_SGML_CATALOG ]
then
# xmlcatalog deletes OVERRIDE YES directive, use install-catalog instead
#         /usr/bin/xmlcatalog --sgml --noout --add \
#     "/etc/sgml/docbook-slides.cat"

  install-catalog --add \
  $PKG_SGML_CATALOG \
  $ROOT_SGML_CATALOG 1>/dev/null

# Hack to workaround bug in install-catalog
  sed -i '/^CATALOG.*log\"$/d' $PKG_SGML_CATALOG
  sed -i '/^CATALOG.*log$/d' $PKG_SGML_CATALOG
fi

####################################################################

# Finally, make sure everything in /etc/*ml is readable!
/bin/chmod a+r %{_sysconfdir}/sgml/*
/bin/chmod a+r %{_sysconfdir}/xml/*

%postun
##
## SGML and XML catalogs
##
## Jobs: remove package catalog entries from both root catalogs &
##       remove package catalogs

# remove catalog entries only on removal of package
if [ "$1" = 0 ]; then
  %{_bindir}/xmlcatalog --sgml --noout --del \
    %{_sysconfdir}/sgml/catalog \
    "%{_sysconfdir}/sgml/docbook-slides.cat"

  %{_bindir}/xmlcatalog --noout --del \
    "file://%{_sysconfdir}/xml/docbook-slides.xml" \
    %{_sysconfdir}/xml/catalog
fi

%changelog
* Tue May 18 2010 Ondrej Vasik <ovasik@redhat.com> - 3.4.0-9
- post scriptlet requires sed (#593081)

* Tue Feb 23 2010 Ondrej Vasik <ovasik@redhat.com> - 3.4.0-8
- ship README.redhat instead of README.fedora

* Mon Nov 30 2009 Dennis Gregorovic <dgregor@redhat.com> - 3.4.0-7.1
- Rebuilt for RHEL 6

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Nov 21 2008 Ondrej Vasik <ovasik@redhat.com> - 3.4.0-5
- move tests subdir from tarball (sourceaudit check md5sum
  failure)
- license should be MIT

* Fri Jul 18 2008 Ondrej Vasik <ovasik@redhat.com> - 3.4.0-4
- fix loop in post catalog registration(incomplete sed
  coverage) #455680
- fix broken catalogs for package updates
- fix removal of files during updates

* Tue Nov 06 2007 Ondrej Vasik <ovasik@redhat.com> - 3.4.0-3
- merge review(#225702)
- spec file changed to follow guidelines

* Wed Oct 24 2007 Ondrej Vasik <ovasik@redhat.com> - 3.4.0-2
- rpmlint check
- fixed wrong requirements, some cosmetic changes
- /etc/ files marked as config

* Fri May 25 2007 Ondrej Vasik <ovasik@redhat.com> - 3.4.0-1
- Initial public release
- updated cvs files

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 3.3.1-2.1.1
- rebuild

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Sep  8 2004 Mark Johnson <mjohnson@redhat.com> 3.3.1-1
- Initial public release
- Moved files to /usr/share/xml
- Added SGML catalog registration
- Fixed catalog.xml, which gets broken by xmlcatalog
- Composed README.fedora

* Mon Feb  2 2004 Tim Waugh <twaugh@redhat.com> 3.3.1-0.1
- 3.3.1.

* Tue Dec 23 2003 Tim Waugh <twaugh@redhat.com> 3.3.0-0.1
- 3.3.0.

* Wed Oct 22 2003 Tim Waugh <twaugh@redhat.com> 3.2.0-0.1
- Initial build.


