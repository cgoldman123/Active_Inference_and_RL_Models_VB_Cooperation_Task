root = 'L:/';
file_path = [root 'rsmith/wellbeing/data/raw/'];

d = dir(file_path);
subids = {d([d.isdir]).name}.';
subids = subids(~ismember(subids, {'.','..'}));

all_subjectids = erase(subids, 'sub-');

T = table(all_subjectids, 'VariableNames', {'SubjectID'});
writetable(T, fullfile(file_path, 'coop_local_ids.csv'));