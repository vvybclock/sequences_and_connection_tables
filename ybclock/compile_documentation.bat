%windir%\System32\WindowsPowerShell\v1.0\powershell.exe -ExecutionPolicy ByPass -Command "& '%USERPROFILE%\Anaconda3\shell\condabin\conda-hook.ps1' ; conda activate '%USERPROFILE%\Anaconda3' ; conda activate ybclock; cd '%USERPROFILE%\labscript-suite\userlib\labscriptlib\ybclock'; pdoc3 -c latex_math=True --html labscriptlib.ybclock --force --skip-errors"
%windir%\System32\WindowsPowerShell\v1.0\powershell.exe -ExecutionPolicy ByPass -Command "& '%USERPROFILE%\Anaconda3\shell\condabin\conda-hook.ps1' ; conda activate '%USERPROFILE%\Anaconda3' ; conda activate ybclock; cd '%USERPROFILE%\labscript-suite\userlib\labscriptlib\ybclock'; pdoc3 -c latex_math=True --html user_devices --force --skip-errors"



