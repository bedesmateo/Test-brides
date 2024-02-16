% ContinuityTest
% Send signals to all channels one by one
% chValue=[0:63] pwmValue=[0:65535]
function [y]=ContinuityTest(pwmValue,name)

global sObj1;
global sObj2;
global sObj3;

if name == 1
    sObj = sObj1;
elseif name == 2
    sObj = sObj2;
elseif name == 3
    sObj = sObj3;
else
    disp('ERROR: name not valide');
    return;
    
end

pwmString = dec2hex(pwmValue,4);
pwmString_0 = dec2hex(0,4);

chIn = [ 4 5 6 7 9 10 13 14 17 18 23 24 25 26 29 30 31 32 35 36 38 39 44 45 48 49 50 51 53 54 55 ]

% chValue = zeros(1,60);
% chString = zeros(1,60);
% chString = string(chString);
% cmdString = zeros(1,60);
% cmdString = string(cmdString);
% cmdCode_rply = zeros(1,60);

chValue = zeros(1,60);
chString = zeros(1,size(chIn,2));
chString = string(chString);
cmdString = zeros(1,size(chIn,2));
cmdString = string(cmdString);
cmdCode_rply = zeros(1,size(chIn,2));

cmdCode_rply = string(cmdCode_rply);
smFlag = cmdCode_rply;
for i = 1:60
    chValue(1,i)=i;
end
disp(chValue)
disp(sObj);

cmdCode = 'A';

pause(10)

for i = 1:size(chIn,2)
    % chString(1,i)=dec2hex(chValue(1,i),2); %Select ch i
    chString(1,i)=dec2hex(chIn(1,i),2); %Select ch i

    cmdString(1,i)=sprintf('%s%s%s',cmdCode,chString(1,i),pwmString);
    if(isvalid(sObj)~=1)
        disp('ERROR: serial device not connected or SerialSETUP command not issued');
        return;
    else
        fprintf(sObj,cmdString(1,i));
    end
    reply = fscanf(sObj,'%c%x');
    cmdCode_rply(1,i)=char(reply(1));
    smFlag(1,i)=reply(2);  %ch i is at pwmValue

    pause(10); 
    
    cmdString(1,i)=sprintf('%s%s%s',cmdCode,chString(1,i),pwmString_0);
    if(isvalid(sObj)~=1)
        disp('ERROR: serial device not connected or SerialSETUP command not issued');
        return;
    else
        fprintf(sObj,cmdString(1,i));
    end
    reply = fscanf(sObj,'%c%x');
    cmdCode_rply(1,i)=char(reply(1));
    smFlag(1,i)=reply(2);  %ch i is at 0

    pause(3);

    disp('Ch i Done');

end
disp('end');

y=smFlag;

end

