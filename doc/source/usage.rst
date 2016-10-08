========
Usage
========

Adds a config into ``/etc/nova/nova.conf``::

    [DEFAULT]
    scheduler_default_filters=RamFilter,ComputeFilter,AvailabilityZoneFilter,ComputeCapabilitiesFilter,ImagePropertiesFilter,PciPassthroughFilter,NUMATopologyFilter

Sets flavor key as the following command::

    nova flavor-key m1.small set "hw:mem_page_size=large"
