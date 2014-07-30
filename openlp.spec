%define oname	OpenLP

Summary:	Open source Church presentation and lyrics projection application
Name:		openlp
Version:	2.0.5
Release:	1
URL:		http://openlp.org/en/
Source0:	http://downloads.sourceforge.net/%{name}/%{oname}-%{version}.tar.gz
License:	GPLv2
Group:		Publishing
BuildArch:	noarch

BuildRequires:	desktop-file-utils
BuildRequires:	python-devel
BuildRequires:	python-setuptools
BuildRequires:	qt4-devel
Requires:	vlc
Requires:	PyQt4
Requires:	python-qt4-phonon
Requires:	phonon-backend
Requires:	python-beautifulsoup
Requires:	python-chardet
Requires:	python-lxml
Requires:	python-sqlalchemy
Requires:	python-enchant
Requires:	python-mako
Requires:	python-sqlalchemy-migrate
Requires:	hicolor-icon-theme
Requires:	libreoffice-graphicfilter
Requires:	libreoffice-impress
Requires:	libreoffice-headless

%description
openlp is a church presentation software, for lyrics projection software,
used to display slides of Songs, Bible verses, videos, images, and
presentations via LibreOffice using a computer and projector.


%prep
%setup -q -n %{oname}-%{version}
# Needed to prevent /usr/lib/python2.7/site-packages/resources from being built
rm resources/__init__.py

%build
python setup.py build

# Compile the translation files and copy them to the correct directory
# Presumes you are in the base directory of OpenLP

%install
python setup.py install --skip-build -O1 --prefix=%{_prefix} --root=%{buildroot}

install -m644 -p -D resources/images/openlp-logo-16x16.png %{buildroot}%{_datadir}/icons/hicolor/16x16/apps/openlp.png
install -m644 -p -D resources/images/openlp-logo-32x32.png %{buildroot}%{_datadir}/icons/hicolor/32x32/apps/openlp.png
install -m644 -p -D resources/images/openlp-logo-48x48.png %{buildroot}%{_datadir}/icons/hicolor/48x48/apps/openlp.png
install -m644 -p -D resources/images/openlp-logo.svg %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/openlp.svg

mv %{buildroot}%{_bindir}/openlp.pyw %{buildroot}%{_bindir}/openlp

mkdir -p %{buildroot}%{_datadir}/openlp/i18n/
for TSFILE in resources/i18n/*.ts; do
    lrelease $TSFILE -qm %{buildroot}%{_datadir}/openlp/i18n/`basename $TSFILE .ts`.qm;
done

mkdir -p %{buildroot}%{_datadir}/mime/packages
cp -p resources/openlp.xml %{buildroot}%{_datadir}/mime/packages


%post
touch --no-create %{_datadir}/icons/hicolor ||:
gtk-update-icon-cache -q %{_datadir}/icons/hicolor 2> /dev/null ||:
update-mime-database %{_datadir}/mime &> /dev/null ||:
update-desktop-database &> /dev/null ||:

%postun
touch --no-create %{_datadir}/icons/hicolor ||:
gtk-update-icon-cache -q %{_datadir}/icons/hicolor 2> /dev/null ||:
update-mime-database %{_datadir}/mime &> /dev/null ||:
update-desktop-database &> /dev/null ||:

%files
%defattr(-,root,root)
%doc copyright.txt LICENSE
%{_bindir}/openlp
%{_datadir}/mime/packages/openlp.xml
%{_datadir}/applications/openlp.desktop
%{_datadir}/icons/hicolor
%{_datadir}/openlp
%{python_sitelib}/openlp/
%{python_sitelib}/%{name}-%{version}*.egg-info
%{_mandir}/man1/%{name}.1*

