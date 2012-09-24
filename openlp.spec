%define oname	OpenLP

Summary:	Open source Church presentation and lyrics projection application
Name:		openlp
Version:	1.9.12
Release:	%mkrel 1
URL:		http://openlp.org/
Source0:	http://downloads.sourceforge.net/%{name}/%{version}/%{oname}-%{version}.tar.gz
License:	GPLv2
Group:		Publishing
BuildArch:	noarch

BuildRequires:	desktop-file-utils
BuildRequires:	python-devel
BuildRequires:	python-setuptools
BuildRequires:	qt5-devel
Requires:	PyQt4
Requires:	phonon-gstreamer
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

%build
python setup.py build

%install
rm -rf %{buildroot}
python setup.py install --skip-build -O1 --prefix=%{_prefix} --root=%{buildroot}

install -m644 -p -D resources/images/openlp-logo-16x16.png %{buildroot}%{_datadir}/icons/hicolor/16x16/apps/openlp.png
install -m644 -p -D resources/images/openlp-logo-32x32.png %{buildroot}%{_datadir}/icons/hicolor/32x32/apps/openlp.png
install -m644 -p -D resources/images/openlp-logo-48x48.png %{buildroot}%{_datadir}/icons/hicolor/48x48/apps/openlp.png
install -m644 -p -D resources/images/openlp-logo.svg %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/openlp.svg

desktop-file-install --dir %{buildroot}/%{_datadir}/applications resources/openlp.desktop
desktop-file-validate %{buildroot}/%{_datadir}/applications/openlp.desktop

mv %{buildroot}%{_bindir}/openlp.pyw %{buildroot}%{_bindir}/openlp

mkdir -p %{buildroot}%{_datadir}/openlp/i18n/
for TSFILE in resources/i18n/*.ts; do
    lrelease $TSFILE -qm %{buildroot}%{_datadir}/openlp/i18n/`basename $TSFILE .ts`.qm;
done
mkdir -p %{buildroot}%{_datadir}/mime/packages
cp -p resources/openlp.xml %{buildroot}%{_datadir}/mime/packages
install -m644 documentation/%{name}.1 -D %{buildroot}%{_mandir}/man1/%{name}.1

%clean
rm -rf %{buildroot}

%files
%doc copyright.txt
%{_bindir}/openlp
%{_datadir}/mime/packages/openlp.xml
%{_datadir}/applications/openlp.desktop
%{_datadir}/icons/hicolor/*/apps/openlp.*
%{_datadir}/openlp
%{python_sitelib}/openlp/
%exclude %{python_sitelib}/resources/
%{python_sitelib}/OpenLP-%{version}*.egg-info
%{_mandir}/man1/%{name}.1*


