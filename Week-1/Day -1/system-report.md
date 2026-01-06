                                                        Hestabit Learning & Development
                                                                Week-1

Day 1 : SYSTEM REVERSE ENGINEERING + NODE & TERMINAL MASTERING

IDENTIFY AND DOCUMENT : -
-OS Version
-Current Shell (bash/zsh/powershell).
-Node binary path (which node).
-NPM global installation path.
-All path entries that include "node" or npm.

-> OS Versions:

-What is an OS?
    An OPERATING SYSTEM (OS) is a collection of software that manages a computer's hardware and applications by allocation of resources, including memory, CPU, input/output devices and file storage.
-OS Versions:
    It refers to the specific releases or iteration of operating systems.
    Generally speaking , it talks about the evolution of the operating systems over the period of time , starting from 1950 , where the first OS was discovered, and moving onto the changes and new discoveries that made the current systems. The most common and popular operating system in today's time are : Apple MacOS, Microsoft Windows, Googles' Android OS, Linux Operating System, and Apple ios.
    
=> Finding the OS version in Linux:

-COMMAND :
            uname -r
It gives the Linux Kernel version of your current operating system
        cat /etc/os-release
It gives the complete information about the release of the version and its distribution(Linux).
            
! [An Screenshot image of OS version command & output](/home/sparshagarwal/Pictures/Screenshots/Screenshot from 2026-01-06 13-04-55.png)
            
            OR 
            
-COMMAND : 
        lsb_release -a
It gives the Linux Standard Base module information about the operating system, including the established standards and guidelines across Linux Distributions.

! [An Screenshot image of OS version command & output](/home/sparshagarwal/Pictures/Screenshots/Screenshot from 2026-01-06 16-21-11.png)


->Current Shell (bash/zsh/powershell):

What is Shell?
    It is a computing interface of an operating system (OS) that acts as a translator, taking the users' commands and converting them into actions for the core OS (kernel) to execute, bridging or reducing the gap between user and hardware.
Generally, its of two types:
>Command-Line Shells (CLI) - e.g. Bash, Zsh, PowerShell
>Graphical Shells - e.g. Windows Explorer

=> Checking the working (current) shell in Linux:

-COMMAND : 
            echo $SHELL
It gives the current/working shell of the system on the console.

! [An Screenshot image of shell command & output](/home/sparshagarwal/Pictures/Screenshots/Screenshot from 2026-01-06 14-09-48.png)

->Node Binary Path:
    It refers to the location of the node executable file on a system, which is used to run JavaScript code outside the browser.

=> Finding the Node Binary Path:

-COMMAND : 
            which node
It gives the absolute path to the Node.js executable files on a system.

But before executing this command , make sure to install Node.js on the system 
-COMMAND :
            sudo apt install -y nodejs npm
It installs the Node.js and NPM on the system using the packages provided by the operating system, while acting as a superuser.

! [An Screenshot image of Node.js & NPM installation command & output](/home/sparshagarwal/Pictures/Screenshots/Screenshot from 2026-01-06 14-10-42.png)
! [An Screenshot image of Node.js & NPM installation command & output](/home/sparshagarwal/Pictures/Screenshots/Screenshot from 2026-01-06 14-11-28.png)

! [An Screenshot image of finding binary node path command & output](/home/sparshagarwal/Pictures/Screenshots/Screenshot from 2026-01-06 14-11-49.png)


-> NPM Global Installation Path:
    It refers to the location of the globally installed packages typically depending on a system & how Node.js was installed.
    
=> Finding NPM Global Installation Path:

-COMMAND :
            npm root -g
It gives the path to the directory where all the global packages are installed.

! [An Screenshot image of the finding npm global installation path command & output](/home/sparshagarwal/Pictures/Screenshots/Screenshot from 2026-01-06 14-11-58.png)


->All path entries that include "node" or npm:
    It refers to the searching of all the files and directories, precisely entries that include 'node' or 'npm' in their path.

=> Finding the paths:

-COMMAND : 
            echo $PATH | tr ':' '\n' | grep -i "node\|npm"
It gives all the entries or the path where node or npm is included.

! [An Screenshot image of finding all entries with command & output](/home/sparshagarwal/Pictures/Screenshots/Screenshot from 2026-01-06 14-14-03.png)

This usually gives no output when executed on NPM, while the command and system are initialized correctly.
Therefore, it is executed using NVM (Node Version Manager)
