#!/bin/bash

wget "http://templateimage.str.cloudn-service.com/ubuntu1404-tso-off.qcow2?AWSAccessKeyId=I5M4F3PLSDGWHR8RSETY&Expires=1509909060&Signature=2d0HGRgK%2FzBur80j9dY1x8pOs0c%3D&x-amz-pt=NGQ4ZWVjOTI3NjE0NzgzNjk3OTA4Nzg" -O ubuntu1404.raw
openstack --os-username admin --os-password secret image create ubuntu --disk-format qcow2 --container-format bare --public --file ./ubuntu1404.raw
nova --os-username admin --os-password secret flavor-create test 99 1024 3 1
