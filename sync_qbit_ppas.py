SOURCE_PPA = "raring"
DEST_PPAS = ["precise", "quantal"]

from launchpadlib.launchpad import Launchpad

launchpad = Launchpad.login_with("QBit's PPAs synchronizer", 'production')

team = launchpad.people["qbit-perl"]

source_ppa = team.getPPAByName(name=SOURCE_PPA)
source_packages = source_ppa.getPublishedSources();

for dest_ppa_name in DEST_PPAS:
    dest_ppa = team.getPPAByName(name=dest_ppa_name)
    dest_packages = dest_ppa.getPublishedSources();

    dest_packages_dict = dict([(p.source_package_name, p.source_package_version) for p in dest_packages])

    for source_package in source_packages:
        if source_package.status <> u'Published':
            continue

        need_sync = False
        if not source_package.source_package_name in dest_packages_dict:
            print "Package '%s (%s)' does not exists in '%s'," % (source_package.source_package_name, dest_packages_dict[source_package.source_package_name], dest_ppa_name),
            need_sync = True

        if source_package.source_package_version > dest_packages_dict[source_package.source_package_name]:
            print "Package '%s (%s)' is outdated in '%s'," % (source_package.source_package_name, dest_packages_dict[source_package.source_package_name], dest_ppa_name),
            need_sync = True

        if need_sync:
            print "synchronizing to version %s" % (source_package.source_package_version)
            dest_ppa.syncSource(
                                from_archive = source_package.archive,
                                source_name  = source_package.source_package_name,
                                version      = source_package.source_package_version,
                                to_series    = dest_ppa_name,
                                to_pocket    = source_package.pocket
                            )
