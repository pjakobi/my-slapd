MYPWD:=$(shell slappasswd -T password)
TEMP_FILE:=$(shell mktemp /tmp/myslapd.XXXXXX)


all: slapd.conf basedomain.ldif

slapd.conf:
	@./getdc.sh ./root_dse ./slapd.conf.skel ./slapd.conf

	
	@echo $(MYPWD)
	@echo $(TEMP_FILE)
	@echo -n 'rootpw ' > $(TEMP_FILE)
	@echo  $(MYPWD) >> $(TEMP_FILE)
	@echo "Sed 1"
	sed -i '/rootpw/r $(TEMP_FILE)' $@
	@echo "Sed 2"
#
	sed -i '/rootpw$$/d' $@

basedomain.ldif:
	@./getdc.sh ./root_dse ./basedomain.ldif.skel ./basedomain.ldif

clean:
	@rm -f slapd.conf basedomain.ldif $(TEMP_FILE)
