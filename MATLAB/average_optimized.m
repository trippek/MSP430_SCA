function [pt_unique, averaged_traces] = average_optimized(pt, traces)

% timing
tic;

% indexing variable
index = 1;

% copies
copies = zeros(numel(pt(:,1)), 1);
copies(index) = copies(index) + 1;

% groups
groups = zeros(numel(pt(:,1)), 1);
groups(index) = groups(index) + 1;

% unique plaintext
pt_unique = zeros(numel(pt(:,1)), 16);
pt_unique(index,:) = pt(index,:);

for i = 1:numel(pt(:,1))-1
    if ~all((pt(i,:) ~= pt((i+1),:)) == 0)
        index = index + 1;
    end
    groups(i + 1) = index;
    copies(index) = copies(index) + 1;
    pt_unique(index,:) = pt(i+1,:);
end

% remove trailing zeros
lastNonZeroIndex = find(copies, 1, 'last');
copies = copies(1:lastNonZeroIndex);

lastNonZeroRow = find(pt_unique(:,1), 1, 'last');
pt_unique = pt_unique(1:lastNonZeroRow,:);

% initialize array for averages
average_traces = zeros(index, size(traces, 2));

for i = 1:numel(traces(1,:))
    average_traces(:, i) = accumarray(groups, traces(:, i));
    % disp(['Completed column ' num2str(i) ' of traces matrix.']);
end

% set test_function equal to the variable being tested
average_traces = average_traces ./ copies;
averaged_traces = average_traces;

% timing
elapsed_time = toc;
disp(['Elapsed time to average synchronized traces: ' num2str(elapsed_time) ' seconds']);

end