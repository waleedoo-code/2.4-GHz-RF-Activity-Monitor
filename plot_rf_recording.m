clear;
clc;

% Choose your recording
[name, folder] = uigetfile('*.bin', 'Select recording.bin');

if isequal(name, 0)
    return;
end

% Read the file as bytes
file = fopen(fullfile(folder, name), 'rb');
if file == -1
    error('Could not open the recording.');
end

raw = fread(file, Inf, 'uint8');
fclose(file);

% Each saved record: 4 timestamp bytes + 126 channel counts
if isempty(raw) || mod(numel(raw), 130) ~= 0
    error('File is empty or contains an incomplete record.');
end

records = reshape(raw, 130, []);

% Decode the little-endian timestamp, then convert ms to hours
time_ms = records(1,:) ...
    + records(2,:) * 256 ...
    + records(3,:) * 65536 ...
    + records(4,:) * 16777216;

time_hours = time_ms / 3600000;

% Convert counts out of 50 into detection percentages
counts = records(5:130, :).';
activity = counts / 50 * 100;

frequency = 2400:2525;

% Draw the 3D graph
figure;
surf(frequency, time_hours, activity, 'EdgeColor', 'none');

xlabel('Frequency (MHz)');
ylabel('Time since recording started (hours)');
zlabel('Detections (%)');
title('2.4 GHz activity recording');

colorbar;
caxis([0 100]);
zlim([0 100]);
axis tight;
view(45, 35);
grid on;
rotate3d on;

fprintf('Loaded %d scans.\n', size(counts, 1));
fprintf('Last scan: %.2f hours.\n', time_hours(end));
