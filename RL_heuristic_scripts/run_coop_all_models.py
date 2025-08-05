import sys, os, re, subprocess
import getpass

username = getpass.getuser()

print(f"Python detected username: {username}")

subject_list_path = None
#subject_list_path = '/media/labs/rsmith/lab-members/cgoldman/Wellbeing/cooperation_task/cooperation_prolific_IDs.csv'
#subject_list_path = 'L:/rsmith/wellbeing/data/raw/coop_local_ids.csv'
results = sys.argv[1]
experiment_mode = sys.argv[2] # indicate local, mturk, or prolific


if experiment_mode == 'prolific':
    subject_list_path = '/media/labs/rsmith/lab-members/cgoldman/Wellbeing/cooperation_task/cooperation_prolific_IDs.csv'
elif experiment_mode == 'local':
    subject_list_path = '/media/labs/rsmith/wellbeing/data/raw/coop_local_ids.csv'
else:
    raise ValueError(f"Unsupported experiment mode: {experiment_mode}")

if username == 'osanchez': 
    ssub_path = '/media/labs/rsmith/lab-members/osanchez/wellbeing/cooperation/scripts/other_models/RL_RW/Final_RL_KPC_heuristic/run_coop_all_models.ssub'
elif username == 'gkozlowski':
    ssub_path = '/media/labs/rsmith/lab-members/gkozlowski/Cooperation/Active_Inference_and_RL_Models_VB_Cooperation_Task/RL_heuristic_scripts/run_coop_all_models.ssub'
elif username == 'kchou':
    ssub_path = '/media/labs/rsmith/lab-members/kchou/COP_wellbeing/Final_RL_KPC_heuristic/run_coop_all_models.ssub'
else:
    raise ValueError(f"Unknown username: {username}")

models = [
    {'field': 'beta,cl,cr,V0,alpha,psi,gamma'},
    {'field': 'beta,cl,cr,V0,alpha_win,alpha_neutral,alpha_loss,psi,gamma'},
    {'field': 'beta,cl,cr,V0,alpha,psi_win,psi_neutral,psi_loss,gamma'},
    {'field': 'beta,cl,cr,V0,alpha,eta,gamma'},
    {'field': 'beta,cl,cr,V0,alpha,eta,psi,gamma'},
    {'field': 'beta_0,c,cl,cr,V0,alpha,psi,gamma'},
    {'field': 'beta_0,c,cl,cr,V0,alpha_win,alpha_neutral,alpha_loss,psi,gamma'},
    {'field': 'beta_0,c,cl,cr,V0,alpha,psi_win,psi_neutral,psi_loss,gamma'}
    ]   


if not os.path.exists(results):
    os.makedirs(results)
    print(f"Created results directory {results}")

if not os.path.exists(f"{results}/logs"):
    os.makedirs(f"{results}/logs")
    print(f"Created results-logs directory {results}/logs")

subjects = []
with open(subject_list_path) as infile:
    next(infile)    
    for line in infile:
        subjects.append(line.strip())
    
#ssub_path = '/media/labs/rsmith/lab-members/osanchez/wellbeing/cooperation/scripts/other_models/RL_RW/Final_RL_KPC_heuristic/run_coop_all_models.ssub'

    
for index, model in enumerate(models, start=1):
    combined_results_dir = os.path.join(results, f"model{index}")
    field = model['field']
    
    if not os.path.exists(f"{combined_results_dir}/logs"):
        os.makedirs(f"{combined_results_dir}/logs")
        print(f"Created results-logs directory {combined_results_dir}/logs")
    
    for subject in subjects:
        #ssub_path = '/media/labs/rsmith/lab-members/osanchez/wellbeing/cooperation/scripts/other_models/RL_RW/Final_RL_KPC_heuristic/run_coop_all_models.ssub'
        stdout_name = f"{combined_results_dir}/logs/{subject}-%J.stdout"
        stderr_name = f"{combined_results_dir}/logs/{subject}-%J.stderr"
    
        jobname = f'coop_fit-{index}_RL-{subject}'
        os.system(f"sbatch -J {jobname} -o {stdout_name} -e {stderr_name} {ssub_path} {subject} {combined_results_dir} {field} {experiment_mode}")
        #os.system(f"sbatch -J {jobname} -o {stdout_name} -e {stderr_name} {ssub_path} \"{subject}\" \"{combined_results_dir}\" \"{field}\" \"{experiment_mode}\"")
    
        print(f"SUBMITTED JOB [{jobname}]")
        
    # ml Python/3.11.5-GCCcore-13.2.0
    ###python3 /media/labs/rsmith/lab-members/osanchez/wellbeing/cooperation/scripts/other_models/RL_RW/Final_RL_KPC_heuristic/run_coop_all_models.py  /media/labs/rsmith/lab-members/osanchez/wellbeing/cooperation/scripts/other_models/RL_RW/Final_RL_KPC_heuristic/model_output/ "prolific"
    #python3 /media/labs/rsmith/lab-members/gkozlowski/Cooperation/Active_Inference_and_RL_Models_VB_Cooperation_Task/RL_heuristic_scripts/run_coop_all_models.py  /media/labs/rsmith/lab-members/gkozlowski/Cooperation/Results/model_output_080425 "local"

    ## joblist | grep coop | grep -Po 98.... | xargs scancel
    #OR
    ## joblist | grep coop | grep -Po 43... |xargs -n1 scancel