# To customize the plotting you can import the PlotConfig class, see below for usage examples.
# If you leave that out, the plots will have gneric color maps and values ranges.
import sys
sys.path.append('../../auxiliary')
from plot_config import PlotConfig

root = "/silod8/karsten"

name = "compare_to_uncoupled"

reference = {
    "T_2M_AV" : {  "reference-file-pattern" : root+"/work/IOW_ESM_CCLM_uncoupled/output/CCLM_RUN01_monthly/CCLM_Eurocordex/*/T_2M_AV.nc",
                   "reference-variable-name" : "T_2M_AV",
                   "plot-config-anomaly" : PlotConfig("T_2M_AV", min_value = -6.75, max_value = 6.75, delta_value = 0.5, color_map = 'seismic'),
             },

    "DAY_PREC" : {  "reference-file-pattern" : root+"/work/IOW_ESM_CCLM_uncoupled/output/CCLM_RUN01_monthly/CCLM_Eurocordex/*/DAY_PREC.nc",
                    "reference-variable-name" : "DAY_PREC",
                    "plot-config-anomaly" : PlotConfig("DAY_PREC", min_value = -0.5, max_value = 0.5, delta_value = 0.1, color_map = 'BrBG')
                 },    

    "ASWD_S" : {  "reference-file-pattern" : root+"/work/IOW_ESM_CCLM_uncoupled/output/CCLM_RUN01_monthly/CCLM_Eurocordex/*/ASWD_S.nc",
                  "reference-variable-name" : "ASWD_S",
                  "plot-config-anomaly" : PlotConfig("ASWD_S", min_value = -10.0, max_value = 10.0, delta_value = 2.0, color_map = 'seismic')
               },  
    
    "ALWD_S" : {  "reference-file-pattern" : root+"/work/IOW_ESM_CCLM_uncoupled/output/CCLM_RUN01_monthly/CCLM_Eurocordex/*/ALWD_S.nc",
                  "reference-variable-name" : "ALWD_S",
                  "plot-config-anomaly" : PlotConfig("ALWD_S", min_value = -10.0, max_value = 10.0, delta_value = 2.0, color_map = 'seismic')
               },     
               
    "SPEED_10M_AV" : {  "reference-file-pattern" : root+"/work/IOW_ESM_CCLM_uncoupled/output/CCLM_RUN01_monthly/CCLM_Eurocordex/*/PEED_10M_AV.nc",
                  "reference-variable-name" : "SPEED_10M_AV",
                  "plot-config-anomaly" : PlotConfig("SPEED_10M_AV", min_value = -1.5, max_value = 1.5, delta_value = 0.3, color_map = 'seismic')
               }, 
               
    "PMSL_AV" : {  "reference-file-pattern" : root+"/work/IOW_ESM_CCLM_uncoupled/output/CCLM_RUN01_monthly/CCLM_Eurocordex/*/PMSL_AV.nc",
                  "reference-variable-name" : "PMSL_AV",
                  "plot-config-anomaly" : PlotConfig("PMSL_AV", min_value = -150.0, max_value = 150.0, delta_value = 30.0, color_map = 'seismic')
               }, 
    
    "AEVAP_S" : {  "reference-file-pattern" : root+"/work/IOW_ESM_CCLM_uncoupled/output/CCLM_RUN01_monthly/CCLM_Eurocordex/*/AEVAP_S.nc",
                  "reference-variable-name" : "AEVAP_S",
                  "plot-config-anomaly" : PlotConfig("AEVAP_S", min_value = -1.0, max_value = 1.0, delta_value = 0.2, color_map = 'seismic')
               },  
    
    "ALHFL_S" : {  "reference-file-pattern" : root+"/work/IOW_ESM_CCLM_uncoupled/output/CCLM_RUN01_monthly/CCLM_Eurocordex/*/ALHFL_S.nc",
              "reference-variable-name" : "ALHFL_S",
              "plot-config-anomaly" : PlotConfig("ALHFL_S", min_value = -20.0, max_value = 20.0, delta_value = 4.0, color_map = 'seismic')
           },
    
    "ASHFL_S" : {  "reference-file-pattern" : root+"/work/IOW_ESM_CCLM_uncoupled/output/CCLM_RUN01_monthly/CCLM_Eurocordex/*/ASHFL_S.nc",
              "reference-variable-name" : "ASHFL_S",
              "plot-config-anomaly" : PlotConfig("ASHFL_S", min_value = -10.0, max_value = 10.0, delta_value = 2.0, color_map = 'seismic')
           },    
    "CLCT" : {  "reference-file-pattern" : root+"/work/IOW_ESM_CCLM_uncoupled/output/CCLM_RUN01_monthly/CCLM_Eurocordex/*/CLCT.nc",
              "reference-variable-name" : "CLCT",
              "plot-config-anomaly" : PlotConfig("CLCT", min_value = -0.5, max_value = 0.5, delta_value = 0.1, color_map = 'seismic')
           }, 
    
    "AUMFL_S" : {  "reference-file-pattern" : root+"/work/IOW_ESM_CCLM_uncoupled/output/CCLM_RUN01_monthly/CCLM_Eurocordex/*/AUMFL_S.nc",
              "reference-variable-name" : "AUMFL_S",
              "plot-config-anomaly" : PlotConfig("AUMFL_S", min_value = -0.01, max_value = 0.01, delta_value = 0.002, color_map = 'seismic')
           }, 
    
    "AVMFL_S" : {  "reference-file-pattern" : root+"/work/IOW_ESM_CCLM_uncoupled/output/CCLM_RUN01_monthly/CCLM_Eurocordex/*/AVMFL_S.nc",
              "reference-variable-name" : "AVMFL_S",
              "plot-config-anomaly" : PlotConfig("AVMFL_S", min_value = -0.01, max_value = 0.01, delta_value = 0.002, color_map = 'seismic')
           },  
    
    "T" : {  "reference-file-pattern" : root+"/work/IOW_ESM_CCLM_uncoupled/output/CCLM_RUN01_monthly/CCLM_Eurocordex/*/T.nc",
              "reference-variable-name" : "T",
              "plot-config-anomaly" : PlotConfig("T", min_value = -0.01, max_value = 0.01, delta_value = 0.002, color_map = 'seismic')
           },     
}
         

