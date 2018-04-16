#!/bin/sh

# getdc.sh - retrieve first component from an LDAP root DSE
# dc=tests,dc=gov,dc=sp -> tests, etc.
#
# $1 - Input file (root_dse)
# $2 - Template file (slapd.conf.skel)
# $3 - output file (slapd.conf)

tempfile=$(mktemp /tmp/getdc.XXXXXX) || { echo "Failed to create temp file"; exit 1; }
sed 's/,/\n/g' $1  > $tempfile
sed -i '2,$d' $tempfile
sed -i 's/dc=//' $tempfile
ROOT_DSE=`cat $1`
DC=`cat $tempfile`
sed s/###ROOT_DSE###/$ROOT_DSE/ $2 > $3
sed -i s/###FIRST_DC_VAL###/$DC/ $3
rm -f $tempfile
