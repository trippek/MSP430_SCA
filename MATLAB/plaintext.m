function [pt, traces] = plaintext(directory)

% timing
tic;

% Get a list of all files in the directory
file_list = dir(fullfile(directory, 'power_trace_*.mat'));

% Calculate the number of files in each category
total_files = numel(file_list);
files_per_category = floor(total_files / 3);

% Allocate space for a plaintext and trace arrays
pt = zeros(files_per_category, 16);
% Ideal column for traces is 1127500 - half/third/fifth for MATLAB (could decrease
% resolution on oscilloscope) - could also parse into multiple matricies OR
% lower the resolution later in the code when sampling the trace data
traces = zeros(files_per_category, 375834);

% Offset variable to keep index correct pt when data is invalid
k = 0;

% Accessing the file in the directory
for i = 1:files_per_category
    file_path = fullfile(directory, file_list(i + files_per_category).name);
    load(file_path, 'D4');
    sample_locations = find_transition_indices(D4);

    data = load(file_path, 'D0', 'D1', 'D2', 'D3');
    % try-catch for invalid plaintext data
    try
        % Plaintext
        D0 = data.D0(sample_locations(1:16));
        D1 = data.D1(sample_locations(1:16));
        D2 = data.D2(sample_locations(1:16));
        D3 = data.D3(sample_locations(1:16));
        
        file_path = fullfile(directory, file_list(i).name);
        data = load(file_path, 'D4', 'D5', 'D6', 'D7');
        D4 = data.D4(sample_locations(1:16));
        D5 = data.D5(sample_locations(1:16));
        D6 = data.D6(sample_locations(1:16));
        D7 = data.D7(sample_locations(1:16));
    
        bits = [D7, D6, D5, D4, D3, D2, D1, D0];
        % previous code
        % reshaped_bits = reshape(bits', 4, [])';
        % pt_temp = sum((reshaped_bits .* uint8([8 4 2 1])), 2);
        
        % corrected code - could case issues later****
        reshaped_bits = reshape(bits', 8, [])';
        pt_temp = sum((reshaped_bits .* uint8([128 64 32 16 8 4 2 1])), 2);    
        
        pt(i - k, :) = transpose(pt_temp);

        % Power trace data
        file_path = fullfile(directory, file_list(i + 2*files_per_category).name);
        single_trace = load(file_path, 'data');

        % every other data point is being sampled to fit into the array
        traces(i - k, :) = transpose(single_trace.data(sample_locations(17):3:sample_locations(17)+1127499));

    catch exception
        if strcmp(exception.identifier, 'MATLAB:badsubscript')
            % Handle the case where the index exceeds the number of elements
            % Display an error message or perform some other action
            % disp('Error: Index exceeds the number of array elements');
            k = k + 1;
        else
            % If it's a different type of error, rethrow the exception
            rethrow(exception);
        end
    end
end

% trim arrays to get rid of zeros from invalid data
pt = pt(1:(files_per_category - k), :);
traces = traces(1:(files_per_category - k), :);

% timing
elapsed_time = toc;
disp(['Elapsed time to convert from raw data to plaintext and traces matricies: ' num2str(elapsed_time) ' seconds']);

end