from datetime import datetime, timedelta
import pandas as pd
from ecflow import Trigger, Defs
from os.path import join

nMembers        = 1         # 4
hindcastYear1   = 1993      # 1993
hindcastYear2   = 1993      # 2019

hindcast_month_periods = 5 # 62

start_month_day = "0101"    # "1101"

model_dt = pd.Timedelta(seconds = 900)  # 900 sec

nNodes      = 4
nProcsNEMO  = 252
nProcsXIOS  = 4
nProcsTOTAL = nProcsNEMO + nProcsXIOS
nProcsMerge = 64

defs = Defs()

suite = defs.add_suite("seaclim_ensemble")

suite.add_variable("ECF_JOB_CMD"    , "sbatch %ECF_JOB% 2>&1")

main_dir = "/mnt/lustre/scratch/nlsas/home/empresa/now/iba/seaclim"

suite.add_variable("ECF_HOME"           , "/home/empresa/now/iba/ecflow_server")
suite.add_variable("MAIN_DIR"           , f"{main_dir}/")
suite.add_variable("ECF_INCLUDE"        , f"{main_dir}/include")
suite.add_variable("ECF_FILES"          , f"{main_dir}/src/")
suite.add_variable("STATIC_BASE_DIR"    , f"{main_dir}/static")
suite.add_variable("INPUT_BASE_DIR"     , f"{main_dir}/inputs")
suite.add_variable("OUTPUT_BASE_DIR"    , f"{main_dir}/outputs")    # this must be in a spacious filesystem
suite.add_variable("RESTART_BASE_DIR"   , f"{main_dir}/restarts")
suite.add_variable("CALC_BASE_DIR"      , f"{main_dir}/runs")
suite.add_variable("LOG_BASE_DIR"       , f"{main_dir}/logs")
suite.add_variable("NPROCS_NEMO"        , nProcsNEMO)
suite.add_variable("NPROCS_XIOS"        , nProcsXIOS)
suite.add_variable("NPROCS_TOTAL"       , nProcsTOTAL)
suite.add_variable("NPROCS_MERGE"       , nProcsMerge)

suite.add_variable("START_MONTH_DAY"    , start_month_day)  # should be "1101", I put "0101" for some test 

suite.add_variable("HOST"               , "login210-19")
suite.add_variable("USER"               , "emnowiba")
suite.add_variable("ECF_TRYNO"          , "1")
suite.add_variable("MEMBERS"            , nMembers)              # 4
suite.add_variable("CYCLES"             , hindcast_month_periods) # 62

suite.add_variable("HINDCAST_YEAR1"     , hindcastYear1) # 1993
suite.add_variable("HINDCAST_YEAR2"     , hindcastYear2) # 2019

suite.add_variable("run_time"           ,"00:01:00")

suite.add_variable("NEMOEXE"        ,"/mnt/netapp2/Store_uni/home/empresa/now/iba/codes/nemo5_moi/nemoi/cfgs/MOI_FT3-X2-oper/BLD/bin/nemo.exe")    # absolute path of NEMO executable
suite.add_variable("XIOSEXE"        ,"/mnt/netapp2/Store_uni/home/empresa/now/iba/codes/XIOS2/xios-install/bin/xios_server.exe")    # absolute path of XIOS executable
suite.add_variable("MERGEMPI_EXE"   ,"/mnt/netapp2/Store_uni/home/empresa/now/iba/codes/nemo5_moi/nemoi/tools/MERGE_MPP/BLD/bin/mergefile_mpi.exe" )
suite.add_variable("MERGE_EXE"      ,"/mnt/netapp2/Store_uni/home/empresa/now/iba/codes/nemo5_moi/nemoi/tools/MERGE_MPP/BLD/bin/mergefile4.exe" )

suite.add_variable("NNODES"         , nNodes)

membersList = [str(mem).zfill(3) for mem in range(nMembers)]    # ['000','001','002',...]

#################### families / tasks definition #################

create_log_folders = suite.add_task("create_log_folders")
create_log_folders.add_variable("run_time",'00:05:00')

for member in membersList:
    
    member_family = suite.add_family(f"member_{member}")
    member_family.add( Trigger( "create_log_folders == complete") )

    member_family.add_variable("MEMBER",member)

    for hindcast_start_year in range(hindcastYear1, hindcastYear2+1):

        hindcast_end_year = hindcast_start_year + 5

        hindcast_family = member_family.add_family(f"hindcast_{hindcast_start_year}_{hindcast_end_year}")

        hindcast_family.add_variable("HINDCAST_YEAR"        , f"{hindcast_start_year}")
        hindcast_family.add_variable("HINDCAST_START_DATE"  , f"{hindcast_start_year}{start_month_day}")  # 1st Nov
        hindcast_family.add_variable("HINDCAST_END_DATE"    , f"{hindcast_end_year}1231")      # 31st Dec
        hindcast_family.add_variable("HINDCAST_PERIOD"      , f"{hindcast_start_year}-{hindcast_end_year}")

        hindcast_start_date = "%d%s" % (hindcast_start_year,start_month_day)    # 1101 of each year

        # dates of monthly sub-simulations (or cycles) 
        hindcast_periods = pd.date_range(start=hindcast_start_date ,periods=hindcast_month_periods+1,freq="MS")

        nit000 = 1
        nitend = 0

        # hindcast_periods array (example for hindcast 19931101)
        
        #   |       |       |       |       |       
        #
        #   1       1       1       1       Y
        #   9       9       9       9       Y
        #   9       9       9       9       Y
        #   3       3       4       4       Y
        #   1       1       0       0       m
        #   1       2       1       2       m
        #   0       0       0       0       D
        #   1       1       1       1       D
        #
        #   |       |       |       |       |
        
        #   0       1       2       3       n   python index to access to hindcast_periods array
        #   -------->
        #       1                               cycle number (1 based numbering)
        #           -------->    
        #               2                       cycle number (1 based numbering)
        #                   -------->  
        #                       3               cycle number (1 based numbering)    

        for icycle in range(1,hindcast_month_periods+1):    # monthly sub-simulation or cycle 

            icyclem1 = icycle-1

            cycle_duration = hindcast_periods[icycle] - hindcast_periods[icycle-1]

            cycle_start_date        = hindcast_periods[icycle-1]
            if icycle > 1:     
                cycle_start_date_previous   = hindcast_periods[icycle-2]    # see plot above to justify the index
            else: 
                cycle_start_date_previous   = pd.Timestamp("1900-1-1")  # I set a nonsense date (should not be used)
                     
            cycle_start_date_str            = cycle_start_date.strftime("%Y%m%d")
            cycle_start_date_previous_str   = cycle_start_date_previous.strftime("%Y%m%d")
            cycle_start_year_str            = cycle_start_date.strftime("%Y")
            cycle_start_month_str           = cycle_start_date.strftime("%m").zfill(2)
            cycle_last_date                 = hindcast_periods[icycle]-pd.Timedelta(days=1) # the last simulated day of cyle. Is less 
            cycle_last_date_str             = cycle_last_date.strftime("%Y%m%d")            # than init date of following cycle
            
            #print(cycle_start_date)
            
            n_model_steps = int(cycle_duration / model_dt)                                  # number of model time steps in this cycle
            n_days = int(cycle_duration / pd.Timedelta(days=1))                             # number of simulated days in this cycle
           
            nitend = nitend + n_model_steps            
            
            #print(n_model_steps)
           
            cycle_family = hindcast_family.add_family(f"CYCLE_{str(icycle).zfill(2)}")
            cycle_family.add_variable("NN_IT000",nit000)
            cycle_family.add_variable("NN_ITEND",nitend)

            nit000 += n_model_steps

            if icycle > 1:
                cycle_family.add( Trigger ( f"CYCLE_{str(icyclem1).zfill(2)}/move_rst == complete"  ) )

            cycle_family.add_variable("CYCLE_NUMBER"            , str(icycle).zfill(2))             # 01,02,03   
            cycle_family.add_variable("CYCLE_NUMBER_M1"         , str(icyclem1).zfill(2))           # 00,01,02
            cycle_family.add_variable("CYCLE_START_DATE"        , cycle_start_date_str)             # YYYYmmdd
            cycle_family.add_variable("CYCLE_START_DATE_PREVIOUS", cycle_start_date_previous_str)   # YYYYmmdd
            cycle_family.add_variable("CYCLE_START_YEAR"        , cycle_start_year_str)             # YYYY
            cycle_family.add_variable("CYCLE_START_MONTH"       , cycle_start_month_str)            # mm           
            cycle_family.add_variable("MODEL_STEPS"             , n_model_steps)                    # int
            cycle_family.add_variable("CYCLE_LAST_DATE"         , cycle_last_date_str)              # YYYYmmdd
            cycle_family.add_variable("CYCLE_DAYS"              , n_days)                           # int
            
            task_prepare_run = cycle_family.add_task(f"prepare_run")    

            task_recup_rst = cycle_family.add_task(f"recup_rst")
            task_recup_rst.add( Trigger( "prepare_run == complete") )            

            task_recup_atm = cycle_family.add_task(f"recup_atm")
            task_recup_atm.add( Trigger( "prepare_run == complete") )
            
            task_recup_bdy = cycle_family.add_task(f"recup_bdy")
            task_recup_bdy.add( Trigger( "prepare_run == complete") )

            task_model_run = cycle_family.add_task(f"model_run")
            task_model_run.add( Trigger ( "recup_rst == complete and recup_atm == complete and recup_bdy == complete" ) )
            task_model_run.add_variable("run_time",'00:30:00')

            #task_fake_model = cycle_family.add_task(f"fake_model")
            #task_fake_model.add( Trigger ( "recup_atm == complete and recup_bdy == complete" ))

            # task move restart
            task_move_rst = cycle_family.add_task(f"move_rst")
            task_move_rst.add( Trigger ( "model_run == complete"))
            
            # task merge / move output
            task_merge_mv_out = cycle_family.add_task(f"merge_mv_out")
            task_merge_mv_out.add( Trigger( "model_run == complete") )
            task_merge_mv_out.add_variable("run_time","00:10:00")

            # task clean calc folder

defs.save_as_defs("seaclim_ensemble.def")
