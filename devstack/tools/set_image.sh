#!/bin/bash

wget "http://templateimage.str.cloudn-service.com/ubuntu1404.raw?AWSAccessKeyId=I5M4F3PLSDGWHR8RSETY&Expires=1509815820&Signature=7iS8sNnuK%2BmAdMv0l%2FWGociasqc%3D&x-amz-pt=NGI1MTQyOTI3NjE0NzgyNzYzMDI4MTQ" -O ubuntu1404.raw
openstack --os-username admin --os-password secret image create ubuntu --disk-format qcow2 --container-format bare --public --file ./ubuntu1404.raw
nova --os-username admin --os-password secret flavor-create test 99 1024 3 1
