
SHELL:=/bin/csh
MPROJNAME='T065GPC00_aa'
MTOPCELLNAME='ara'
MTOPLIBNAME='ARA_DIG'
MLIBNAME=${LIBNAME}
MCELLNAME=${CELLNAME}
export CDS_PROJECT:=/data/${PROJNAME}/users/${USER}

init:
	@echo "Project name:$(MPROJNAME)"
	@echo "Library name:$(MLIBNAME)"
	@echo "Cell name:$(MCELLNAME)"
	@echo "CDSP name:${CDS_PROJECT}";

drc:
	@mkdir -p /scratch/$(USER)/DRC/$(MCELLNAME); \
	cd /scratch/$(USER)/DRC/$(MCELLNAME); \
	sed 's/USER/$(USER)/g' /data/$(MPROJNAME)/users/$(USER)/pv_batch/pegasusdrcctl_eic | sed 's/CELLNAME/$(MCELLNAME)/g' > /scratch/$(USER)/DRC/$(MCELLNAME)/pegasusdrcctl; \
	/bin/cp -f /data/$(MPROJNAME)/users/$(USER)/pv_batch/drc.config.rul /scratch/$(USER)/DRC/$(MCELLNAME)/.config.rul; \
	/bin/cp -f /data/$(MPROJNAME)/users/$(USER)/pv_batch/drc.technology.rul /scratch/$(USER)/DRC/$(MCELLNAME)/.technology.rul; \
	/tools/cadence/ICADVM201-270/tools/dfII/bin/strmout -library $(MLIBNAME) -topCell $(MCELLNAME) -layerMap /cad/pdks/TSMC/N65/CRN65GP/tsmcN65/tsmcN65.layermap -strmFile /scratch/$(USER)/DRC/$(MCELLNAME)/$(MCELLNAME).gds.gz -logfile /scratch/$(USER)/DRC/$(MCELLNAME)/strmOut_$(MCELLNAME).log -cdslib /data/$(MPROJNAME)/users/$(USER)/cds.lib -ignorePcellEvalFail; \
	/tools/cadence/PEGASUS213-0000/bin/pegasus -top_cell $(MCELLNAME) -ui_data --control /scratch/$(USER)/DRC/$(MCELLNAME)/pegasusdrcctl -log /scratch/$(USER)/DRC/$(MCELLNAME)/pegasus.drc.log /scratch/$(USER)/DRC/$(MCELLNAME)/.config.rul /scratch/$(USER)/DRC/$(MCELLNAME)/.technology.rul; \
	cd /data/$(MPROJNAME)/users/$(USER)/pv_batch

lvs:
	@mkdir -p /scratch/$(USER)/LVS/$(MCELLNAME) ;\
	cd /scratch/$(USER)/LVS/$(MCELLNAME); \
	sed 's/USER/$(USER)/g' /data/$(MPROJNAME)/users/$(USER)/pv_batch/pegasuslvsctl_eic | sed 's/CELLNAME/$(MCELLNAME)/g' > /scratch/$(USER)/LVS/$(MCELLNAME)/pegasuslvsctl ; \
	/bin/cp -f /data/$(MPROJNAME)/users/$(USER)/pv_batch/lvs.config.rul /scratch/$(USER)/LVS/$(MCELLNAME)/.config.rul; \
	/bin/cp -f /data/$(MPROJNAME)/users/$(USER)/pv_batch/lvs.technology.rul /scratch/$(USER)/LVS/$(MCELLNAME)/.technology.rul; \
	/tools/cadence/ICADVM201-270/tools/dfII/bin/strmout -library $(MLIBNAME) -topCell $(MCELLNAME) -layerMap /cad/pdks/TSMC/N65/CRN65GP/tsmcN65/tsmcN65.layermap -strmFile /scratch/$(USER)/LVS/$(MCELLNAME)/$(MCELLNAME).gds.gz -logfile /scratch/$(USER)/LVS/$(MCELLNAME)/strmOut_$(MCELLNAME).log -cdslib /data/$(MPROJNAME)/users/$(USER)/cds.lib -ignorePcellEvalFail; \
	/share/home/akshat/repositories/git/digital/digital/design/common/bin/ltnet ${MLIBNAME} ${MCELLNAME} -f cdl -k -o /scratch/${USER}/LVS/${MCELLNAME}/; \
	/tools/cadence/PEGASUS213-0000/bin/pegasus -lvs -top_cell $(MCELLNAME) -source_top_cell $(MCELLNAME) -spice /scratch/$(USER)/LVS/$(MCELLNAME)/$(MCELLNAME).spi -control /scratch/$(USER)/LVS/$(MCELLNAME)/pegasuslvsctl -ui_data -gdb_data -log /scratch/$(USER)/LVS/$(MCELLNAME)/pegasus.lvs.log /scratch/$(USER)/LVS/$(MCELLNAME)/.config.rul /scratch/$(USER)/LVS/$(MCELLNAME)/.technology.rul;\
	cd /data/$(MPROJNAME)/users/$(USER)/pv_batch

qrc:
	@mkdir -p /scratch/${USER}/QRC/vfi_quantus_${MCELLNAME}; \
	cd /scratch/$(USER)/QRC/$(MCELLNAME) ;\
	sed 's/USER/${USER}/g' /data/$(MPROJNAME)/users/$(USER)/pv_batch/quantusctl_eic.ccl | sed 's/CELLNAME/${MCELLNAME}/g' > /scratch/${USER}/QRC/vfi_quantus_${MCELLNAME}/quantusctl.ccl; \
	/tools/cadence/QUANTUS211//bin/qrc -cmd /scratch/${USER}/QRC/vfi_quantus_${MCELLNAME}/quantusctl.ccl

fill:
	@mkdir -p /scratch/$(USER)/FILL/$(MCELLNAME); \
	cd /scratch/$(USER)/FILL/$(MCELLNAME); \
	/tools/cadence/ICADVM201-270/tools/dfII/bin/strmout -library $(MLIBNAME) -topCell $(MCELLNAME) -layerMap /cad/pdks/TSMC/N65/CRN65GP/tsmcN65/tsmcN65.layermap -strmFile /scratch/$(USER)/FILL/$(MCELLNAME)/$(MCELLNAME).gds.gz -logfile /scratch/$(USER)/FILL/$(MCELLNAME)/strmOut_$(MCELLNAME).log -cdslib /data/$(MPROJNAME)/users/$(USER)/cds.lib -ignorePcellEvalFail; \
	sed 's/USER/$(USER)/g' /data/$(MPROJNAME)/users/$(USER)/pv_batch/Dummy_Metal_PVS_65nm.25a | sed 's/CELLNAME/$(MCELLNAME)/g' > /scratch/$(USER)/FILL/$(MCELLNAME)/Dummy_Metal_PVS_65nm.25a ; \
	sed 's/USER/$(USER)/g' /data/$(MPROJNAME)/users/$(USER)/pv_batch/Dummy_OD_PO_PVS_65nm.25a | sed 's/CELLNAME/$(MCELLNAME)/g' > /scratch/$(USER)/FILL/$(MCELLNAME)/Dummy_OD_PO_PVS_65nm.25a ; \
	/tools/cadence/PEGASUS213-0000/bin/pegasus -fill /scratch/$(USER)/FILL/$(MCELLNAME)/Dummy_Metal_PVS_65nm.25a ; \
	/tools/cadence/PEGASUS213-0000/bin/pegasus -fill /scratch/$(USER)/FILL/$(MCELLNAME)/Dummy_OD_PO_PVS_65nm.25a

top_fill:
	@mkdir -p /scratch/$(USER)/FILL/$(MTOPCELLNAME); \
	cd /scratch/$(USER)/FILL/$(MTOPCELLNAME); \
	/tools/cadence/ICADVM201-270/tools/dfII/bin/strmout -library $(MTOPLIBNAME) -topCell $(MTOPCELLNAME) -layerMap /cad/pdks/TSMC/N65/CRN65GP/tsmcN65/tsmcN65.layermap -strmFile /scratch/$(USER)/FILL/$(MTOPCELLNAME)/$(MTOPCELLNAME).gds.gz -logfile /scratch/$(USER)/FILL/$(MTOPCELLNAME)/strmOut_$(MTOPCELLNAME).log -cdslib /data/$(MPROJNAME)/users/$(USER)/cds.lib -ignorePcellEvalFail; \
	sed 's/USER/$(USER)/g' /data/$(MPROJNAME)/users/$(USER)/pv_batch/Dummy_Metal_PVS_65nm.25a.TOP | sed 's/CELLNAME/$(MTOPCELLNAME)/g' > /scratch/$(USER)/FILL/$(MTOPCELLNAME)/Dummy_Metal_PVS_65nm.25a.TOP ; \
	sed 's/USER/$(USER)/g' /data/$(MPROJNAME)/users/$(USER)/pv_batch/Dummy_OD_PO_PVS_65nm.25a.TOP | sed 's/CELLNAME/$(MTOPCELLNAME)/g' > /scratch/$(USER)/FILL/$(MTOPCELLNAME)/Dummy_OD_PO_PVS_65nm.25a.TOP ; \
	/tools/cadence/PEGASUS213-0000/bin/pegasus -fill /scratch/$(USER)/FILL/$(MTOPCELLNAME)/Dummy_Metal_PVS_65nm.25a.TOP ; \
	/tools/cadence/PEGASUS213-0000/bin/pegasus -fill /scratch/$(USER)/FILL/$(MTOPCELLNAME)/Dummy_OD_PO_PVS_65nm.25a.TOP
