% Step 1: Open the binary file for reading
fileID = fopen('1329/ir20x.b', 'rb');
if fileID == -1
    error('Cannot open file. Check the file path or permissions.');
end

% Step 2: Read the data as 4-byte unsigned integers
data = fread(fileID, inf, 'uint32');

% Step 3: Close the binary file
fclose(fileID);

% Step 4: Convert the data to hexadecimal strings
hexData = dec2hex(data);

% Step 5: Open the output text file for writing
outputFileID = fopen('ir20x.txt', 'w');
if outputFileID == -1
    error('Cannot create output file.');
end

% Step 6: Write the hexadecimal values to the text file
fprintf(outputFileID, '%08X\n', hexData'); % Each value is 8 hex digits, uppercase

% Step 7: Close the text file
fclose(outputFileID);

disp('Conversion complete! Hexadecimal data written to ir20x.txt.');
