% main script !

directory = 'E:\srand1000_2000';
[pt, traces] = plaintext(directory);
aligned_matrix_SAD = align_signals_SAD_conv(traces);
[pt_unique, average_traces] = average_optimized(pt, aligned_matrix_SAD);

disp(['Number of unique traces: ' num2str(numel(average_traces(:,1)))]);

% save commands
% save('traces1000_2000.mat', 'traces', '-v7.3');
% save('pt1000_2000.mat', 'pt');