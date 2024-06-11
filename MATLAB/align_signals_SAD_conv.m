function aligned_matrix = align_signals_SAD_conv(matrix)
    
% timing
tic;

% Get the number of rows in the matrix
num_rows = size(matrix, 1);
    
% Initialize an empty matrix to store the aligned signals
aligned_matrix = zeros(size(matrix));
    
% Iterate through each row of the matrix
for i = 1:num_rows
    % Get the current row
    signal = matrix(i, :);
    
    % Compute sum of absolute differences with the first row
    sad = conv(abs(diff(signal)), abs(diff(matrix(1, :))), 'valid');
    
    % Find index of minimum SAD
    [~, min_index] = min(sad);
    
    % Calculate the shift
    shift = min_index - 1;
    
    % Shift the current row to align with the first row
    aligned_signal = circshift(signal, [-shift, 0]);
    
    % Store the aligned signal in the aligned matrix
    aligned_matrix(i, :) = aligned_signal;
end

% timing
elapsed_time = toc;
disp(['Elapsed time to synchronize the traces matrix using SAD conv: ' num2str(elapsed_time) ' seconds']);

end